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
        return [[], False, False, center_text]

    tbody = root.xpath("//table")[-1]

    course_table = []
    for sections, r in enumerate(tbody[1:]):
        section = ""
        start_time = ""
        end_time = ""

        for weekends, c in enumerate(r.xpath("td")):
            classes = {"title": "", "date": {}, "location": {}, "instructors": []}

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

                continue

            if not r:
                continue

            classes["title"] = r[0]
            classes["date"]["start_time"] = start_time
            classes["date"]["end_time"] = end_time
            classes["date"]["weekday"] = " MTWRFSH"[weekends]
            classes["date"]["section"] = section

            classes["location"]["building"] = ""
            classes["location"]["room"] = r[2] if len(r) > 2 else ""

            classes["instructors"].append(r[1])

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
        return [[], [], center_text]

    score_table = []
    for r_index, r in enumerate(tbody[1:-1]):
        r = list(map(lambda x: x.replace(u"\xa0", ""), r.itertext()))

        row = {}

        row["course_name"] = r[1]
        row["credit"] = r[2]
        row["time"] = r[3]
        row["required"] = r[4]
        row["at"] = r[5]
        row["middle_score"] = r[6]
        row["final_score"] = r[7]
        row["remark"] = r[8]

        score_table.append(row)

    total_score = root.xpath("//div")[-1].text.replace(u"　　　　", " ").split(" ")

    return [score_table, total_score, False]


parse_function = {"ag222": course, "ag008": score}


if __name__ == "__main__":
    # print(course(open("c.html").read()))
    pass
