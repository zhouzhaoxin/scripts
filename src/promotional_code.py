"""
生成优惠码
"""
import datetime
import os
import uuid

import redis

from src import aes

BASE_DIR = os.getcwd()


def generate_with_rule_id(rule_id, mark_up):
    random_str = str(uuid.uuid4())[:8]
    total = sum([int(i) if i.isdigit() else int(ord(i)) for i in list(random_str)])
    seed = chr(total) if total > 127 else chr(total) + chr(total)
    symbol = seed + mark_up + str(rule_id)
    encrypt_symbol = aes.get_encrypt_hex(symbol)
    return random_str, encrypt_symbol


def combine_result(encrypt_symbol, random_str):
    res = []
    for j in range(16):
        index = j // 2
        if j % 2 == 0:
            res.append(encrypt_symbol[index])
        else:
            res.append(random_str[index])
    return ''.join(res)


def write_txt_batch(exchange_ids, file_name):
    base_dir = '/home/apple/projects/PycahrmProjects/wow_script/tests/redpacket/encode01txt/{}.txt'
    with open(base_dir.format(file_name), 'a') as master:
        master.writelines(exchange_ids)


def generate_promotional_code(rule_id, total, mark_up, save_name):
    r = redis.StrictRedis(
        host='127.0.0.1',
        port=6379,
        password='')
    start = datetime.datetime.now()
    exchange_ids = []
    for i in range(total):
        while True:
            random_str, encrypt_symbol = generate_with_rule_id(rule_id, mark_up)
            if r.sadd('redpacket' + encrypt_symbol, random_str):
                exchange_id = combine_result(encrypt_symbol, random_str)
                exchange_ids.append('{}\n'.format(exchange_id))
                break
            if len(exchange_ids) > 10000:
                write_txt_batch(exchange_ids, save_name)
                exchange_ids = []
    if len(exchange_ids) > 0:
        write_txt_batch(exchange_ids, save_name)
    end = datetime.datetime.now()
    print('total cost {}'.format(end - start))
