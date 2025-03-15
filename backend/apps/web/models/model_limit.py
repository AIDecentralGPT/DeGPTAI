from peewee import Model, CharField, IntegerField, BigIntegerField # 导入Peewee中的Model、CharField和DateTimeField
from apps.web.internal.db import DB  # 导入数据库实例DB
from pydantic import BaseModel  # 导入Pydantic中的BaseModel
from typing import Optional, List  # 导入类型提示
from playhouse.shortcuts import model_to_dict  # 导入Peewee中的model_to_dict方法

# 定义ModelLimit模型
class ModelLimit(Model):
    model = CharField(primary_key=True, unique=True)  # 模型名称
    normal = IntegerField()  # 访客用户次数
    wallet = IntegerField() # 钱包用户次数
    kyc = IntegerField() # KYC用户次数
    vip = IntegerField()  # VIP用户次数
    created_at = BigIntegerField()  # 定义默认值为当前时间的日期时间字段created_at

    class Meta:
        database = DB  # 指定数据库
        table_name = 'model_limit'  # 指定表名

# 定义Pydantic模型EmailCodeModel
class ModelLimitModel(BaseModel):
    model: str  # 模型名称
    normal: int  # 访客用户次数
    wallet: int # 钱包用户次数
    kyc: int # KYC用户次数
    vip: int  # VIP用户次数
    created_at: int  # 定义created_at字段，类型为日期时间

# 定义ModelLimitTable类
class ModelLimitTable:
    def __init__(self, db):
        self.db = db  # 初始化数据库实例
        self.db.create_tables([ModelLimit])  # 创建EmailCodeTable表

    def get_info_by_model(self, model: str) -> Optional[ModelLimitModel]:
        try:
            modellimit = ModelLimit.get_or_none(ModelLimit.model == model)
            if modellimit is None:
                return None
            else:
                modellimit_dict = model_to_dict(modellimit)  # 将数据库对象转换为字典
                modellimit_model = ModelLimitModel(**modellimit_dict)  # 将字典转换为Pydantic模型
                return modellimit_model
        except Exception as e:
            print("========================", e)
            return None
        
    def get_info_by_models(self, models: list) -> Optional[List[ModelLimitModel]]:
        try:
            modellimits = ModelLimit.select().where(ModelLimit.model.in_(models))
            # 将数据库对象转换为字典
            modellimit_list = [ModelLimitModel(**model_to_dict(modellimit)) for modellimit in modellimits]
            return modellimit_list  
        except Exception as e:
            print("========================", e)
            return None
        
    def get_all(self) -> Optional[List[ModelLimitModel]]:
        try:
            modellimits = ModelLimit.select()
            modellimit_list = [ModelLimitModel(**model_to_dict(modellimit)) for modellimit in modellimits] 
            return modellimit_list
        except Exception as e:
            print("========================", e)
            return None


# 实例化ModelLimitTable类
ModelLimitInstance = ModelLimitTable(DB)

