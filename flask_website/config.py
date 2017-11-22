import os
class Config(object):
    DEBUG = True
    BASEDIR = os.path.abspath(os.path.dirname(__file__))

    HOST = '0.0.0.0'
    PORT = '8000'
    ALIYUN_API_FORMAT = "JSON"
    # 阿里云的access key id
    ALIYUN_API_KEY = "LTAIp5j2DxU47O42"
    # 阿里云的access secret
    ALIYUN_API_SECRET = "EY9OdjeinAnEOeDyFNZb2OiT3Xg4ep"
    # 区域,可选
    ALIYUN_API_REGION_ID = ""

    ALISMS_GATEWAY = "https://sms.aliyuncs.com/"
    ALISMS_SIGN = "富春江app"
    ALISMS_TPL_REGISTER = "SMS_5250008"


class Development(Config):  # inherit from Config
    pass


class Production(Config):
    DEBUG = False
    HOST = '127.0.0.1'
    PORT = 14000