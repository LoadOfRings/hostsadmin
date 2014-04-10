import os
import socket
import fcntl
import struct
import redis

def get_ip(ifname):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl( s.fileno(), 0x8915, struct.pack('256s',ifname[:15]))[20:24])
    except:
        localIP = socket.gethostbyname(socket.gethostname())
        ipList = socket.gethostbyname_ex(socket.gethostname())
        for i in ipList:
            if i != localIP and type(i) is type([]) and len(i):
                return "".join(i)
        return localIP

app_settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
    "debug":True
}
server_config = {
    "ip": get_ip("eth0"),
    "port": 8000
}
redis_config = {
    "host": "10.210.230.30",
    "port": 6379,
    "db": 4,
}
file_name = r"/etc/hosts"

redis_client = redis.Redis(
                host=redis_config['host'],
                port=redis_config['port'],
                db=redis_config['db']
            )
