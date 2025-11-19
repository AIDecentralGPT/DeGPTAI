import secrets
import hashlib
import string

class ApiUtils:
    def generate_key_with_hash(self) -> tuple[str, str]:
        chars = string.ascii_letters + string.digits + string.punctuation
        key = ''.join(secrets.choice(chars) for _ in range(8))
        # 计算哈希（加盐 + 多次哈希增强安全性）
        salt = "degpt"  # 随机盐值
        key_hash = hashlib.pbkdf2_hmac(
            'sha256',  # 哈希算法
            key.encode('utf-8'),  # 密钥明文
            salt.encode('utf-8'),  # 盐值
            100000  # 迭代次数
        ).hex()
        # 存储时需保存 盐值 + 哈希值（用分隔符区分）
        stored_value = f"{salt}-{key_hash}"
        return key, stored_value

    def verify_key_with_hash(self, input_key: str, stored_value: str) -> bool:
        try:
            salt, key_hash = stored_value.split('-')
            input_hash = hashlib.pbkdf2_hmac(
                'sha256',
                input_key.encode('utf-8'),
                salt.encode('utf-8'),
                100000
            ).hex()
            return input_hash == key_hash
        except (ValueError, TypeError):
            return False
    
ApiUtilInstance = ApiUtils()