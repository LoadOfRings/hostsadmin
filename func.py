import socket
import urllib
import urllib2
import json

def get_ip():
    localIP = socket.gethostbyname(socket.gethostname())
    ipList = socket.gethostbyname_ex(socket.gethostname())
    for i in ipList:
        if i != localIP and type(i) is type([]) and len(i):
            return "".join(i)
    return localIP

def valid_user(username, password, login_url="http://10.75.14.217:8322/sina_auth_ad.php"):
    params = urllib.urlencode({
            'login':username,
            'pwd':password
        })
    request = urllib2.Request(login_url, params)
    try:
        response = urllib2.urlopen(request).read()
        status = json.JSONDecoder().decode(response)['status_ok']
        if status == True:
            return True
        else:
            return False
    except:
        return False
