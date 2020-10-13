
"""第三方配置"""

# 互亿无线短信验证平台配置
HY_SMS_URL = 'https://106.ihuyi.com/webservice/sms.php?method=Submit'
HY_SMS_PARAMS = {
    'account':'C56473882',
    'password':'eb23889c9d4cbaee41ab4375e8fba4e8',
    'content':'您的验证码是：%d。请不要把验证码泄露给其他人。',  # 大忌：一定要符合content魔板内容，否则发送失败
    'mobile':None,
    'format':'json'
}


# 七牛云平台配置
QN_ACCESS_KEY = 'nzxbLvH0Xh-e9XfQqBj6FyGUcQ1H7T7cmPS94VS1'
QN_SECRET_KEY = 'GOZ6qu-0TEVo2H22_PAreTi71EkVoIaCB0gjMZxB'
QN_BASE_URL = 'qesc2g848.bkt.clouddn.com'
QN_BUCKET = 'luciano'
