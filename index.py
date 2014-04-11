import json
import time
import tornado.web
import tornado.websocket
import tornado.ioloop
from config import app_settings, server_config, redis_client, file_name
from func import valid_user

class BaseHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect('/task')

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def write_json(self, code, message, data = ''):
        self.write(json.JSONEncoder().encode({"code":code, "message":message, "data":data}))

class HearbeatHandler(BaseHandler):
    def get(self):
        self.write("don't shoot!your friend!")

class LoginHandler(BaseHandler):
    def get(self):
        self.clear_all_cookies()
        self.render('templates/login.html')

    def post(self):
        if valid_user(self.get_argument('name'), self.get_argument('pass')):
            self.set_secure_cookie("user", self.get_argument("name"))
            self.redirect("/")
        else:
            self.redirect("/login")

class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.set_cookie("_flag", str(time.time()))
        nodes = [eval(node) for node in redis_client.smembers("nodes")]

        self.render('templates/hosts.html', **{
            "ip_address": server_config["ip"],
            "text": "".join(file(file_name)),
            "port": server_config["port"],
            "nodes": nodes,
            "nodes_len": len(nodes),
            "file_name": file_name
        })

class HostsHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        self.set_header("Content-Type","text/json")
        text = self.get_argument("text")
        old_text = "".join(file(file_name))
        if old_text != text:
            with open(file_name, "w+") as f:
                f.write(text)

            user_name = tornado.escape.xhtml_escape(self.current_user)
            SocketHandler.send_to_all(
                json.JSONEncoder().encode({
                    "text":text, 
                    "user": user_name, 
                    "_flag":self.get_cookie("_flag")
                })
            )
            self.write_json(0, "success")
        else:
            self.write_json(1, "not modify")

class SocketHandler(tornado.websocket.WebSocketHandler):
    clients = set()
    def open(self):
        SocketHandler.clients.add(self)
    def on_close(self):
        SocketHandler.clients.remove(self)
    @staticmethod
    def send(message, client):
        client.write_message(message)
    @staticmethod
    def send_to_all(message):
        for c in SocketHandler.clients:
            c.write_message(message)

application = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/edit_hosts', HostsHandler),
    (r'/soc', SocketHandler),
    (r'/login', LoginHandler),
    (r'/heartbeat', HearbeatHandler)
], **app_settings)

if '__main__' == __name__:
    redis_client.sadd("nodes", {"ip": server_config["ip"], "port": server_config["port"]})
    application.listen(server_config["port"])
    tornado.ioloop.IOLoop.instance().start()
