
import requests


HY_SMS_URL = 'https://106.ihuyi.com/webservice/sms.php?method=Submit'
# 查看用户名 登录用户中心->验证码通知短信>产品总览->API接口信息->APIID
account = "C56473882"
# 查看密码 登录用户中心->验证码通知短信>产品总览->API接口信息->APIKEY
password = "eb23889c9d4cbaee41ab4375e8fba4e8"

def send_verfiy_code(phonenum):

    headers = {
        "Content-type": 'application/x-www-form-urlencoded',  # 发送的数据格式
        'Accept': 'text/plain'  # 接收数据的文本格式
    }
    vcode = "您的验证码是：121254。请不要把验证码泄露给其他人。"

    params = {
    'account':'C56473882',
    'password':'eb23889c9d4cbaee41ab4375e8fba4e8',
    'content':vcode,
    'mobile':str(phonenum),
    'format':'json'
    }
    response = requests.post(HY_SMS_URL,headers=headers,data=params)
    print(response.text)
    return response




if __name__ == '__main__':

    a = send_verfiy_code(13694677650)
    print(a)