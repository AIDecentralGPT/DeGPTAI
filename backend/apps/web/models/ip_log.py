from peewee import Model, CharField, BigIntegerField, AutoField
from apps.web.internal.db import DB
from pydantic import BaseModel
from typing import Optional
from playhouse.shortcuts import model_to_dict
import time
import logging
import uuid  # Import UUID module to generate unique ID

log = logging.getLogger(__name__)

# Define the IpLog model
class IpLog(Model):
    id = AutoField()  # Using AutoField as the primary key
    user_id = CharField()  # user id
    ip_address = CharField()  # device ID
    created_at = BigIntegerField(default=lambda: int(time.time()))  # Creation time

    class Meta:
        database = DB  # Specify Database
        table_name = 'ip_logs'  # Specify table name

# Define Pydantic model IpLogModel
class IpLogModel(BaseModel):
    id: Optional[int]  # Define the id field as optional
    user_id: str  # Define the user_id field as a string type
    ip_address: str  # Define the Device_id field as a string type
    created_at: int  # Define the 'creatd_at' field as an integer type


# Define the IpLogsTable class for manipulating the IpLogs table
class IpLogsTable:
    def __init__(self, db):
        self.db = db  # Initialize database instance
        self.db.create_tables([IpLog])  # Create IpLog table

    def insert_new_ip_log(self, user_id: str, ip_address: str) -> Optional[IpLogModel]:
        log.info(f"Inserting new IP log for user_id: {user_id} with ip_address: {ip_address}")
        created_at = int(time.time())
        try:
            ip_log = IpLog.create(ip_address=ip_address, created_at=created_at,user_id=user_id)
            inserted_ip_log = IpLog.get(IpLog.id == ip_log.id)
            return IpLogModel(**model_to_dict(inserted_ip_log))
        except Exception as e:
            log.error(f"Error inserting IP log: {e}")
            return None


    # Retrieve IP logs based on ipaddress
    def get_ip_log_by_address(self, ip_address: str) -> Optional[IpLogModel]:
        try:
            ip_log = IpLog.get(IpLog.ip_address == ip_address)  # Retrieve IP logs from the database
            return IpLogModel(**model_to_dict(ip_log))  # Convert database objects to Pydantic models and return
        except IpLog.DoesNotExist:
            return None  # If the query fails, return None

    # Update IP log information
    def update_ip_log_by_address(self, ip_address: str, updated: dict) -> Optional[IpLogModel]:
        try:
            query = IpLog.update(**updated).where(IpLog.ip_address == ip_address)  # Update IP log information
            query.execute()  # Perform update operation
            ip_log = IpLog.get(IpLog.ip_address == ip_address)  # Query the updated IP logs
            return IpLogModel(**model_to_dict(ip_log))  # Convert database objects to Pydantic models and return
        except IpLog.DoesNotExist:
            return None  # If the update fails, return None

    # Delete IP log information
    def delete_ip_log_by_address(self, ip_address: str) -> bool:
        try:
            query = IpLog.delete().where(IpLog.ip_address == ip_address)  # Delete IP log information
            result = query.execute()  # Perform deletion operation
            return result > 0  # If the deletion is successful, return True; otherwise, return False
        except:
            return False  # If an exception occurs, return False

# Instantiate the IpLogsTable class
ip_logs_table = IpLogsTable(DB)
