#!/usr/local/bin python
# coding=utf-8
# @Time    : 2018/8/13 下午8:05
# @Author  : lifangyi
# @File    : test_uuid.py
# @Software: PyCharm

import uuid

uuid_buffer=''
for i in range(90):
    uid=str(uuid.uuid4())
    print(uid)

    uuid_buffer=uuid_buffer+uid+'\n'

with open('uuid.txt','w') as f:
    f.write(uuid_buffer)
