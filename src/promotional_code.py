"""
生成优惠码
1. 码不保存到库里
2. 码里面有对应的优惠信息
3. 不可以被用户猜到
4. 和美年达、七喜合作，生成5亿个5元和10元码
"""
import datetime
import os
import uuid

import redis

from src import aes

BASE_DIR = os.getcwd()


def generate_with_rule_mark(rule_mark, mark_up):
    """
    返回uuid随机生成字符串，以及与此字符串相关联，包含规则标记的加密串
    """
    random_str = str(uuid.uuid4())[:8]
    total = sum([int(i) if i.isdigit() else int(ord(i)) for i in list(random_str)])
    seed = chr(total) if total > 127 else chr(total) + chr(total)
    symbol = seed + mark_up + str(rule_mark)
    encrypt_symbol = aes.get_encrypt_hex(symbol)
    return random_str, encrypt_symbol


def combine_result(encrypt_symbol, random_str):
    """
    返回两个字符串的奇偶组合
    """
    res = [encrypt_symbol[i // 2] if i % 2 == 0 else random_str[i // 2] for i in range(16)]
    return ''.join(res)


def write_txt_batch(exchange_ids, file_path):
    """
    逐行写入txt
    """
    with open(file_path, 'a') as master:
        master.writelines(exchange_ids)


def generate_promotional_code(rule_mark, total, mark_up, save_path):
    """
    根据`rule_mark`生成`total`个16位优惠券，保存到`save_path`中
    生成规则为：
        1. 使用uuid生成8位随机数
        2. 根据这8位随机数生成一个标记位，这个标记位需要占用两个字符，见（generate_with_rule_mark）方法中seed属性
        3. 使用seed + mark_up + rule_mark拼接成四个字符的字符串 symbol
        4. 把symbol AES CFB加密 生成8字符字符串
        5. 将uuid生成的随机数与symbol生成的字符串进行奇偶拼接，生成16位优惠券码
    支持最大生成不重复券数量为 `(26 + 10) ** 8 * 128 ** 4`
    :param rule_mark: 优惠券特殊标记 只支持 chr(0) ~ chr(127)
    :param total:  生成券的总数
    :param mark_up:  生成本次券的特殊标记
        由于生成券需要使用redis去重，而8g电脑生成5000w券内存就有些吃紧，所以添加一个标记位，当生成券超过5000w时，可以先生成5000w，
        然后使用redis.flushdb()清空生成券使用的redis，从新指定此字段，可保证券永不重复
    :param save_path:
    :return:
    """
    start = datetime.datetime.now()
    r = redis.StrictRedis(
        host='127.0.0.1',
        port=6379,
        password='')
    promotional_codes = []
    for i in range(total):
        while True:
            random_str, encrypt_symbol = generate_with_rule_mark(rule_mark, mark_up)
            if r.sadd('promotional' + encrypt_symbol, random_str):
                promotional_code = combine_result(encrypt_symbol, random_str)
                promotional_codes.append('{}\r\n'.format(promotional_code))
                break
            if len(promotional_codes) > 10000:
                write_txt_batch(promotional_codes, save_path)
                promotional_codes = []
    if len(promotional_codes) > 0:
        write_txt_batch(promotional_codes, save_path)
    end = datetime.datetime.now()
    print('total cost {}'.format(end - start))


def decrypt_promotional_code(code):
    """
    解析出优惠标记
    """
    encrypt_symbol = ''.join([code[i] for i in range(16) if i % 2 == 0])
    random_str = ''.join([code[i] for i in range(16) if i % 2 != 0])
    decrypted = aes.get_decrypt_hex_bytes(encrypt_symbol)
    total = sum([int(i) if i.isdigit() else int(ord(i)) for i in list(random_str)])
    seed = chr(total) if total > 127 else chr(total) + chr(total)
    need_seed = decrypted[0] if total > 127 else decrypted[:2]
    if not seed == need_seed:
        print('标记位不对')
        return False
    return decrypted[-1]
