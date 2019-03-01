from Crypto.Cipher import AES


class AESUtil:
    """
    AES加密解密
    >>> a = AESUtil()
    >>> a.encrypt_hex('1231')
    67cffc63
    >>> d = AESUtil()
    >>> d.decrypt_hex('67cffc63')
    1231
    """

    def __init__(self, secret='eNKUnNN0ciKExL8R'):
        self.obj = AES.new(secret, AES.MODE_CFB, 'e9ixND5wkhDYrLvc')

    def encrypt(self, need_encrypt: str):
        ciphertext = self.obj.encrypt(need_encrypt)
        return ciphertext

    def encrypt_hex(self, need_encrypt: str):
        ciphertext = self.obj.encrypt(need_encrypt)
        return bytes.hex(ciphertext)

    def decrypt(self, nee_decrypt: bytes):
        return self.obj.decrypt(nee_decrypt)

    def decrypt_hex(self, need_decrypt: str):
        need_decrypt_hex = bytes.fromhex(need_decrypt)
        print(need_decrypt_hex)
        return self.obj.decrypt(need_decrypt_hex)


def get_encrypt_hex(s):
    obj = AESUtil()
    return obj.encrypt_hex(s)


def get_decrypt_hex(s):
    obj = AESUtil()
    try:
        result = obj.decrypt_hex(s)
        print(result)
        data = result.decode()
    except Exception:
        import traceback
        traceback.print_exc()
        data = False
    return data


def get_decrypt_hex_bytes(s):
    obj = AESUtil()
    try:
        result = obj.decrypt_hex(s)

        data = result.decode()
    except Exception:
        import traceback
        traceback.print_exc()
        data = False
    return data
