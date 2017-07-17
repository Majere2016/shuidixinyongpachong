import requests, mimetypes, urllib.parse, json, time

class YDMHttp:

    apiurl = 'http://api.yundama.com/api.php'
    
    username = ''
    password = ''
    appid = ''
    appkey = ''

    def __init__(self, username, password, appid, appkey):
        self.username = username  
        self.password = password
        self.appid = str(appid)
        self.appkey = appkey

    # 向接口发请求
    def request(self, fields, files=[]):
        try:
            response = post_url(self.apiurl, fields, files)
            response = json.loads(response)
        except Exception as e:
            response = None
        return response

    # 查询账户余额
    def balance(self):
        data = {'method': 'balance', 'username': self.username, 'password': self.password, 'appid': self.appid, 'appkey': self.appkey}
        response = self.request(data)
        if (response):
            if (response['ret'] and response['ret'] < 0):
                return response['ret']
            else:
                return response['balance']
        else:
            return -9001
    # 登录账户
    def login(self):
        data = {'method': 'login', 'username': self.username, 'password': self.password, 'appid': self.appid, 'appkey': self.appkey}
        response = self.request(data)
        if (response):
            if (response['ret'] and response['ret'] < 0):
                return response['ret']
            else:
                return response['uid']
        else:
            return -9001
    # 上传验证码图片
    def upload(self, filename, codetype, timeout):
        data = {'method': 'upload', 'username': self.username, 'password': self.password, 'appid': self.appid, 'appkey': self.appkey, 'codetype': str(codetype), 'timeout': str(timeout)}
        file = {'file': open(filename,'rb')}

        response = requests.post(self.apiurl,data=data,files=file).text
        response = json.loads(response)
        if (response):
            if (int(response['ret']) and int(response['ret']) < 0):
                return response['ret']
            else:
                return response['cid']
        else:
            return -9001

    # 根据cid查询打码结果
    def result(self, cid):
        data = {'method': 'result', 'username': self.username, 'password': self.password, 'appid': self.appid, 'appkey': self.appkey, 'cid': str(cid)}
        response = self.request(data)
        return response and response['text'] or ''
    # 打码过程
    def decode(self, filename, codetype, timeout):
        cid = self.upload(filename, codetype, timeout)
        if (cid > 0):
            for i in range(0, timeout):
                result = self.result(cid)
                if (result != ''):
                    return cid, result
                else:
                    time.sleep(1)
            return -3003, ''
        else:
            return cid, ''

######################################################################

def post_url(url, fields, files=[]):
    urlparts = urllib.parse.urlsplit(url)  # 切分url
    return post_multipart(urlparts[1], urlparts[2], fields, files)
#
def post_multipart(host, selector, fields, files):
    content_type, body = encode_multipart_formdata(fields, files)
    headers = {
        'Host': host,
        'Content-Type': content_type,
        'Content-Length': str(len(body))
    }
    url = 'http://'+host+selector
    res = requests.post(url,headers=headers,data=body)
    return res.text

def encode_multipart_formdata(fields, files=[]):
    BOUNDARY = 'WebKitFormBoundaryJKrptX8yPbuAJLBQ'
    CRLF = '\r\n' 
    L = [] 
    for field in fields:
        key = field
        value = fields[key]
        L.append('--' + BOUNDARY) 
        L.append('Content-Disposition: form-data; name="%s"' % key) 
        L.append('') 
        L.append(value) 
    for field in files:
        key = field
        filepath = files[key]
        L.append('--' + BOUNDARY) 
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filepath))
        L.append('Content-Type: %s' % get_content_type(filepath)) 
        L.append('')
        L.append(open(filepath, 'rb').read())
    L.append('--' + BOUNDARY + '--') 
    L.append('') 
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY 
    return content_type, body 

def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

######################################################################
def main(imgname):
    # 用户名
    username    = 'panshi001'

    # 密码
    password    = 'panshi123456'

    # 软件ＩＤ，开发者分成必要参数。登录开发者后台【我的软件】获得！
    appid       = 1

    # 软件密钥，开发者分成必要参数。登录开发者后台【我的软件】获得！
    appkey      = '22cc5376925e9387a23cf797cb9ba745'

    # 图片文件
    filename    = imgname

    # 验证码类型，# 例：1004表示4位字母数字，不同类型收费不同。请准确填写，否则影响识别率。在此查询所有类型 http://www.yundama.com/price.html
    codetype    = 1004

    # 超时时间，秒
    timeout     = 60

    # 检查
    if (username == 'username'):
        print ('请设置好相关参数再测试')
    else:
        # 初始化
        yundama = YDMHttp(username, password, appid, appkey)

        # 登陆云打码
        uid = yundama.login()
        print ('uid: %s' % uid)

        # 查询余额
        balance = yundama.balance()
        print ('balance: %s' % balance)

        # 开始识别，图片路径，验证码类型ID，超时时间（秒），识别结果
        cid, result = yundama.decode(filename, codetype, timeout)
        print ('cid: %s, result: %s' % (cid, result))

######################################################################
