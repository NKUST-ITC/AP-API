# coding=utf-8
from japronto import Application

if __name__ == "__main__":
    app = Application(debug=True)
    router = app.router

    app.run()
