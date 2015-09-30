#-*- coding: utf-8 -*-

import requests
import execjs
import json
import time
import datetime


js_function = """
        function baseEncryption(e) {
        function h(b, a) { var d, c, e, f, g; e = b & 2147483648; f = a & 2147483648; d = b & 1073741824; c = a & 1073741824; g = (b &
1073741823) + (a & 1073741823); return d & c ? g ^ 2147483648 ^ e ^ f : d | c ? g & 1073741824 ? g ^ 3221225472 ^ e ^ f : g ^ 1073741824 ^ e
^ f : g ^ e ^ f } function g(b, a, d, c, e, f, g) { b = h(b, h(h(a & d | ~a & c, e), g)); return h(b << f | b >>> 32 - f, a) } function i(b,
a, d, c, e, f, g) { b = h(b, h(h(a & c | d & ~c, e), g)); return h(b << f | b >>> 32 - f, a) } function j(b, a, c, d, e, f, g) { b = h(b,
h(h(a ^ c ^ d, e), g)); return h(b << f | b >>> 32 - f, a) } function k(b, a, c, d, e, f, g) {
            b = h(b, h(h(c ^
        (a | ~d), e), g)); return h(b << f | b >>> 32 - f, a)
            } function l(b) { var a = "", c = "", d; for (d = 0; 3 >= d; d++) c = b >>> 8 * d & 255, c = "0" + c.toString(16), a +=
c.substr(c.length - 2, 2); return a } var f = [], m, n, o, p, b, a, d, c, f = function (b) { var a, c = b.length; a = c + 8; for (var d = 16
* ((a - a % 64) / 64 + 1), e = Array(d - 1), f = 0, g = 0; g < c;) a = (g - g % 4) / 4, f = 8 * (g % 4), e[a] |= b.charCodeAt(g) << f, g++;
a = (g - g % 4) / 4; e[a] |= 128 << 8 * (g % 4); e[d - 2] = c << 3; e[d - 1] = c >>> 29; return e } (e); b = 1732584193; a = 4023233417; d =
2562383102; c = 271733878; for (e = 0; e < f.length; e += 16) m = b, n = a, o = d, p = c, b = g(b, a, d, c, f[e +
        0], 7, 3614090360), c = g(c, b, a, d, f[e + 1], 12, 3905402710), d = g(d, c, b, a, f[e + 2], 17, 606105819), a = g(a, d, c,
b, f[e + 3], 22, 3250441966), b = g(b, a, d, c, f[e + 4], 7, 4118548399), c = g(c, b, a, d, f[e + 5], 12, 1200080426), d = g(d, c, b, a, f[e
+ 6], 17, 2821735955), a = g(a, d, c, b, f[e + 7], 22, 4249261313), b = g(b, a, d, c, f[e + 8], 7, 1770035416), c = g(c, b, a, d, f[e + 9],
12, 2336552879), d = g(d, c, b, a, f[e + 10], 17, 4294925233), a = g(a, d, c, b, f[e + 11], 22, 2304563134), b = g(b, a, d, c, f[e + 12], 7,
1804603682), c = g(c, b, a, d, f[e + 13], 12, 4254626195), d = g(d, c, b, a, f[e + 14], 17, 2792965006), a = g(a, d,
        c, b, f[e + 15], 22, 1236535329), b = i(b, a, d, c, f[e + 1], 5, 4129170786), c = i(c, b, a, d, f[e + 6], 9, 3225465664), d =
i(d, c, b, a, f[e + 11], 14, 643717713), a = i(a, d, c, b, f[e + 0], 20, 3921069994), b = i(b, a, d, c, f[e + 5], 5, 3593408605), c = i(c, b,
a, d, f[e + 10], 9, 38016083), d = i(d, c, b, a, f[e + 15], 14, 3634488961), a = i(a, d, c, b, f[e + 4], 20, 3889429448), b = i(b, a, d, c,
f[e + 9], 5, 568446438), c = i(c, b, a, d, f[e + 14], 9, 3275163606), d = i(d, c, b, a, f[e + 3], 14, 4107603335), a = i(a, d, c, b, f[e +
8], 20, 1163531501), b = i(b, a, d, c, f[e + 13], 5, 2850285829), c = i(c, b, a, d, f[e + 2], 9, 4243563512), d = i(d,
        c, b, a, f[e + 7], 14, 1735328473), a = i(a, d, c, b, f[e + 12], 20, 2368359562), b = j(b, a, d, c, f[e + 5], 4, 4294588738),
c = j(c, b, a, d, f[e + 8], 11, 2272392833), d = j(d, c, b, a, f[e + 11], 16, 1839030562), a = j(a, d, c, b, f[e + 14], 23, 4259657740), b =
j(b, a, d, c, f[e + 1], 4, 2763975236), c = j(c, b, a, d, f[e + 4], 11, 1272893353), d = j(d, c, b, a, f[e + 7], 16, 4139469664), a = j(a, d,
c, b, f[e + 10], 23, 3200236656), b = j(b, a, d, c, f[e + 13], 4, 681279174), c = j(c, b, a, d, f[e + 0], 11, 3936430074), d = j(d, c, b, a,
f[e + 3], 16, 3572445317), a = j(a, d, c, b, f[e + 6], 23, 76029189), b = j(b, a, d, c, f[e + 9], 4, 3654602809),
        c = j(c, b, a, d, f[e + 12], 11, 3873151461), d = j(d, c, b, a, f[e + 15], 16, 530742520), a = j(a, d, c, b, f[e + 2], 23,
3299628645), b = k(b, a, d, c, f[e + 0], 6, 4096336452), c = k(c, b, a, d, f[e + 7], 10, 1126891415), d = k(d, c, b, a, f[e + 14], 15,
2878612391), a = k(a, d, c, b, f[e + 5], 21, 4237533241), b = k(b, a, d, c, f[e + 12], 6, 1700485571), c = k(c, b, a, d, f[e + 3], 10,
2399980690), d = k(d, c, b, a, f[e + 10], 15, 4293915773), a = k(a, d, c, b, f[e + 1], 21, 2240044497), b = k(b, a, d, c, f[e + 8], 6,
1873313359), c = k(c, b, a, d, f[e + 15], 10, 4264355552), d = k(d, c, b, a, f[e + 6], 15, 2734768916), a = k(a, d, c, b, f[e + 13], 21,
        1309151649), b = k(b, a, d, c, f[e + 4], 6, 4149444226), c = k(c, b, a, d, f[e + 11], 10, 3174756917), d = k(d, c, b, a, f[e
+ 2], 15, 718787259), a = k(a, d, c, b, f[e + 9], 21, 3951481745), b = h(b, m), a = h(a, n), d = h(d, o), c = h(c, p); return (l(b) + l(a) +
l(d) + l(c)).toLowerCase()
        }
        loginEncryption = function (e, h) {
            var g = Math.floor(1163531501 * Math.random()) + 15441, i = Math.floor(1163531502 * Math.random()) + 0, j =
Math.floor(1163531502 * Math.random()) + 0, k = Math.floor(1163531502 * Math.random()) + 0, g = baseEncryption("J" + g), i =
baseEncryption("E" + i), j = baseEncryption("R" + j), k = baseEncryption("Y" + k), e = baseEncryption(e + encA1(g)), h = baseEncryption(e + h
+ "JERRY" + encA1(i)), l = baseEncryption(e + h + "KUAS" + encA1(j)), l = baseEncryption(l + e + encA1("ITALAB") + encA1(k)), l =
baseEncryption(l + h + "MIS" + k); return '{ a:"' + l + '",b:"' +
        g + '",c:"' + i + '",d:"' + j + '",e:"' + k + '",f:"' + h + '" }'
        }; function encA2(e) { return baseEncryption(e) };
        function encA1(e) {var r = e;r = encA2(e+ '77460');r = encA2('78398' + e);r = encA2(e+ '9F0E75318F99D12A92FB1F4BA3507B7B');r
= encA2(e+ '8991');return r;};
        function gets(password){
            return loginEncryption(password , new Date().getTime());
        }
        function getTime(){
            return new Date().getTime();
        }
        """


