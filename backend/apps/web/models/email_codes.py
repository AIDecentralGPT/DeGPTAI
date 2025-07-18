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
    language: str

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

    def create_email_body(self, address:str, code:str, language: str):
        email_body = {
            "en-US": f"""<html><head><meta charset="UTF-8"></head><body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 750px; margin: 0 auto; padding: 20px;">
                        <h1 style="color: #2c3e50;">Confirm Your Email Address</h1>
                        <p style="color:rgba(184, 142, 86, 1); font-size: 20px;">Wallet Address: {address}</p>
                        <p>Let's make sure this is the right email address for you. Please enter the following verification code to continue using DeGPT:</p>
                        <p style="font-size: 24px; font-weight: bold; color: #3498db;">{code}</p>
                        <p>Verification codes expire after two hours.</p>
                        <p>Thank you.</p>  
                        <div style="margin-top: 20px; border-top: 1px solid #eee; padding-top: 20px;">
                            <img src="https://www.degpt.ai/static/email/telegram_icon_url.png" alt="DecentralGPT Logo" style="width: 200px; height: auto;">
                            <div style="margin-top: 15px;">
                                <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://www.decentralgpt.org/">DecentralGPT Website</a>
                                <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://x.com/DecentralGPT">Follow on Twitter</a>
                                <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://t.me/DecentralGPT">Join Telegram</a>
                            </div>
                            <p>Best regards,<br>DecentralGPT Team</p>
                        </div>
                    </div></body></html>""",
            "de-DE": f"""<html><head><meta charset="UTF-8"></head><body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 750px; margin: 0 auto; padding: 20px;">
                        <h1 style="color: #2c3e50;">Bestätigen Sie Ihre E-Mail-Adresse</h1>
                        <p style="color:rgba(184, 142, 86, 1); font-size: 20px;">Wallet-Adresse: {address}</p>
                        <p>Lassen Sie uns sicherstellen, dass dies die richtige E-Mail-Adresse für Sie ist. Bitte geben Sie den folgenden Bestätigungscode ein, um DeGPT weiterhin nutzen zu können:</p>
                        <p style="font-size: 24px; font-weight: bold; color: #3498db;">{code}</p>
                        <p>Bestätigungscodes verfallen nach zwei Stunden.</p>
                        <p>Vielen Dank.</p>  
                        <div style="margin-top: 20px; border-top: 1px solid #eee; padding-top: 20px;">
                            <img src="https://www.degpt.ai/static/email/telegram_icon_url.png" alt="DecentralGPT Logo" style="width: 200px; height: auto;">
                            <div style="margin-top: 15px;">
                                <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://www.decentralgpt.org/">DecentralGPT Webseite</a>
                                <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://x.com/DecentralGPT">Folgen Sie uns auf Twitter</a>
                                <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://t.me/DecentralGPT">Telegram beitreten</a>
                            </div>
                            <p>Mit freundlichen Grüßen,<br>Das DecentralGPT Team</p>
                        </div>
                    </div></body></html>""",
            "es-ES": f"""<html><head><meta charset="UTF-8"></head><body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 750px; margin: 0 auto; padding: 20px;">
                        <h1 style="color: #2c3e50;">Confirma tu dirección de correo electrónico</h1>
                        <p style="color:rgba(184, 142, 86, 1); font-size: 20px;">Dirección de Wallet: {address}</p>
                        <p>Verifiquemos que esta es la dirección de correo correcta para ti. Por favor ingresa el siguiente código de verificación para continuar usando DeGPT:</p>
                        <p style="font-size: 24px; font-weight: bold; color: #3498db;">{code}</p>
                        <p>Los códigos de verificación expiran después de dos horas.</p>
                        <p>Gracias.</p>  
                        <div style="margin-top: 20px; border-top: 1px solid #eee; padding-top: 20px;">
                            <img src="https://www.degpt.ai/static/email/telegram_icon_url.png" alt="DecentralGPT Logo" style="width: 200px; height: auto;">
                            <div style="margin-top: 15px;">
                                <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://www.decentralgpt.org/">Sitio Web de DecentralGPT</a>
                                <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://x.com/DecentralGPT">Síguenos en Twitter</a>
                                <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://t.me/DecentralGPT">Únete a Telegram</a>
                            </div>
                            <p>Saludos cordiales,<br>El equipo de DecentralGPT</p>
                        </div>
                    </div></body></html>""",
            "fr-FR": f"""<html><head><meta charset="UTF-8"></head><body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 750px; margin: 0 auto; padding: 20px;">
                        <h1 style="color: #2c3e50;">Confirmez votre adresse email</h1>
                        <p style="color:rgba(184, 142, 86, 1); font-size: 20px;">Adresse du portefeuille : {address}</p>
                        <p>Vérifions qu'il s'agit bien de votre adresse email. Veuillez saisir le code de vérification suivant pour continuer à utiliser DeGPT :</p>
                        <p style="font-size: 24px; font-weight: bold; color: #3498db;">{code}</p>
                        <p>Les codes de vérification expirent au bout de deux heures.</p>
                        <p>Merci.</p>  
                        <div style="margin-top: 20px; border-top: 1px solid #eee; padding-top: 20px;">
                            <img src="https://www.degpt.ai/static/email/telegram_icon_url.png" alt="DecentralGPT Logo" style="width: 200px; height: auto;">
                            <div style="margin-top: 15px;">
                                <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://www.decentralgpt.org/">Site Web DecentralGPT</a>
                                <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://x.com/DecentralGPT">Suivez-nous sur Twitter</a>
                                <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://t.me/DecentralGPT">Rejoignez Telegram</a>
                            </div>
                            <p>Cordialement,<br>L'équipe DecentralGPT</p>
                        </div>
                    </div></body></html>""",
            "id-ID": f"""<html><head><meta charset="UTF-8"></head><body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 750px; margin: 0 auto; padding: 20px;">
                        <h1 style="color: #2c3e50;">Konfirmasi Alamat Email Anda</h1>
                        <p style="color:rgba(184, 142, 86, 1); font-size: 20px;">Alamat Wallet: {address}</p>
                        <p>Mari pastikan ini adalah alamat email yang benar untuk Anda. Silakan masukkan kode verifikasi berikut untuk terus menggunakan DeGPT:</p>
                        <p style="font-size: 24px; font-weight: bold; color: #3498db;">{code}</p>
                        <p>Kode verifikasi akan kedaluwarsa setelah dua jam.</p>
                        <p>Terima kasih.</p>  
                        <div style="margin-top: 20px; border-top: 1px solid #eee; padding-top: 20px;">
                            <img src="https://www.degpt.ai/static/email/telegram_icon_url.png" alt="DecentralGPT Logo" style="width: 200px; height: auto;">
                            <div style="margin-top: 15px;">
                                <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://www.decentralgpt.org/">Situs Web DecentralGPT</a>
                                <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://x.com/DecentralGPT">Ikuti di Twitter</a>
                                <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://t.me/DecentralGPT">Bergabung dengan Telegram</a>
                            </div>
                            <p>Salam hormat,<br>Tim DecentralGPT</p>
                        </div>
                    </div></body></html>""",
            "ja-JP": f"""<html><head><meta charset="UTF-8"></head><body style="font-family: 'Hiragino Sans', 'Hiragino Kaku Gothic Pro', Meiryo, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 750px; margin: 0 auto; padding: 20px;">
                        <h1 style="color: #2c3e50;">メールアドレスの確認</h1>
                        <p style="color:rgba(184, 142, 86, 1); font-size: 20px;">ウォレットアドレス: {address}</p>
                        <p>登録いただいたメールアドレスが正しいか確認いたします。DeGPTをご利用になるには、以下の確認コードを入力してください:</p>
                        <p style="font-size: 24px; font-weight: bold; color: #3498db;">{code}</p>
                        <p>確認コードの有効期限は2時間です。</p>
                        <p>よろしくお願いいたします。</p>  
                        <div style="margin-top: 20px; border-top: 1px solid #eee; padding-top: 20px;">
                            <img src="https://www.degpt.ai/static/email/telegram_icon_url.png" alt="DecentralGPTロゴ" style="width: 200px; height: auto;">
                            <div style="margin-top: 15px;">
                                <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://www.decentralgpt.org/">DecentralGPT公式サイト</a>
                                <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://x.com/DecentralGPT">Twitterでフォロー</a>
                                <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://t.me/DecentralGPT">Telegramに参加</a>
                            </div>
                            <p>DecentralGPTチームより</p>
                        </div>
                    </div></body></html>""",
            "ko-KR": f"""<html><head><meta charset="UTF-8"></head><body style="font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', Dotum, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 750px; margin: 0 auto; padding: 20px;">
                        <h1 style="color: #2c3e50;">이메일 주소 확인</h1>
                        <p style="color:rgba(184, 142, 86, 1); font-size: 20px;">지갑 주소: {address}</p>
                        <p>등록하신 이메일 주소가 정확한지 확인해 주세요. DeGPT를 계속 사용하시려면 아래의 인증 코드를 입력해 주십시오:</p>
                        <p style="font-size: 24px; font-weight: bold; color: #3498db;">{code}</p>
                        <p>인증 코드는 2시간 후에 만료됩니다.</p>
                        <p>감사합니다.</p>  
                        <div style="margin-top: 20px; border-top: 1px solid #eee; padding-top: 20px;">
                            <img src="https://www.degpt.ai/static/email/telegram_icon_url.png" alt="DecentralGPT 로고" style="width: 200px; height: auto;">
                            <div style="margin-top: 15px;">
                                <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://www.decentralgpt.org/">DecentralGPT 웹사이트</a>
                                <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://x.com/DecentralGPT">트위터 팔로우</a>
                                <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://t.me/DecentralGPT">텔레그램 참여</a>
                            </div>
                            <p>감사합니다.<br>DecentralGPT 팀 드림</p>
                        </div>
                    </div></body></html>""",
            "pt-PT": f"""<html><head><meta charset="UTF-8"></head><body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 750px; margin: 0 auto; padding: 20px;">
                        <h1 style="color: #2c3e50;">Confirme seu endereço de e-mail</h1>
                        <p style="color:rgba(184, 142, 86, 1); font-size: 20px;">Endereço da Carteira: {address}</p>
                        <p>Vamos confirmar se este é o e-mail correto. Por favor, insira o seguinte código de verificação para continuar usando o DeGPT:</p>
                        <p style="font-size: 24px; font-weight: bold; color: #3498db;">{code}</p>
                        <p>Os códigos de verificação expiram após duas horas.</p>
                        <p>Agradecemos sua atenção.</p>  
                        <div style="margin-top: 20px; border-top: 1px solid #eee; padding-top: 20px;">
                            <img src="https://www.degpt.ai/static/email/telegram_icon_url.png" alt="Logo DecentralGPT" style="width: 200px; height: auto;">
                            <div style="margin-top: 15px;">
                                <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://www.decentralgpt.org/">Site do DecentralGPT</a>
                                <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://x.com/DecentralGPT">Siga-nos no Twitter</a>
                                <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://t.me/DecentralGPT">Junte-se ao Telegram</a>
                            </div>
                            <p>Atenciosamente,<br>Equipe DecentralGPT</p>
                        </div>
                    </div></body></html>""",
            "ru-RU": f"""<html><head><meta charset="UTF-8"></head><body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 750px; margin: 0 auto; padding: 20px;">
                    <h1 style="color: #2c3e50;">Подтвердите ваш email-адрес</h1>
                    <p style="color:rgba(184, 142, 86, 1); font-size: 20px;">Адрес кошелька: {address}</p>
                    <p>Пожалуйста, подтвердите, что это правильный email. Введите следующий код для продолжения использования DeGPT:</p>
                    <p style="font-size: 24px; font-weight: bold; color: #3498db;">{code}</p>
                    <p>Код действителен в течение 2 часов.</p>
                    <p>Спасибо!</p>  
                    <div style="margin-top: 20px; border-top: 1px solid #eee; padding-top: 20px;">
                        <img src="https://www.degpt.ai/static/email/telegram_icon_url.png" alt="Логотип DecentralGPT" style="width: 200px; height: auto;">
                        <div style="margin-top: 15px;">
                            <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://www.decentralgpt.org/">Сайт DecentralGPT</a>
                            <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://x.com/DecentralGPT">Twitter</a>
                            <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://t.me/DecentralGPT">Telegram</a>
                        </div>
                        <p>С уважением,<br>Команда DecentralGPT</p>
                    </div>
                </div></body></html>""",
            "th-TH": f"""<html><head><meta charset="UTF-8"></head><body style="font-family: 'Sukhumvit Set', 'Kanit', 'Noto Sans Thai', sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 750px; margin: 0 auto; padding: 20px;">
                    <h1 style="color: #2c3e50;">ยืนยันอีเมลของคุณ</h1>
                    <p style="color:rgba(184, 142, 86, 1); font-size: 20px;">ที่อยู่ Wallet: {address}</p>
                    <p>โปรดยืนยันว่าเป็นอีเมลที่ถูกต้อง กรุณาใส่รหัสยืนยันด้านล่างเพื่อใช้งาน DeGPT ต่อไป:</p>
                    <p style="font-size: 24px; font-weight: bold; color: #3498db;">{code}</p>
                    <p>รหัสยืนยันจะมีอายุ 2 ชั่วโมง</p>
                    <p>ขอบคุณ</p>  
                    <div style="margin-top: 20px; border-top: 1px solid #eee; padding-top: 20px;">
                        <img src="https://www.degpt.ai/static/email/telegram_icon_url.png" alt="โลโก้ DecentralGPT" style="width: 200px; height: auto;">
                        <div style="margin-top: 15px;">
                            <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://www.decentralgpt.org/">เว็บไซต์ DecentralGPT</a>
                            <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://x.com/DecentralGPT">ติดตาม Twitter</a>
                            <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://t.me/DecentralGPT">เข้าร่วม Telegram</a>
                        </div>
                        <p>ด้วยความนับถือ<br>ทีม DecentralGPT</p>
                    </div>
                </div></body></html>""",
            "tr-TR": f"""<html><head><meta charset="UTF-8"></head><body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 750px; margin: 0 auto; padding: 20px;">
                    <h1 style="color: #2c3e50;">E-posta Adresinizi Doğrulayın</h1>
                    <p style="color:rgba(184, 142, 86, 1); font-size: 20px;">Cüzdan Adresi: {address}</p>
                    <p>Doğru e-posta adresiniz olduğunu teyit edelim. Lütfen DeGPT'yi kullanmaya devam etmek için aşağıdaki doğrulama kodunu girin:</p>
                    <p style="font-size: 24px; font-weight: bold; color: #3498db;">{code}</p>
                    <p>Doğrulama kodları 2 saat sonra geçersiz olacaktır.</p>
                    <p>Teşekkür ederiz.</p>  
                    <div style="margin-top: 20px; border-top: 1px solid #eee; padding-top: 20px;">
                        <img src="https://www.degpt.ai/static/email/telegram_icon_url.png" alt="DecentralGPT Logosu" style="width: 200px; height: auto;">
                        <div style="margin-top: 15px;">
                            <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://www.decentralgpt.org/">DecentralGPT Web Sitesi</a>
                            <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://x.com/DecentralGPT">Twitter'da Takip Et</a>
                            <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://t.me/DecentralGPT">Telegram'a Katıl</a>
                        </div>
                        <p>Saygılarımızla,<br>DecentralGPT Ekibi</p>
                    </div>
                </div></body></html>""",
            "vi-VN": f"""<html><head><meta charset="UTF-8"></head><body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 750px; margin: 0 auto; padding: 20px;">
                    <h1 style="color: #2c3e50;">Xác nhận địa chỉ email</h1>
                    <p style="color:rgba(184, 142, 86, 1); font-size: 20px;">Địa chỉ Ví: {address}</p>
                    <p>Vui lòng xác nhận đây là địa chỉ email chính xác của bạn. Nhập mã xác minh bên dưới để tiếp tục sử dụng DeGPT:</p>
                    <p style="font-size: 24px; font-weight: bold; color: #3498db;">{code}</p>
                    <p>Mã xác minh sẽ hết hạn sau 2 giờ.</p>
                    <p>Trân trọng cảm ơn.</p>  
                    <div style="margin-top: 20px; border-top: 1px solid #eee; padding-top: 20px;">
                        <img src="https://www.degpt.ai/static/email/telegram_icon_url.png" alt="Logo DecentralGPT" style="width: 200px; height: auto;">
                        <div style="margin-top: 15px;">
                            <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://www.decentralgpt.org/">Trang web DecentralGPT</a>
                            <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://x.com/DecentralGPT">Theo dõi trên Twitter</a>
                            <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://t.me/DecentralGPT">Tham gia Telegram</a>
                        </div>
                        <p>Trân trọng,<br>Đội ngũ DecentralGPT</p>
                    </div>
                </div></body></html>""",
            "zh-CN": f"""<html><head><meta charset="UTF-8"></head><body style="font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 750px; margin: 0 auto; padding: 20px;">
                    <h1 style="color: #2c3e50;">确认您的电子邮箱地址</h1>
                    <p style="color:rgba(184, 142, 86, 1); font-size: 20px;">钱包地址: {address}</p>
                    <p>请确认这是您正确的电子邮箱地址。请输入以下验证码以继续使用DeGPT：</p>
                    <p style="font-size: 24px; font-weight: bold; color: #3498db;">{code}</p>
                    <p>验证码将在2小时后失效。</p>
                    <p>感谢您的配合。</p>  
                    <div style="margin-top: 20px; border-top: 1px solid #eee; padding-top: 20px;">
                        <img src="https://www.degpt.ai/static/email/telegram_icon_url.png" alt="DecentralGPT 标志" style="width: 200px; height: auto;">
                        <div style="margin-top: 15px;">
                            <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://www.decentralgpt.org/">DecentralGPT 官网</a>
                            <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://x.com/DecentralGPT">关注Twitter</a>
                            <a style="margin-right: 10px; color: #3498db; text-decoration: none;" href="https://t.me/DecentralGPT">加入Telegram</a>
                        </div>
                        <p>此致<br>DecentralGPT 团队</p>
                    </div>
                </div></body></html>"""
        }
        return email_body.get(language, "en-US")



# 实例化EmailCodeOperations类
email_code_operations = EmailCodeOperations(DB)

