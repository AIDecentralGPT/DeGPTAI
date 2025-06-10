from peewee import Model, CharField, IntegerField, BigIntegerField # 导入Peewee中的Model、CharField和DateTimeField
from apps.web.internal.db import DB  # 导入数据库实例DB
from pydantic import BaseModel  # 导入Pydantic中的BaseModel
from typing import Optional, List  # 导入类型提示
from playhouse.shortcuts import model_to_dict  # 导入Peewee中的model_to_dict方法

# 定义Models模型
class Models(Model):
    model = CharField(primary_key=True, unique=True)  # 模型名称
    type = IntegerField()  # 模型类型
    created_at = BigIntegerField()  # 定义默认值为当前时间的日期时间字段created_at

    class Meta:
        database = DB  # 指定数据库
        table_name = 'models'  # 指定表名

# 定义Pydantic模型ModelModel
class ModelsModel(BaseModel):
    model: str  # 模型名称
    type: int  # 访客用户次数
    created_at: int  # 定义created_at字段，类型为日期时间

# 定义ModelsTable类
class ModelsTable:
    def __init__(self, db):
        self.db = db  # 初始化数据库实例
        self.db.create_tables([Models])  # 创建Models表

    def get_info_by_model(self, model: str) -> Optional[ModelsModel]:
        try:
            models = Models.get_or_none(ModelsModel.model == model)
            if models is None:
                return None
            else:
                models_dict = model_to_dict(models)  # 将数据库对象转换为字典
                models_model = ModelsModel(**models_dict)  # 将字典转换为Pydantic模型
                return models_model
        except Exception as e:
            print("========================", e)
            return None
        
    def get_info_by_models(self, models: list) -> Optional[List[ModelsModel]]:
        try:
            modelss = Models.select().where(Models.model.in_(models))
            # 将数据库对象转换为字典
            models_list = [ModelsModel(**model_to_dict(model)) for model in modelss]
            return models_list
        except Exception as e:
            print("========================", e)
            return None
        
    def get_all(self) -> Optional[List[ModelsModel]]:
        try:
            modelss = Models.select()
            models_list = [ModelsModel(**model_to_dict(model)) for model in modelss] 
            return models_list
        except Exception as e:
            print("========================", e)
            return None


# 实例化ModelsTable类
ModelsInstance = ModelsTable(DB)

