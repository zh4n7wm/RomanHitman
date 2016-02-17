#!/usr/bin/env python
# encoding: utf-8
import os
import magic
import base64
import lzma
from datetime import datetime
import re
import uu
import sys
import gzip
"""
gist: https://gist.github.com/zealic/38510fd8ecd1be75924a
zhihu: https://www.zhihu.com/question/28582088
"""


def get_content(fname):
    # import requests
    # gist_url = 'https://gist.github.com/zealic/38510fd8ecd1be75924a/raw/87260ec7f785bd869289387640a8b0356c59b9f5/Roman%2520Hitman'
    # data = requests.get(gist_url).content
    with open(fname) as f:
        data = f.read()
    return data


def b64decode(data):
    return base64.b64decode(data)


def save_to_file(fname, data):
    with open(fname, 'wb') as f:
        f.write(data)


def check_file_type(data):
    return magic.from_buffer(data)


def lzop_decompress(fname):
    # lzo.decompress(data)
    os.system('lzop -fd %s' % fname)
    de_fname = os.path.splitext(fname)[0]
    # data = open(de_fname).read()
    data = ''.join(open(de_fname).readlines()[2:]).strip()
    os.remove(de_fname)
    os.remove(fname)
    return data


def lzma_decompress(data):
    return lzma.decompress(data)


def caesar_decode(data, num=47):
    res = ''
    for x in data:
        x = chr(x)
        if x in (' ', '\n'):
            tmp = x
        elif 32 <= (ord(x) + num) <= 126:
            tmp = chr(ord(x) + num)
        else:
            tmp = chr(ord(x) - num)
        res += tmp

    return res


def get_group_number(data):
    text = re.findall(r'Group number.*\((.*)\).*', data)[0].split()
    group_number = ''
    for x in text:
        if x[0] == 'D':
            group_number += str(int(x[1:]))
        elif x[0] == 'O':
            group_number += str(int(x[1:], 8))
        elif x[0] == 'B':
            group_number += str(int(x[1:], 2))

    return group_number


def fib(n):
    if n == 0:
        return 0
    if n <= 2:
        return 1
    return fib(n - 1) + fib(n - 2)


def get_q1_answer():
    """The answer to life, the universe, and everything?
    """

    return 42


def get_q2_answer():
    return fib(10)


def get_q3_answer():
    """XXX sensitive day and datetime now format
    """
    return datetime(1989, 6, 4).strftime('%m%d') + \
        datetime.now().strftime('%d%M')


if __name__ == '__main__':
    in_file = 'Question.txt'
    out_file = 'questions.bin'
    uu.decode(in_file, out_file=out_file, mode='wb')
    data = open(out_file).read()
    data = lzma_decompress(data)
    data = base64.b64decode(''.join(data.split('\n')[2:]))
    save_to_file(out_file, data)
    data = gzip.open(out_file).read()
    os.remove(out_file)
    question = caesar_decode(data)
    group_number = get_group_number(question)
    verify_code = 'Z%s%s%s' % (get_q1_answer(), get_q2_answer(), get_q3_answer())
    print(question)
    print('QQ group number: %s' % group_number)
    print('QQ verify code: %s' % verify_code)
    # print('抱歉，群主不让说。。')
