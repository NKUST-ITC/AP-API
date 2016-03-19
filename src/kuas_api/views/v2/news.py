# -*- coding: utf-8 -*-

import random
import json

from flask import redirect

import kuas_api.kuas.cache as cache


from kuas_api import admin, app
from kuas_api import news_db as db
from flask_admin.contrib import sqla


DEFAULT_WEIGHT = 1
ENABLE = 1
NEWS_ID = 0

# Nestable blueprints problem
# not sure isn't this a best practice now.
# https://github.com/mitsuhiko/flask/issues/593
#from kuas_api.views.v2 import api_v2
routes = []


def route(rule, **options):
    def decorator(f):
        url_rule = {
            "rule": rule,
            "view_func": f,
            "options": options if options else {}
        }

        routes.append(url_rule)
        return f

    return decorator


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(100))
    link = db.Column(db.Text())
    image = db.Column(db.Text())
    weight = db.Column(db.Integer())

    # Required for administrative interface. For python 3 please use __str__
    # instead.
    def __str__(self):
        return self.username


class NewsInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    key = db.Column(db.String(64), nullable=False)
    value = db.Column(db.String(64))

    news_id = db.Column(db.Integer(), db.ForeignKey(News.id))
    news = db.relationship(News, backref='info')

    def __str__(self):
        return '%s - %s' % (self.key, self.value)


class NewsAdmin(sqla.ModelView):
    inline_models = (NewsInfo,)


admin.add_view(NewsAdmin(News, db.session))


def build_news_db():
    db.drop_all()
    db.create_all()

    # Create sample Users
    news_list = [
        {
            "news_title": "第八屆泰北團-夢想，「泰」不一樣",
            "news_image": "http://i.imgur.com/iNbbd4B.jpg",
            "news_url": "https://docs.google.com/forms/d/11Awcel_MfPeiEkl7zQ0MldvnAw59gXKLecbIODPOaMs/viewform?edit_requested=true",
            "news_content": "",
            "news_weight": 3
        },
        {
            "news_title": "體委幹部體驗營",
            "news_image": "http://i.imgur.com/aJyQlJp.jpg",
            "news_url": "https://www.facebook.com/Kuas%E9%AB%94%E5%A7%94-440439566106678/?fref=ts",
            "news_content": "",
            "news_weight": 4
        },
        {
            "news_title": "遊戲外掛 原理實戰",
            "news_image": "http://i.imgur.com/WkI23R2.jpg",
            "news_url": "https://www.facebook.com/profile.php?id=735951703168873",
            "news_content": "",
            "news_weight": 6
        },
        {
            "news_title": "好日子育樂營",
            "news_image": "https://scontent-hkg3-1.xx.fbcdn.net/hphotos-xft1/v/t34.0-0/p206x206/12834566_977348362345349_121675822_n.jpg?oh=e04f6830fdfe5d3a77e05a8b3c32fefc&oe=56E663E6",
            "news_url": "https://m.facebook.com/kuasYGR/",
            "news_content": "",
            "news_weight": 6
        }
    ]

    for i in range(len(news_list)):
        user = News()
        user.title = news_list[i]['news_title']
        user.image = news_list[i]['news_image']
        user.link = news_list[i]['news_url']
        user.weight = news_list[i]['news_weight']
        user.content = news_list[i]['news_content']
        db.session.add(user)

    db.session.commit()

    return


def check_db():
    import os

    app_dir = os.path.realpath(os.path.driname(__file__))
    database_path = os.path.join(app_dir, app.config["DATABASE_FILE"])

    if not os.path.exists(database_path):
        build_news_db()


def random_by_weight(p):
    choice_id = []
    for i in range(len(p)):
        choice_id += [i for _ in range(DEFAULT_WEIGHT + p[i]["news_weight"])]

    return p[random.choice(choice_id)]


def random_news():
    news_list = []

    for i in News.query.all():
        news_list.append({
            "news_title": i.title,
            "news_weight": i.weight,
            "news_image": i.image,
            "news_url": i.link,
            "news_content": i.content
        })

    return random_by_weight(news_list)


@route('/news')
def news():
    """
    News for kuas.

    return [enable, news_id, news_title, news_template, news_url]
        enable: bool
        news_id: int
        news_title: string
        news_tempalte: string
        news_url: string
    """

    # Get news from random news
    news = random_news()

    news_title = news["news_title"]
    news_template = (
        "<div style='text-align:center;'>"
        "<div><img style='display:block;margin-left:auto;margin-right:auto;max-width:80%;min-height:150px;height:auto;' src='"
        + news["news_image"] + "'></img>" + news["news_content"] + "</div>" +
        "</div>"

    )

    news_url = news["news_url"]

    return json.dumps([ENABLE, NEWS_ID, news_title, news_template, news_url])


# @route('/news/admin/build')
# def build_admin_db():
#     build_news_db()

#     return redirect("/admin")


if __name__ == "__main__":
    build_news_db()
