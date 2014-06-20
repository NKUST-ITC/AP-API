# -*- coding: utf-8 -*-

from lxml import etree


def course(cont):
    root = etree.HTML(cont)

    tbody = root.xpath("//table/tbody")[-1]


    course_table = []
    for r in tbody[1:]:
        row = []
        for index, c in enumerate(r.xpath("td")):
            row.append(list(filter(lambda x: x != "\xa0", c.itertext())))

        course_table.append(row)

    return course_table
      



if __name__ == "__main__":
    course(open("course.html").read())