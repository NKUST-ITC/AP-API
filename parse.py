# -*- coding: utf-8 -*-

from lxml import etree


def course(cont):
    root = etree.HTML(cont)

    tbody = root.xpath("//table")[-1]


    course_table = {}
    for r_index, r in enumerate(tbody[1:]):
        row = {}
        for index, c in enumerate(r.xpath("td")):
            r = list(filter(lambda x: x != u"\xa0", c.itertext()))
            
            if index == 0:
                row['time'] = r[0]
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

        # Check if over 8th didn't have class
        for i in row:
            if r_index < 10 or i != "time" and row[i]["course_name"]:
                course_table[r_index] = row
                break

    # Check Saturday and Sunday class
    have_saturday = False
    have_sunday = False
    for r in course_table:
        if not isinstance(course_table[r], bool) and course_table[r][6]["course_name"]:
            have_saturday = True
        if not isinstance(course_table[r], bool) and course_table[r][7]["course_name"]:
            have_sunday = True


    return [course_table, have_saturday, have_sunday]
      

def score(cont):
    root = etree.HTML(cont)

    tbody = root.xpath("//table")[-1]


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

    return [score_table]

if __name__ == "__main__":
    course(open("course.html").read())