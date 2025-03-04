from pydantic import BaseModel
from peewee import * 
from playhouse.shortcuts import model_to_dict 
from typing import List, Union, Optional 

import uuid
import time

from apps.web.internal.db import DB, aspect_database_operations


####################
# ErrorLog DB Schema
####################

# Define the Error Log model
class ErrorLog(Model):
    id = CharField(unique=True)  # Define a unique character field ID
    name = CharField()  # name
    err = TextField()  # error message
    created_at = BigIntegerField()  # Create time
    updated_at = BigIntegerField()  # Update time

    class Meta:
        database = DB  # Specify Database
        table_name = 'error_log'  # Specify table name

# Define Pydantic Model Error Log
class ErrorLogModel(BaseModel):
    id: str  # Define the id field as a string type
    name: str  # Define the name field as a string type
    err: str  # Define error message field, type as string
    created_at: int  # Define the 'creatd_at' field, which is of type integer and represents the epoch timestamp
    updated_at: int  # Define the 'updated_at' field, which is of type integer and represents the epoch timestamp

# Define Pydantic Model Error Log
class ErrorLogRequest(BaseModel):
    name: str  # Define Name Field
    err: str  # Define error message fields


# Define the Error Log Table class for manipulating the Error Log table
class ErrorLogTable:
    def __init__(self, db):
        self.db = db  # Initialize database instance
        self.db.create_tables([ErrorLog])  # Create an Error Log table

    # Insert new user
    def insert_errorlog(
        self,
        name: str,
        err: str
    ) -> Optional[ErrorLogModel]:
        
        # Create UserModel instance
        errLog = ErrorLogModel(
            **{
                "id": str(uuid.uuid4()),
                "name": name,
                "err": err,
                "created_at": int(time.time()),
                "updated_at": int(time.time())
            }
        )

        # Create a new log in the database
        result = ErrorLog.create(**errLog.model_dump())
        
        # return result info:
        return result  # Return the created log

# Instantiate the Error Log Table class
ErrorLogInstance = ErrorLogTable(DB)
