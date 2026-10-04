#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import time

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(ROOT_PATH)
import memory
import utils


BASE_ADDR = 0x7FFC233EB7E0

def find_game_process():
    processes = memory.list_process()

    pid = None
    for item in processes:
        name = os.path.basename(item['name'])
        if name == 'HSLR.exe':
            pid = item['pid']
            break

    return pid


def get_money_address(hProcess):
    """
    获取金币的实际内存地址：
    BASE_ADDR -> B8 -> 100 -> 40
    """

    addr = memory.read_process(hProcess, BASE_ADDR, 8)
    if not addr:
        return None

    addr = memory.read_process(hProcess, addr + 0xB8, 8)
    if not addr:
        return None

    addr = memory.read_process(hProcess, addr + 0x100, 8)
    if not addr:
        return None

    return addr + 0x40


def read_money_value(hProcess):
    """
    读取金币值
    """
    addr = get_money_address(hProcess)
    if not addr:
        return None

    return memory.read_process(hProcess, addr, 4)


def write_money_value(hProcess, value):
    """
    修改金币值
    """
    if value < 0:
        raise Exception('值不能小于0')

    addr = get_money_address(hProcess)
    if not addr:
        return None

    return memory.write_process(hProcess, addr, value, 4)


def get_warehouse_address(hProcess):
    """
    获取仓库开始的内存地址：
    "GameAssembly.dll"+0559B7E0 -> B8 -> 100 -> 68 -> 18 -> 20
    """

    addr = memory.read_process(hProcess, BASE_ADDR, 8)
    if not addr:
        return None

    addr = memory.read_process(hProcess, addr + 0xB8, 8)
    if not addr:
        return None

    addr = memory.read_process(hProcess, addr + 0x100, 8)
    if not addr:
        return None

    addr = memory.read_process(hProcess, addr + 0x68, 8)
    if not addr:
        return None

    addr = memory.read_process(hProcess, addr + 0x18, 8)
    if not addr:
        return None

    return addr + 0x20


def list_warehouse(hProcess, addr=None):
    """
    获取仓库物品
    """

    if not addr:
        addr = get_warehouse_address(hProcess)
    if not addr:
        return None

    ret = []
    value = memory.read_process(hProcess, addr, 4)
    if not value:
        # 仓库为空
        return ret

    i = 0
    while True:
        i += 1
        category = memory.read_process(hProcess, addr + 8 * i, 4)
        count = memory.read_process(hProcess, addr + 8 * i + 4, 4)
        i += 1     # 跳过下一件物品指向占位空间
        if not category or not count:
            break

        ret.append({'category': category, 'count': count})
    return ret


def set_warehouse_item(hProcess, category, count, addr=None, current_materials=None):
    """
    设置仓库指定物品的数量
    """
    if count <= 0:
        raise Exception('值不能小于0')

    if not addr:
        addr = get_warehouse_address(hProcess)
    if not addr:
        return None

    if current_materials is None:
        materials = list_warehouse(hProcess, addr)
    else:
        materials = current_materials

    is_empty = len(materials) == 0
    is_exist = False

    if is_empty:
        index = 0
    else:
        index = 0
        for item in materials:
            if item['category'] == category:
                is_exist = True
                break
            index += 1

    base_addr = addr + 8 + (16 * index)

    if is_empty:
        # 仓库为空则头部指向的第一件物品类型
        memory.write_process(hProcess, addr, category, 4)
    elif not is_exist:
        # 物品不存在，追加
        memory.write_process(hProcess, base_addr - 8, category, 4)
        memory.write_process(hProcess, base_addr, category, 4)

    memory.write_process(hProcess, base_addr + 4, count, 4)


def main():
    pid = find_game_process()
    print("游戏进程： %s" % (pid))

    if not pid:
        return

    hProcess = memory.inject_process(pid)

    print("金币： %s" % (read_money_value(hProcess)))

    # write_money_value(hProcess, 500000)

    materials = list_warehouse(hProcess)
    print("----- 仓库总物品： %d -----" % (len(materials)))
    i = 1
    for item in materials:
        print("[%02d] 物品： %X，数量 ： %d" % (i, item['category'], item['count']))
        i += 1

    set_warehouse_item(hProcess, 0xD4, 2, None, materials)

    memory.close_process(hProcess)


if __name__ == '__main__':
    main()
