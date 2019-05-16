APIs
====


Utils 
------

.. autoflask:: web-server:app
    :endpoints: latest.get_auth_token


.. autoflask:: web-server:app
    :endpoints: latest.device_version

.. autoflask:: web-server:app
    :endpoints: latest.servers_status


Bus
----

.. autoflask:: web-server:app
    :endpoints: latest.timetables


.. http:get:: /bus/reservations

    Get user's bus reservations.

    :reqheader Authorization: Using Basic Auth
    :statuscode 200: no error


    **Request**

    .. sourcecode:: http

        GET /latest/bus/reservations HTTP/1.1
        Host: kuas.grd.idv.tw:14769
        Authorization: Basic xxxxxxxxxxxxx=

    .. sourcecode:: shell

        curl -u username:password -X GET https://kuas.grd.idv.tw:14769/v2/bus/reservations


    **Response**

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json


        {
          "reservation":[
            {
              "endTime":"2017-08-06 16:50",
              "end":"燕巢",
              "cancelKey":"1559062",
              "time":"2017-08-07 07:50"
            }
          ]
        }


.. http:put:: /bus/reservations/(int:bus_id)

    Make a reservations for user.

    :reqheader Authorization: Using Basic Auth
    :query int bus_id: Bus identifier
    :statuscode 200: no error


    **Request**

    .. sourcecode:: http

        PUT /latest/bus/reservations/36065 HTTP/1.1
        Host: kuas.grd.idv.tw:14769
        Authorization: Basic xxxxxxxxxxxxx=

    .. sourcecode:: shell

        curl -u username:password -X PUT https://kuas.grd.idv.tw:14769/v2/bus/reservations/36065


    **Response**

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json


        {
          "success":true,
          "code":200,
          "count":0,
          "message":"預約成功",
          "data":{
            "budId":36065,
            "startTime":"/Date(1502355600000)/"
          }
        }


.. http:delete:: /bus/reservations/(int:cancel_key)

    Delete a reservations for user.

    :reqheader Authorization: Using Basic Auth
    :query int cancel_key: Bus cancel key
    :statuscode 200: no error


    **Request**

    .. sourcecode:: http

        DELETE /latest/bus/timetables/1559063 HTTP/1.1
        Host: kuas.grd.idv.tw:14769
        Authorization: Basic xxxxxxxxxxxxx=

    .. sourcecode:: shell

        curl -u username:password -X DELETE https://kuas.grd.idv.tw:14769/v2/bus/reservations/1559063


**Response**

.. sourcecode:: http



Notifications
---------------

.. autoflask:: web-server:app
    :endpoints: latest.notification


AP
---------------

.. autoflask:: web-server:app
    :endpoints: latest.ap_user_info

.. autoflask:: web-server:app
    :endpoints: latest.ap_user_picture

.. autoflask:: web-server:app
    :endpoints: latest.get_coursetables

.. autoflask:: web-server:app
    :endpoints: latest.get_score

.. autoflask:: web-server:app
    :endpoints: latest.ap_semester

Leave
---------------

.. autoflask:: web-server:app
    :endpoints: latest.get_leave

.. autoflask:: web-server:app
    :endpoints: latest.leave_submit

News
---------------

.. autoflask:: web-server:app
    :endpoints: latest.news_all

.. autoflask:: web-server:app
    :endpoints: latest.news