headers = {"User-Agnet":
           "Mozilla/5.0 (X11; Linux x86_64; rv:30.0) Gecko/20100101 Firefox/35.0"}


# Bus url setting
BUS_URL = "http://bus.kuas.edu.tw"
BUS_SCRIPT_URL = "http://bus.kuas.edu.tw/API/Scripts/a1"
BUS_API_URL = "http://bus.kuas.edu.tw/API/"
BUS_LOGIN_URL = BUS_API_URL + "Users/login"
BUS_FREQ_URL = BUS_API_URL + "Frequencys/getAll"
BUS_RESERVE_URL = BUS_API_URL + "Reserves/getOwn"
BUS_BOOK_URL = BUS_API_URL + "Reserves/add"
BUS_UNBOOK_URL = BUS_API_URL + "Reserves/remove"

# Bus timeout setting
BUS_TIMEOUT = 1.0


def _get_real_time(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp) / 10000000 - 62135596800).strftime("%Y-%m-%d %H:%M")


def status():
    """Return Bus server status code

    :rtype: int
    :returns: A HTTP status code

    >>> status()
    200
    """

    try:
        bus_status_code = requests.head(
            BUS_URL, timeout=BUS_TIMEOUT).status_code
    except requests.exceptions.Timeout:
        bus_status_code = 408

    return bus_status_code


