# Import the required modules
from peewee import Model, CharField, AutoField, ForeignKeyField, BigIntegerField
from apps.web.internal.db import DB
from pydantic import BaseModel
from typing import Optional
from apps.web.models.users import User
from playhouse.shortcuts import model_to_dict
import time
import logging
log = logging.getLogger(__name__)

# Define Device Model
class Device(Model):
    id = AutoField()  # Using AutoField as the primary key
    user_id = CharField()  # user id
    device_id = CharField()  # device ID
    created_at = BigIntegerField(default=lambda: int(time.time()))  # Creation time

    class Meta:
        database = DB  # Specify Database
        table_name = 'devices'  # Specify table name

# Define Pydance model DeviceModel
class DeviceModel(BaseModel):
    id: Optional[int]  # Define the ID field
    user_id: str  # Define the user_id field as a string type
    device_id: str  # Define the Device_id field as a string type
    created_at: int  # Define the 'creatd_at' field as an integer type

# Define the DevicesTable class for manipulating the Devices table
class DevicesTable:
    def __init__(self, db):
        self.db = db  # Initialize database instance
        self.db.create_tables([Device])  # Create Device Table

    # Insert new device
    def insert_new_device(self, user_id: str, device_id: str) -> Optional[DeviceModel]:
        log.info("insert_new_device")

        device_data = {
            "user_id": user_id,
            "device_id": device_id,
            "created_at": int(time.time())
        }
        result = Device.create(**device_data)  # Create a new device in the database
        if result:
            return DeviceModel(id=result.id, **device_data)  # Return the created device
        else:
            return None  # If the creation fails, return None

    # Retrieve the device based on the device ID
    def get_device_by_id(self, device_id: str) -> Optional[DeviceModel]:
        try:
            device = Device.get(Device.device_id == device_id)  # Retrieve devices from the database
            return DeviceModel(**model_to_dict(device))  # Convert database objects to Pydantic models and return
        except Device.DoesNotExist:
            return None  # If the query fails, return None

    # Update device information
    def update_device_by_id(self, device_id: str, updated: dict) -> Optional[DeviceModel]:
        try:
            query = Device.update(**updated).where(Device.device_id == device_id)  # Update device information
            query.execute()  # Perform update operation
            device = Device.get(Device.device_id == device_id)  # Search for updated devices
            return DeviceModel(**model_to_dict(device))  # Convert database objects to Pydantic models and return
        except Device.DoesNotExist:
            return None  # If the update fails, return None

    # Delete device information
    def delete_device_by_id(self, device_id: str) -> bool:
        try:
            query = Device.delete().where(Device.device_id == device_id)  # Delete device records
            result = query.execute()  # Perform deletion operation
            return result > 0  # If the deletion is successful, return True; otherwise, return False
        except:
            return False  # If an exception occurs, return False

# Instantiate the DevicesTable class
devices_table = DevicesTable(DB)
