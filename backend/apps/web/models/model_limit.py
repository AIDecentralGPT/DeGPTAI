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
            return None
        
    def get_all(self) -> Optional[List[ModelLimitModel]]:
        try:
            modellimits = ModelLimit.select()
            modellimit_list = [ModelLimitModel(**model_to_dict(modellimit)) for modellimit in modellimits] 
            return modellimit_list
        except Exception as e:
            print("========================", e)
            return None


# Instantiate ModelLimitTable class
ModelLimitInstance = ModelLimitTable(DB)

