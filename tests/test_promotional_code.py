import os
from unittest import TestCase
from src import aes, promotional_code

CURRENT_DIR = os.getcwd()


# noinspection SqlNoDataSourceInspection,SpellCheckingInspection,SqlResolve
class TestUtils(TestCase):
    def setUp(self):
        pass

    def test_generate_with_rule_id(self):
        random_str, encrypt_symbol = promotional_code.generate_with_rule_id('a', 'a')
        print('uuid 生成的随机串为 {}'.format(random_str))
        print('根据规则id与uuid生成的随机串获得的加密串为{}'.format(encrypt_symbol))
        total = sum([int(i) if i.isdigit() else int(ord(i)) for i in list(random_str)])
        print('随机串总长度为{}'.format(total))
        seed = chr(total) if total > 127 else chr(total) + chr(total)
        print('seed 为 {}'.format(seed))
        decrypted = aes.get_decrypt_hex_bytes(encrypt_symbol)
        print('解密结果为{}'.format(decrypted))
        need_seed = decrypted[0] if total > 127 else decrypted[:2]
        self.assertEqual(seed, need_seed)
