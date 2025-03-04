from peewee import Model, CharField, DateTimeField, fn
from apps.web.internal.db import DB
from pydantic import BaseModel
from typing import Optional
from playhouse.shortcuts import model_to_dict
from datetime import datetime, timedelta
import string
import secrets
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import uuid




class EmailRequest(BaseModel):
    email: str

class VerifyCodeRequest(BaseModel):
    email: str
    code: str

class TimeRequest(BaseModel):
    time: str

# Define EmailCodeTable model
class EmailCodeTable(Model):
    id = CharField(primary_key=True, unique=True)  # Define a unique primary key character field id
    email = CharField(index=True)  # Define index character field email
    code = CharField()  # Define character field code
    created_at = DateTimeField(default=datetime.now)  # Define the default value as the current time for the date time field 'creatd_at'

    class Meta:
        database = DB  # Specify Database
        table_name = 'email_codes'  # Specify table name

# Define Pydance model EmailCodeModel
class EmailCodeModel(BaseModel):
    id: str  # Define the ID field as a string type
    email: str  # Define email field, type as string
    code: str  # Define the code field as a string type
    created_at: datetime  # Define the 'creatd_at' field with a date and time type

# Define the EmailCodeOperations class for manipulating the EmailCodeTable table
class EmailCodeOperations:
    def __init__(self, db):
        self.db = db  # Initialize database instance
        self.db.create_tables([EmailCodeTable])  # Create EmailCodeTable table
        self.server = None
        self.connect()  # Establish connection during initialization


    def generate_code(self, length: int = 6) -> str:
        characters = string.ascii_letters + string.digits  # A character set containing letters and numbers
        return ''.join(secrets.choice(characters) for _ in range(length))

    def is_expired(self, created_at: datetime) -> bool:
        print("is_expired ", datetime.now() , created_at, created_at + timedelta(minutes=10))
        return datetime.now() > created_at + timedelta(minutes=10)

    def get_by_email(self, email: str) -> Optional[EmailCodeModel]:
        try:
            # code_record = EmailCodeTable.get(EmailCodeTable.email == email)  # Query records in the database
            code_record = (EmailCodeTable
                .select()
                .where(EmailCodeTable.email == email)
                .order_by(EmailCodeTable.created_at.desc())
                .get())
            
            return EmailCodeModel(**model_to_dict(code_record))  # Convert database objects to Pydantic models and return
        except EmailCodeTable.DoesNotExist:
            return None  # If the query fails, return None

    def create(self, email: str, code: str) -> Optional[EmailCodeModel]:
        code_record = EmailCodeModel(

            id=str(uuid.uuid4()),
            email=email,
            code=code,
            created_at=datetime.now()
        )
        result = EmailCodeTable.create(**code_record.dict())  # Create a new record in the database
        if result:
            return code_record  # Return the created record
        else:
            return None  # If the creation fails, return None

    def connect(self):
        try:   
            self.server = smtplib.SMTP('smtpdm.aliyun.com', 80, timeout=3000)
            self.server.starttls()  # Activate TLS encryption
            self.server.login('service@dgc.degpt.ai', '*********')
            print("SMTP connection successful")
            
        except Exception as e:
            print(f"SMTP connection failed: {e}")
            self.server = None

    def send_email(self, to_email: str, subject: str, body: str):
        if not to_email:
            return

        if not self.server:
            print("SMTP connection lost, try reconnecting")
            self.connect()
            print("Email service recipients:", self.server)
            
        print("Email service recipients:", self.server)
        msg = MIMEMultipart()
        from_email = 'service@dgc.degpt.ai'
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html', "utf-8"))
        

        try:
            self.server.sendmail(from_email, to_email, msg.as_string())
            print(f"Email sent successfully：{to_email}")
        except smtplib.SMTPException as e:
            print(f"Sending email failed: {e}")
            self.server = None  # Make the connection fail in order to reconnect
            self.connect()

            if self.server:
                try:
                    self.server.sendmail(from_email, to_email, msg.as_string())
                    print(f"Email resent successfully：{to_email}")
                except smtplib.SMTPException as e:
                    print(f"Email resend failed: {e}")




    @staticmethod
    def connect_smtp():
        # This is the link to the smtp website, which can be viewed through Google Mail
        # server = smtplib.SMTP('smtp.163.com', 25, timeout=10)

        # server = smtplib.SMTP('smtp.163.com', 465, timeout=3000)
        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=3000)
        # Connect TLS
        server.starttls()
        server.login('ddegptservice@gmail.com', '****************')
        return server

    def ensure_connection(self):
        """Ensure that the SMTP connection is available, and if it is not available, try reconnecting"""
        print("ensure_connection server", self.server)
        if self.server is None:
            print("SMTP connection lost, try reconnecting...")
            self.connect()

        



# Instantiate EmailCodeOperations class
email_code_operations = EmailCodeOperations(DB)

