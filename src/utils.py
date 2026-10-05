#!/usr/bin/env python
# encoding: utf-8

import ctypes
import struct
import binascii


def float_to_hex(number):
    """
    将单浮点数转为16进制
    """
    return struct.unpack('<I', struct.pack('<f', number))[0]


def double_to_hex(number):
    """
    将双浮点数转为16进制
    """
    return struct.unpack('<Q', struct.pack('<d', number))[0]


def hex_to_float(hex_number):
    """
    将16进制转为单浮点数
    """
    return struct.unpack('<f', struct.pack('<I', hex_number))[0]


def hex_to_double(hex_number):
    """
    将16进制转为双浮点数
    """
    return struct.unpack('<d', struct.pack('<Q', hex_number))[0]


def bytes_to_int(b, size=4, unsigned=True):
    """
    将字节转为整数
    """
    # char
    f = '<B' if unsigned else 'b'
    if size == 8:       # long long
        f = '<Q' if unsigned else 'q'
    if size == 4:       # int
        f = '<I' if unsigned else 'i'
    if size == 2:       # short
        f = '<H' if unsigned else 'h'
    return struct.unpack(f, b)[0]


def int_to_bytes(i, size=4, unsigned=True):
    """将整数转为字节"""
    # char
    f = '<B' if unsigned else 'b'
    if size == 8:       # long long
        f = '<Q' if unsigned else 'q'
    if size == 4:       # int
        f = '<I' if unsigned else 'i'
    if size == 2:       # short
        f = '<H' if unsigned else 'h'
    return struct.pack(f, i)


def bytes_to_hex_str(buf):
    """
    b'\xAB\xCD' => 'ABCD'
    """
    return binascii.hexlify(buf).decode('utf8')


def hex_byte_to_str(data, coding='gbk'):
    """
    将16进制的字节数据转为字符串
    """
    b = bytes.fromhex(data)
    return b.decode(coding)

def str_to_hex_byte(data, coding='gbk'):
    """
    将字符串转为16进制的字节数据
    """
    b = data.encode(coding)
    r = bytes_to_hex_str(b).upper()
    return ' '.join(r[i:i+2] for i in range(0, len(r), 2))

def hex_byte_to_address(data):
    """
    例： "00 34 61 7F" => "7F613400"
    """
    l = data.split()
    l.reverse()
    return ''.join(l)

def address_to_hex_byte(data):
    """
    例：'7F613400' => '0034617F00'
    """
    if len(data) < 8:
        num = 8
    else:
        num = 16
    r = ((num - len(data)) * '0') + data
    l = [r[i:i+2] for i in range(0, len(r), 2)]
    l.reverse()
    return ''.join(l)


def array_to_list(value):
    """将C Array 转为 python list"""
    data = []
    for v in (value):
        if isinstance(v, ctypes.Array):
            data.append(array_to_list(v))
        else:
            data.append(v)
    return data


def int_array_to_hex_str(arr, size=4):
    """
    ([188, 69], 8) => BC 00 00 00 00 00 00 00 45 00 00 00 00 00 00 00
    """
    l = []
    for i in arr:
        r = bytes_to_hex_str(int_to_bytes(i, size))
        l = l + [r[i:i+2] for i in range(0, len(r), 2)]
    return ' '.join(l).upper()


def convert_power_value_to_hex_str(values, expand=True):
    """
    将 攻击力、防御力、物理命中率、魔击力、魔法命中率、敏捷度、移动力、火抗、水抗、土抗、风抗、心抗 转为十六进制
    """
    if len(values) != 12:
        raise Exception('输入数值个数不对，需要12个数据')

    data = [
        values[1],  # 防御力
    ]
    if expand:      # 两项占位数值
        data.append(0)
        data.append(0)
    data.append(values[5])  # 敏捷度
    data.append(values[6])  # 移动
    data.append(values[0])  # 攻击力
    data.append(values[3])  # 魔击力
    data.append(values[7])  # 火抗
    data.append(values[8])  # 水抗
    data.append(values[10]) # 风抗
    data.append(values[9])  # 土抗
    data.append(values[11]) # 心抗
    data.append(values[2])  # 物理命中率
    data.append(values[4])  # 魔法命中率
    return int_array_to_hex_str(data, 4)


if __name__ == '__main__':
    data = []
    v = int(input("输入攻击力： "))
    data.append(v)

    v = int(input("输入防御力： "))
    data.append(v)

    v = int(input("输入物理命中率： "))
    data.append(v)

    v = int(input("输入魔击力： "))
    data.append(v)

    v = int(input("输入魔法命中率： "))
    data.append(v)

    v = int(input("输入敏捷度： "))
    data.append(v)

    v = int(input("输入移动力： "))
    data.append(v)

    v = int(input("输入火抗： "))
    data.append(v)

    v = int(input("输入水抗： "))
    data.append(v)

    v = int(input("输入风抗： "))
    data.append(v)

    v = int(input("输入土抗： "))
    data.append(v)

    v = int(input("输入心抗： "))
    data.append(v)

    print("转换结果： %s" % convert_power_value_to_hex_str(data))