from peewee import Model, CharField, IntegerField, BigIntegerField # 导入Peewee中的Model、CharField和DateTimeField
from apps.web.internal.db import DB  # 导入数据库实例DB
from pydantic import BaseModel  # 导入Pydantic中的BaseModel
from typing import Optional, List  # 导入类型提示
from playhouse.shortcuts import model_to_dict  # 导入Peewee中的model_to_dict方法

# 定义AppVersion模型
class AppVersion(Model):
    id = IntegerField(primary_key=True, unique=True) #主键
    versionCode = IntegerField()  # 版本号
    versionName = CharField()  # 版本名称
    desc = CharField()  # 版本描述
    open = IntegerField()  # 是否开启
    url = CharField() #下载地址
    created_at = BigIntegerField()  # 定义默认值为当前时间的日期时间字段created_at

    class Meta:
        database = DB  # 指定数据库
        table_name = 'app_version'  # 指定表名

# 定义Pydantic模型AppVersionModel
class AppVersionModel(BaseModel):
    versionCode: int  # 版本号
    versionName: str  # 版本名称
    desc: str  # 版本描述
    open: int  # 是否开启
    url: str #下载地址
    created_at: int  # 定义created_at字段，类型为日期时间

# 定义AppVersionTable类
class AppVersionTable:
    def __init__(self, db):
        self.db = db  # 初始化数据库实例
        self.db.create_tables([AppVersion])  # 创建Models表

    def get_app_version(self) -> Optional[AppVersionModel]:
        try:
            appversion = AppVersion.get_or_none(AppVersion.open == 1)
            if appversion is None:
                return None
            else:
                return AppVersionModel(**model_to_dict(appversion))
        except Exception as e:
            print("=============get_info_by_model error===========", e)
            return None


# 实例化AppVersionTable类
AppVersionInstance = AppVersionTable(DB)

