# -*- coding: utf-8 -*-

from lxml import etree


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

    course_table = {}
    for r_index, r in enumerate(tbody[1:]):
        row = {}
        for index, c in enumerate(r.xpath("td")):
            r = list(filter(lambda x: x != u"\xa0", c.itertext()))
            
            if index == 0:
                row['time'] = r[0].replace(" ", "")
            else:
                row[index] = {
                        "course_name": "",
                        "course_teacher": "",
                        "course_classroom": ""
                    }

                if r:
                    while len(r) < 3:
                        r.append("")

                    row[index]["course_name_simple"] = r[0][:2]
                    row[index]["course_name"] = r[0]
                    row[index]["course_teacher"] = r[1]
                    row[index]["course_classroom"] = r[2]

        course_table[r_index] = row


    # Check if over 8th didn't have class
    token_b = False
    token_night = False


    for r in course_table:
        for c in course_table[r]:
            if r > 9 and c != "time" and course_table[r][c]['course_name']:
                if r == 10:
                    token_b = True
                else:
                    #print(course_table[r][c]['course_name'])
                    token_night = True

    #print(token_b, token_night)


    if token_night: 
        pass
    elif token_b:
        for i in [11, 12, 13, 14]:
            del course_table[i]
    else:
        for i in [10, 11, 12, 13, 14]:
            del course_table[i]

        

    # Check Saturday and Sunday class
    have_saturday = False
    have_sunday = False
    
    for r in course_table:
        if not isinstance(course_table[r], bool) and course_table[r][6]["course_name"]:
            have_saturday = True
        if not isinstance(course_table[r], bool) and course_table[r][7]["course_name"]:
            have_sunday = True


    return [course_table, have_saturday, have_sunday, False]
      

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
    #print(course(open("c.html").read()))
    pass
