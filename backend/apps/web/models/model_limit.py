<<<<<<< HEAD
from peewee import Model, CharField, IntegerField, BigIntegerField
from apps.web.internal.db import DB
from pydantic import BaseModel
from typing import Optional, List
from playhouse.shortcuts import model_to_dict

# Define ModelLimit model
class ModelLimit(Model):
    model = CharField(primary_key=True, unique=True)  # Model name
    normal = IntegerField()  # Number of visitor users
    wallet = IntegerField() # Wallet users
    vip = IntegerField()  # Number of VIP users
    created_at = BigIntegerField()  # Define the default value as the current time for the date time field 'creatd_at'

    class Meta:
        database = DB  # Specify Database
        table_name = 'model_limit'  # Specify table name

# Define ModelLimitTable
class ModelLimitModel(BaseModel):
    model: str  # Model name
    normal: int  # Number of visitor users
    wallet: int # Wallet users
    vip: int  # Number of VIP users
    created_at: int  # Define the 'creatd_at' field with a date and time type

# Define ModelLimitTable class
class ModelLimitTable:
    def __init__(self, db):
        self.db = db  # Initialize database instance
        self.db.create_tables([ModelLimit])  # Create EmailCodeTable table

    def get_info_by_model(self, model: str) -> Optional[ModelLimitModel]:
        try:
            modellimit = ModelLimit.get_or_none(ModelLimit.model == model)
            if modellimit is None:
                return None
            else:
                modellimit_dict = model_to_dict(modellimit)  # Convert database objects to dictionaries
                modellimit_model = ModelLimitModel(**modellimit_dict)  # Convert dictionary to Pydantic model
                return modellimit_model
        except Exception as e:
            print("========================", e)
            return None
        
    def get_info_by_models(self, models: list) -> Optional[List[ModelLimitModel]]:
        try:
            modellimits = ModelLimit.select().where(ModelLimit.model.in_(models))
            # Convert database objects to dictionaries
            modellimit_list = [ModelLimitModel(**model_to_dict(modellimit)) for modellimit in modellimits]
            return modellimit_list  
        except Exception as e:
            print("========================", e)
=======
from peewee import Model, CharField, IntegerField, BigIntegerField # 导入Peewee中的Model、CharField和DateTimeField
from apps.web.internal.db import DB  # 导入数据库实例DB
from pydantic import BaseModel  # 导入Pydantic中的BaseModel
from typing import Optional, List  # 导入类型提示
from playhouse.shortcuts import model_to_dict  # 导入Peewee中的model_to_dict方法

# 定义ModelLimit模型
class ModelLimit(Model):
    id = IntegerField(primary_key=True, unique=True)  # 主键
    user_tier = CharField()  # 用户类型
    model_type = CharField() # 模型类型
    vip = CharField() # VIP类型
    limits = IntegerField()  # 访问次数
    created_at = BigIntegerField()  # 定义默认值为当前时间的日期时间字段created_at

    class Meta:
        database = DB  # 指定数据库
        table_name = 'model_limit'  # 指定表名

# 定义Pydantic模型EmailCodeModel
class ModelLimitModel(BaseModel):
    id: int  # 主键
    user_tier: str  # 用户类型
    model_type: str # 模型类型
    vip: str # VIP类型
    limits: int  # 访问次数
    created_at: int  # 定义created_at字段，类型为日期时间

# 定义ModelLimitTable类
class ModelLimitTable:
    def __init__(self, db):
        self.db = db  # 初始化数据库实例
        self.db.create_tables([ModelLimit])  # 创建EmailCodeTable表

    def get_info_by_user_vip(self, user_tier: str, vip: str, type: str) -> Optional[ModelLimitModel]:
        try:
            modellimit = ModelLimit.select().where(ModelLimit.user_tier == user_tier, ModelLimit.vip == vip, ModelLimit.model_type == type).first()
            return modellimit
        except Exception as e:
>>>>>>> fingerprintAuth-out
            return None
        
    def get_all(self) -> Optional[List[ModelLimitModel]]:
        try:
            modellimits = ModelLimit.select()
            modellimit_list = [ModelLimitModel(**model_to_dict(modellimit)) for modellimit in modellimits] 
            return modellimit_list
        except Exception as e:
<<<<<<< HEAD
            print("========================", e)
            return None


# Instantiate ModelLimitTable class
=======
            print("============get_modellimit_all============", e)
            return None


# 实例化ModelLimitTable类
>>>>>>> fingerprintAuth-out
ModelLimitInstance = ModelLimitTable(DB)

