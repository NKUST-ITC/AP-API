[![Build Status](https://travis-ci.org/kuastw/AP-API.svg?branch=master)](https://travis-ci.org/kuastw/AP-API)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)

NKUST - API
==========

高雄科技大學 API Server NKUST API Server
---------------------------
Requirement
---
- Ubuntu (18.04 or previous version)
- Python 3.6
- Redis server
- NodeJS (if host by python venv)

How to use?
---
### Clone project
```
$ git clone https://github.com/NKUST-ITC/AP-API
$ cd AP-API
```
By python venv
---
```
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ redis-server &
$ python src/web-server.py
```
By docker  
---
Requirement
* Redis instance running on localhost

Need to add environment variable **-e  REDIS_URL=redis://127.0.0.1:6379/0**

or by export

```
$ export REDIS_URL=redis://127.0.0.1:6379/0
```

And let docker run host network need add  **--network="host"**

Otherwise redis config by docker network(see docker-compose.yml config)

Arguments **gunicorn_cfg.py web-server:app** is production flask uWSGI
```
$ sudo docker run --network="host" nkustitc/ap-api:latest gunicorn -c gunicorn_cfg.py web-server:app
```
or replace by **python3 web-server.py**
```
$ sudo docker run --network="host" nkustitc/ap-api:latest python3 web-server.py
```
By docker-compose
---
Copy .env example
- CADDY_HOST_HTTPS_PORT -> caddy https host port
- REDIS_URL -> python request redis url
```
$ cp env.example .env
```
Copy caddy host config example
```
$ cd caddy
$ cp Caddyfile.example Caddyfile
```
Edit **Caddyfile**'s host config**(Production)**
- line 1 **0.0.0.0:2087** replace by you want host domain and port
```
0.0.0.0:2087 {
	proxy / https://web:14769 {
		transparent
		insecure_skip_verify
	}
	gzip
	tls example@gmail.com
}
```
start docker-compose (if need re download package, can add **--build** build by Dockerfile)
```
$ sudo docker-compose up
```
---
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