def init(session):
    session.head(BUS_URL)
    script_content = session.get(BUS_SCRIPT_URL, headers=headers).text

    js = execjs.compile(js_function + script_content)

    return js


def login(session, username, password):
    """Login to KUAS Bus system.

    :param session: requests session object
    :type session: class requests.sessions.Session
    :param username: username of kuas bus system, actually your kuas student id
    :type username: str or int
    :param password: password of kuas ap system.
    :type password: str or int

    :return: login status
    :rtype: bool
    """

    data = {'account': username, 'password': password}

    try:
        js = init(session)
        data['n'] = js.call('loginEncryption', str(username), str(password))
    except:
        return False

    content = session.post(BUS_LOGIN_URL,
                           data=data,
                           headers=headers,
                           timeout=BUS_TIMEOUT
                           ).text

    resp = json.loads(content)

    return resp['success']


def query(session, y, m, d, operation="全部"):
    """
    Query kuas bus timetable

    :param session: requests session object
    :type session: class requests.sessions.Session
    :param y: year, using common era
    :type y: int
    :param m: month
    :type m: int
    :param d: day
    :type d: int
    :param operation: choosing bus start from yanchao or jiangong, or all.
    :type operation: str

    >>> s = requests.Session()
    >>> login(s, "1102108133", "111")
    True

    >>> type(query(s, "2015", "6", "15"))
    <class 'list'>

    >>> type(query(s, *'2014-10-08'.split("-")))
    <class 'list'>

    """
    data = {
        'data': '{"y": "%s","m": "%s","d": "%s"}' % (y, m, d),
        'operation': operation,
        'page': 1,
        'start': 0,
        'limit': 90
    }

    resp = session.post(BUS_FREQ_URL, data=data, headers=headers)

    resource = json.loads(resp.text)
    returnData = []

    if not resource['data']:
        return []

    for i in resource['data']:
        Data = {}
        Data['EndEnrollDateTime'] = _get_real_time(i['EndEnrollDateTime'])
        Data['runDateTime'] = _get_real_time(i['runDateTime'])
        Data['Time'] = Data['runDateTime'][-5:]
        Data['endStation'] = i['endStation']
        Data['busId'] = i['busId']
        Data['reserveCount'] = i['reserveCount']
        Data['limitCount'] = i['limitCount']
        Data['isReserve'] = int(i['isReserve']) + 1
        returnData.append(Data)

    return returnData


def reserve(session):
    """Query user reserve bus.
    """

    data = {
        'page': 1,
        'start': 0,
        'limit': 90
    }

    content = session.post(BUS_RESERVE_URL, data=data, headers=headers).text

    resource = json.loads(content)

    rd = []
    for i in resource['data']:
        data = {}
        data['time'] = _get_real_time(i['time'])
        data['endTime'] = _get_real_time(i['endTime'])
        data['cancelKey'] = i['key']
        data['end'] = i['end']
        rd.append(data)

    result = sorted(rd, key=lambda k: k['time'])

    return result


def book(session, kid, action=None):
    if not action:
        res = session.post(BUS_BOOK_URL,
                           data="{busId: %s}" % (kid),
                           headers=headers,
                           )
    else:
        # Then compare users reserve bus,
        # if kid is same as time, then found the correct bus,
        # then we can unbook this bus.

        res = session.post(BUS_UNBOOK_URL,
                           data="{reserveId: %d}" % (kid) + "}",
                           headers=headers,
                           )

    resource = json.loads(str(res.content, "utf-8"))

    return resource


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    exit()

    session = requests.session()
    init(session)
    login(session, '1102108133', '111')

    t = time.time()
    print(query(session, *'2014-10-08'.split("-")))
    print(time.time() - t)
    exit()
    #book(session, '22868', '')

    print("---------------------")
    print(reserve(session))
    book(session, '741583', 'un')
    print(reserve(session))
    """
    result = query('2014', '6', '27')
    for i in result:
        if book(i['busId']) :
            print "Book Success"
    result = reserve()
    for i in result:
        if book(i['key'], "Un") :
            print "UnBook Success"
    """
