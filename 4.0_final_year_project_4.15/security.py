from Crypto.PublicKey import RSA
# 这是从 pycryptodome 库中导入的模块，用于生成和处理 RSA 公钥和私钥。
from Crypto.Cipher import PKCS1_OAEP
# 导入了 PKCS1_OAEP 加密方案，这是 RSA 的一种加密填充模式，提供更高的安全性。
import base64
# Python 内置的 base64 模块，用于对二进制数据进行 Base64 编码和解码。



def generate_keys():
    key = RSA.generate(2048)
    with open("private.pem", "wb") as prv_file:
        prv_file.write(key.export_key())
    with open("public.pem", "wb") as pub_file:
        pub_file.write(key.publickey().export_key())
# 选中的代码定义了 generate_keys 函数，用于生成一对 RSA 密钥（2048 位）。私钥保存到 private.pem 文件，公钥保存到 public.pem 文件。这些密钥用于后续的加密和解密操作。

def load_public_key():
    with open("public.pem", "rb") as f:
        return RSA.import_key(f.read())
# 选中的代码定义了 load_public_key 函数，用于从 public.pem 文件中加载 RSA 公钥。它以二进制模式读取文件内容，并通过 RSA.import_key 方法将其解析为可用的公钥对象。


def load_private_key():
    with open("private.pem", "rb") as f:
        return RSA.import_key(f.read())
# 选中的代码定义了 load_private_key 函数，用于从 private.pem 文件中加载 RSA 私钥。它以二进制模式读取文件内容，并通过 RSA.import_key 方法将其解析为可用的私钥对象。

def encrypt_password(password):
    public_key = load_public_key()
    cipher = PKCS1_OAEP.new(public_key)
    encrypted = cipher.encrypt(password.encode())
    return base64.b64encode(encrypted).decode()
# 选中的代码定义了 encrypt_password 函数，用于使用 RSA 公钥加密密码。它加载公钥，使用 PKCS1_OAEP 加密密码，并将加密结果通过 Base64 编码为字符串返回。

def decrypt_password(encrypted_password):
    private_key = load_private_key()
    cipher = PKCS1_OAEP.new(private_key)
    decrypted = cipher.decrypt(base64.b64decode(encrypted_password))
    return decrypted.decode()
# 选中的代码定义了 decrypt_password 函数，用于使用 RSA 私钥解密密码。它加载私钥，使用 PKCS1_OAEP 解密 Base64 解码后的密文，并返回解密后的明文字符串。

if __name__ == "__main__":
    generate_keys()
    print("密钥文件已生成")
