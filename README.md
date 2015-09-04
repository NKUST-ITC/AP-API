KUAS - API
==========

高雄應用科技大學 API Server
KUAS API Server
---------------------------

How to use?
---
```
$ git clone https://github.com/JohnSounder/AP-API
$ pip install -r requirement.txt
$ cd AP-API
$ python src/web-server.py
```


Fixed APIBlueprint
---
You must fixed manually about flask_apiblueprint

```
site-packages/flask_apiblueprint/flask_apiblueprint.py
```
Change .iteritems() to .items() in two place
   



Demo
---
https://kuas.grd.idv.tw:14769/v2/token



Donate
---
[![BitCoin donate
button](http://img.shields.io/bitcoin/donate.png?color=yellow)](https://coinbase.com/checkouts/aa7cf80a2a85b4906cb98fc7b2aad5c5 "Donate
once-off to this project using BitCoin")


