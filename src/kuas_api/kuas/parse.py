# -*- coding: utf-8 -*-

from lxml import etree


sections_time = []
weekdays_abbr = []


def parse(fncid, content):
    if fncid in parse_function:
        return parse_function[fncid](content)
    else:
        return content


def course(cont):
    """Parse raw kuas ap course data
    Return:
        parse data: json
        have_saturday: bool
        have_sunday: bool
        except_text: string
    """

    root = etree.HTML(cont)

    try:
        center = root.xpath("//center")[0]
        center_text = list(center.itertext())[0]
    except:
        center = ""
        center_text = ""

    # Return if no course data
    if center_text.startswith(u'學生目前無選課資料!'):
        return {}

    tbody = root.xpath("//table")[-1]

    course_table = []
    for sections, r in enumerate(tbody[1:]):
        section = ""
        start_time = ""
        end_time = ""

        for weekends, c in enumerate(r.xpath("td")):
            classes = {"title": "", "date": {},
                       "location": {}, "instructors": []}

            r = list(
                filter(
                    lambda x: x,
                    map(lambda x: x.replace("\xa0", ""), c.itertext())
                )
            )

            if not weekends:
                section = r[0]
                start_time = ""
                end_time = ""

                if len(r) > 1:
                    start_time, end_time = r[1].split("-")
                    start_time = "%s:%s" % (start_time[: 2], start_time[2:])
                    end_time = "%s:%s" % (end_time[: 2], end_time[2:])

                continue

            if not r:
                continue

            classes["title"] = r[0]
            classes["date"]["start_time"] = start_time
            classes["date"]["end_time"] = end_time
            classes["date"]["weekday"] = " MTWRFSH"[weekends]
            classes["date"]["section"] = section

            if len(r) > 1:
                classes["instructors"].append(r[1])

            classes["location"]["building"] = ""
            classes["location"]["room"] = r[2] if len(r) > 2 else ""

            course_table.append(classes)

    return course_table


def score(cont):
    root = etree.HTML(cont)

    try:
        tbody = root.xpath("//table")[-1]

        center = root.xpath("//center")
        center_text = list(center[-1].itertext())[0]
    except:
        tbody = ""
        center = ""
        center_text = ""

    if center_text.startswith(u'目前無學生個人成績資料'):
        return {}

    score_table = []
    for r_index, r in enumerate(tbody[1:-1]):
        r = list(map(lambda x: x.replace(u"\xa0", ""), r.itertext()))

        row = {}

        row["title"] = r[1]
        row["units"] = r[2]
        row["hours"] = r[3]
        row["required"] = r[4]
        row["at"] = r[5]
        row["middle_score"] = r[6]
        row["final_score"] = r[7]
        row["remark"] = r[8]

        score_table.append(row)

    total_score = root.xpath("//div")[-1].text.replace(u"　　　　", " ").split(" ")
    detail = {
        "conduct": float(total_score[0].split("：")[-1]) if not total_score[0].startswith("操行成績：0") else 0.0,
        "average": float(total_score[1].split("：")[-1]) if total_score[1] != "總平均：" else 0.0,
        "class_rank": total_score[2].split("：")[-1] if not total_score[2].startswith("班名次/班人數：/") else "",
        "class_percentage": float(total_score[3].split("：")[-1][:-1]) if not total_score[3].startswith("班名次百分比：%") else 0.0
    }

    return {"scores": score_table, "detail": detail}


parse_function = {"ag222": course, "ag008": score}


if __name__ == "__main__":
    # print(course(open("c.html").read()))
    pass
