from peewee import Model, CharField, DateTimeField, fn  # 导入Peewee中的Model、CharField和DateTimeField
from apps.web.internal.db import DB  # 导入数据库实例DB
from pydantic import BaseModel  # 导入Pydantic中的BaseModel
from typing import Optional  # 导入类型提示
from playhouse.shortcuts import model_to_dict  # 导入Peewee中的model_to_dict方法
from datetime import datetime, timedelta
import string
import secrets
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import uuid
import os

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PWD = os.getenv("EMAIL_PWD")


class EmailRequest(BaseModel):
    email: str

class VerifyCodeRequest(BaseModel):
    email: str
    code: str

class TimeRequest(BaseModel):
    time: str

# 定义EmailCodeTable模型
class EmailCodeTable(Model):
    id = CharField(primary_key=True, unique=True)  # 定义唯一的主键字符字段id
    email = CharField(index=True)  # 定义索引字符字段email
    code = CharField()  # 定义字符字段code
    created_at = DateTimeField(default=datetime.now)  # 定义默认值为当前时间的日期时间字段created_at

    class Meta:
        database = DB  # 指定数据库
        table_name = 'email_codes'  # 指定表名

# 定义Pydantic模型EmailCodeModel
class EmailCodeModel(BaseModel):
    id: str  # 定义id字段，类型为字符串
    email: str  # 定义email字段，类型为字符串
    code: str  # 定义code字段，类型为字符串
    created_at: datetime  # 定义created_at字段，类型为日期时间

# 定义EmailCodeOperations类，用于操作EmailCodeTable表
class EmailCodeOperations:
    def __init__(self, db):
        self.db = db  # 初始化数据库实例
        self.db.create_tables([EmailCodeTable])  # 创建EmailCodeTable表
        self.server = None
        self.connect()  # 初始化时建立连接


    def generate_code(self, length: int = 6) -> str:
        characters = string.ascii_letters + string.digits  # 包含字母和数字的字符集
        return ''.join(secrets.choice(characters) for _ in range(length))

    def is_expired(self, created_at: datetime) -> bool:
        print("is_expired ", datetime.now() , created_at, created_at + timedelta(minutes=10))
        return datetime.now() > created_at + timedelta(minutes=10)

    def get_by_email(self, email: str) -> Optional[EmailCodeModel]:
        try:
            # code_record = EmailCodeTable.get(EmailCodeTable.email == email)  # 查询数据库中的记录
            code_record = (EmailCodeTable
                .select()
                .where(EmailCodeTable.email == email)
                .order_by(EmailCodeTable.created_at.desc())
                .get())
            
            return EmailCodeModel(**model_to_dict(code_record))  # 将数据库对象转换为Pydantic模型并返回
        except EmailCodeTable.DoesNotExist:
            return None  # 如果查询失败，返回None

    def create(self, email: str, code: str) -> Optional[EmailCodeModel]:
        code_record = EmailCodeModel(

            id=str(uuid.uuid4()),  # 这里使用email作为id，只是为了示例，实际情况可能需要使用UUID或其他唯一标识符
            email=email,
            code=code,
            created_at=datetime.now()
        )
        result = EmailCodeTable.create(**code_record.dict())  # 在数据库中创建新记录
        if result:
            return code_record  # 返回创建的记录
        else:
            return None  # 如果创建失败，返回None

    # def send_email(self, to_email: str, subject: str, body: str):

    #     if not to_email or to_email == '':
    #         return

    #     if self.server is None:
    #         print("SMTP连接已丢失，尝试重新连接")
    #         # try:
    #         self.connect()
    #         self.send_email(to_email, subject, body)  # 确保连接有效
    #         # except Exception as e:
    #         #     print(e)
    #         #     print("send_email error")
    #         #     self.connect()
    #         #     self.send_email(to_email, subject, body)  # 确保连接有效
                
    #         return
    #     else:
    #         print("发送邮件", self.server)
    #         msg = MIMEMultipart()  # message结构体初始化
    #         from_email = 'degpt'
    #         msg['From'] = from_email
    #         msg['To'] = to_email
    #         msg['Subject'] = subject
    #         try:
    #             msg.attach(MIMEText(body, 'html', "utf-8"))
                
    #             self.server.sendmail(from_email, to_email, msg.as_string())
    #             print(f"邮件发送成功：{to_email}")
    #         except Exception as e:
    #             print(e)
    #             print("send_email error")
    #             self.connect()
    #             self.send_email(to_email, subject, body)  # 确保连接有效
            
    #     # finally:
    #     #     self.server.quit()  # Close the connection


    def connect(self):
        try:   
            self.server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT, timeout=3000)
            self.server.starttls()  # 启动TLS加密
            self.server.login(EMAIL_USER, EMAIL_PWD)
            print("SMTP连接成功")
            
        except Exception as e:
            print(f"SMTP连接失败: {e}")
            self.server = None

    def send_email(self, to_email: str, subject: str, body: str):
        if not to_email:
            return

        if not self.server:
            print("SMTP连接已丢失，尝试重新连接")
            self.connect()
            print("邮件服务对象", self.server)
            
        print("邮件服务对象", self.server)
        msg = MIMEMultipart()
        from_email = EMAIL_USER
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html', "utf-8"))
        

        try:
            self.server.sendmail(from_email, to_email, msg.as_string())
            print(f"邮件发送成功：{to_email}")
        except smtplib.SMTPException as e:
            print(f"发送邮件失败: {e}")
            self.server = None  # 使连接失效，以便重新连接
            self.connect()

            if self.server:
                try:
                    self.server.sendmail(from_email, to_email, msg.as_string())
                    print(f"邮件重新发送成功：{to_email}")
                except smtplib.SMTPException as e:
                    print(f"邮件重新发送失败: {e}")


    @staticmethod
    def connect_smtp():
        # 这里是smtp网站的连接，可以通过谷歌邮箱查看
        server = smtplib.SMTP(EMAIL_SERVER, EMAIL_PORT, timeout=3000)
        # 连接tls
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PWD)
        return server

    def ensure_connection(self):
        """确保SMTP连接可用，如果不可用则尝试重连"""
        print("ensure_connection server", self.server)
        if self.server is None:
            print("SMTP连接已丢失，尝试重新连接...")
            self.connect()

        



# 实例化EmailCodeOperations类
email_code_operations = EmailCodeOperations(DB)

