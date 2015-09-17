# DEBUGGING
reload = True

# Bind IP
bind = "0.0.0.0:14769"

# SSL
#certfile = "/etc/nginx/conf/certs/domain.crt"
#keyfile = "/etc/nginx/conf/certs/domain.key"

# Performance
workers = 3
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 5

# Logger
accesslog = "-"
access_logformat = "[api.v2] %(h)s %(l)s %(u)s %(t)s .%(r)s. %(s)s %(b)s .%(f)s. .%(a)s. conn=\"%({Connection}i)s\""

