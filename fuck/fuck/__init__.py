# 项目中第一个加载文件
import pymysql
pymysql.install_as_MySQLdb()

from lib.orm import patch_model
patch_model()