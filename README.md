AP-API
---
高雄應用科技大學 校務系統 API Server

KUAS AP API Server


How to use?
---
    git clone https://github.com/JohnSounder/AP-API
    python2 web-server.py

And remember to change app.secret_key

    >>>import os
    >>>os.urandom(24)
    b'\xa1I\x1e\xef=|eM<\xa5g%r$Q\x12v^&\x80\x00\x90^$'
    
Copy and change it in web-server.py

    app.secret_key = '\xa1I\x1e\xef=|eM<\xa5g%r$Q\x12v^&\x80\x00\x90^$'
    


Demo
---
http://api.grd.idv.tw:14768/ap/login

http://api.grd.idv.tw:14768/ap/query


TODO LIST
---
 * 查詢缺曠課功能
 * 預定校車
 * 累積學分


Donate
---
[![BitCoin donate
button](http://img.shields.io/bitcoin/donate.png?color=yellow)](https://coinbase.com/checkouts/aa7cf80a2a85b4906cb98fc7b2aad5c5 "Donate
once-off to this project using BitCoin")


