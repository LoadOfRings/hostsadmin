import urllib2
import socket
socket.setdefaulttimeout(5)

from config import redis_client

for _node in redis_client.smembers("nodes"):
    node = eval(_node)
    url = "http://%s:%d/heartbeat" % (node['ip'], node['port'])
    try:
        content = urllib2.urlopen(url).read()
        if content != "don't shoot!your friend!":
            redis_client.srem("nodes", _node)
    except:
        redis_client.srem("nodes", _node)



