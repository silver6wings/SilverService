from cryptography.fernet import Fernet
import base64

custom_key_string = "silver6wings"  # 自定义的字符串密钥


def get_cryptor(key):
    # 将字符串密钥转换为字节类型
    # 这里使用 UTF-8 编码将字符串转换为字节
    custom_key = key.encode('utf-8')

    # 如果密钥长度不足，可以补充填充
    while len(custom_key) < 32:
        custom_key += b'='

    # 创建 Fernet 对象
    fernet = Fernet(base64.urlsafe_b64encode(custom_key))
    return fernet


cryptor = get_cryptor(custom_key_string)


def auth_encode(data: str) -> str:
    # 加密数据
    fernet = cryptor
    encrypted_data = fernet.encrypt(data.encode('utf-8'))
    # print("Encrypted data:", encrypted_data)
    return encrypted_data.decode('utf-8')


def auth_decode(data: str) -> str:
    # 解密数据
    fernet = cryptor
    decrypted_data = fernet.decrypt(data.encode('utf-8'))
    # print("Decrypted data:", decrypted_data.decode())
    return decrypted_data.decode('utf-8')


if __name__ == '__main__':
    # 要加密的数据
    source = '20260101'
    temp = auth_encode(source)
    print(temp)
    temp = auth_decode(temp)
    print(temp)
    print(temp == source)
