import re
import json
import time
import warnings
import datetime
import base64
import unittest
import kuas_api

USERNAME = "1102108133"
PASSWORD = "111"


def ignore_warnings(func):
    def do_test(self, *args, **kwargs):
        with warnings.catch_warnings():
            func(self, *args, **kwargs)
    return do_test


class APITestCase(unittest.TestCase):

    def setUp(self):
        self.app = kuas_api.app.test_client()
        self.username = USERNAME
        self.password = PASSWORD

    def open_with_auth(self, url, method, username, password):
        basic = "Basic %s" % str(
            base64.b64encode(
                bytes(username + ":" + password, "utf-8")), "utf-8")

        return self.app.open(url,
                             method=method,
                             headers={"Authorization": basic}
                             )

    def test_api(self):
        rv = self.app.get("/latest/")
        json_object = json.loads(str(rv.data, "utf-8"))

        # Check version
        assert json_object["version"] == "2"

    @ignore_warnings
    def test_bus_get_timetables(self):
        rv = self.open_with_auth(
            "/latest/bus/timetables?date=2015-09-4",
            "GET",
            self.username,
            self.password)

        json_object = json.loads(str(rv.data, "utf-8"))

        # Check date
        # TODO: date to yyyy-mm-dd
        #   v2/bus.py
        assert "date" in json_object
        assert json_object["date"] == "2015-09-4"

        # Check timetable
        assert "timetable" in json_object
        assert len(json_object["timetable"]) == 4

        # Check bus information
        bus_27037 = {"runDateTime": "2015-09-04 08:20", "limitCount": "999",
                     "reserveCount": "7", "Time": "08:20",
                     "EndEnrollDateTime": "2015-09-03 17:20",
                     "endStation": "燕巢", "isReserve": 0,
                     "busId": "27037", "cancelKey": 0
                     }

        assert json_object["timetable"][0] == bus_27037

    def test_bus_get_put_del_reservations(self):
        tomorrow = datetime.datetime.strftime(
            datetime.date.today() + datetime.timedelta(days=1), "%Y-%m-%d")

        rv = self.open_with_auth(
            "/latest/bus/timetables?date=%s" % (tomorrow),
            "GET",
            self.username,
            self.password)

        json_object = json.loads(str(rv.data, "utf-8"))
        if not json_object["timetable"]:
            print(">>> Warning: Pass testing PUT DELETE for bus resrevations.")
            return False

        # What I want to reseve
        bus_id = json_object["timetable"][-1]["busId"]

        # GET reservations
        rv = self.open_with_auth(
            "/latest/bus/reservations",
            "GET",
            self.username,
            self.password)

        # GET reservations
        json_object = json.loads(str(rv.data, "utf-8"))
        assert "reservation" in json_object

        # PUT reservations
        rv = self.open_with_auth(
            "/latest/bus/reservations/%s" % (bus_id),
            "PUT",
            self.username,
            self.password
        )

        json_object = json.loads(str(rv.data, "utf-8"))

        # Check put reservations
        assert json_object["message"] == "預約成功"

        # Check two put reservations
        rv = self.open_with_auth(
            "/latest/bus/reservations/%s" % (bus_id),
            "PUT",
            self.username,
            self.password
        )

        json_object = json.loads(str(rv.data, "utf-8"))

        # Check has been reserve
        assert json_object["message"] == "該班次已預約,不可重覆預約"

        # Check bus go time
        # go_stamp = re.compile(
        #     "\((.*?)\)").search(json_object['data']['startTime']).group(1)
        # go_date = time.strftime(
        #     "%Y-%m-%d %H:%M", time.localtime(int(go_stamp) / 1000))

        # Check two put reservations
        rv = self.open_with_auth(
            "/latest/bus/reservations/%s" % (bus_id),
            "PUT",
            self.username,
            self.password
        )

        # Get cancel key by timetables
        rv = self.open_with_auth(
            "/latest/bus/timetables?date=%s" % (tomorrow),
            "GET",
            self.username,
            self.password)

        json_object = json.loads(str(rv.data, "utf-8"))

        # Get cancel key
        cancel_key = json_object["timetable"][-1]["cancelKey"]

        # DELETE reservations
        rv = self.open_with_auth(
            "/latest/bus/reservations/%s" % (cancel_key),
            "DELETE",
            self.username,
            self.password
        )

        json_object = json.loads(str(rv.data, "utf-8"))

        # Check bus reserve has been delete
        assert json_object["message"] == "已取消預約紀錄"

        # ERROR: You can't DELETE an non-exist date.
        # Really need to fix for avoid HTTP 500
        # rv = self.open_with_auth(
        #     "/latest/bus/reservations/%s" % (go_date),
        #     "DELETE",
        #     self.username,
        #     self.password
        # )
        # print(rv.data)

        # json_object = json.loads(str(rv.data, "utf-8"))

        # print(json_object)

    def test_notification(self):
        rv = self.app.get("/latest/notifications/1")
        json_object = json.loads(str(rv.data, "utf-8"))

        # Check return content-type
        assert rv.mimetype.startswith("application/json")

        # Check return page
        assert json_object["page"] == 1

        # Check return notification
        assert len(json_object["notification"])

        # Check return notification content
        for c in json_object["notification"]:
            # Check link
            assert "link" in c
            assert c["link"].startswith("http://")

            # Check info
            assert "info" in c
            assert type(c["info"]) == dict
            for key in ["id", "department", "date", "title"]:
                assert key in c["info"]


if __name__ == "__main__":
    unittest.main()
