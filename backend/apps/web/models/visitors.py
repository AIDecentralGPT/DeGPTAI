from peewee import Model, CharField
from apps.web.internal.db import DB
from pydantic import BaseModel
from typing import List, Union, Optional
from playhouse.shortcuts import model_to_dict
from utils.misc import get_gravatar_url
import uuid

# Define the Visitors model
class Visitors(Model):
    id = CharField(unique=True)  # Define a unique character field ID
    visitor_id = CharField()  # Define the character field visitor_id

    class Meta:
        database = DB  # Specify Database
        table_name = 'visitors'  # Specify table name

# Define Pydantic Model VisitorModel
class VisitorModel(BaseModel):
    id: str  # Define the ID field as a string type
    visitor_id: str  # Define the visitor_id field as a string type

# Define the VisitorsTable class for manipulating the VisitorsTable table
class VisitorsTable:
    def __init__(self, db):
        self.db = db  # Initialize database instance
        self.db.create_tables([Visitors])  # Create Visitors table

    # Insert new visitor
    def insert_new_visitor(self, id: str, visitor_id: str) -> Optional[VisitorModel]:
        visitor = VisitorModel(id=id, visitor_id=visitor_id)  # Create VisitorModel instance
        result = Visitors.create(**visitor.dict())  # Create a new visitor in the database
        print("result: ", result,id, visitor_id)
        if result:
            return visitor  # Return the created visitor
        else:
            return None  # If the creation fails, return None

    # Retrieve visitors based on visitor_id
    def get_visitor_by_id(self, visitor_id: str) -> Optional[VisitorModel]:
        try:
            visitor = Visitors.get(Visitors.visitor_id == visitor_id)  # Query visitors in the database
            return VisitorModel(**model_to_dict(visitor))  # Convert database objects to Pydantic models and return
        except Visitors.DoesNotExist:
            return None  # If the query fails, return None

    # Update visitor information
    def update_visitor_by_id(self, visitor_id: str, updated: dict) -> Optional[VisitorModel]:
        try:
            query = Visitors.update(**updated).where(Visitors.visitor_id == visitor_id)
            query.execute()
            visitor = Visitors.get(Visitors.visitor_id == visitor_id)  # Query updated visitors
            return VisitorModel(**model_to_dict(visitor))  # Convert database objects to Pydantic models and return
        except Visitors.DoesNotExist:
            # If the update fails, return None
            return None

    # Delete visitor information
    def delete_visitor_by_id(self, visitor_id: str) -> bool:
        try:
            query = Visitors.delete().where(Visitors.visitor_id == visitor_id)
            result = query.execute()
            return result > 0  # If the deletion is successful, return True; otherwise, return False
        except:
            return False  # If an exception occurs, return False

# Instantiate VisitorsTable class
visitors_table = VisitorsTable(DB)
