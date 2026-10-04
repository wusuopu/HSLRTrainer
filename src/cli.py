#!/usr/bin/env python
# encoding: utf-8

import os
import sys

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(ROOT_PATH)

import hsl
import memory

class Application:
    def __init__(self):
        self.pid = None
        self.hProcess = None

    def refresh_process(self):
        if self.hProcess:
            memory.close_process(self.hProcess)
            self.hProcess = None
        if self.pid:
            self.pid = None

        self.pid = hsl.find_game_process()
        if self.pid:
            self.hProcess = memory.inject_process(self.pid)

        if self.pid:
            print("游戏进程: %d" % self.pid)
        else:
            print("游戏未启动")

    def quit(self):
        if self.hProcess:
            memory.close_process(self.hProcess)
            self.hProcess = None
        if self.pid:
            self.pid = None

    def print_help(self):
        print("幻世录重制版物品修改器:")
        print("[h] 显示该帮助信息")
        print("[r] 刷新游戏进程")
        print("[1] 读取金币值")
        print("[2] 设置金币值")
        print("[3] 获取仓库物品")
        print("[4] 修改仓库物品")
        print("[q] 退出程序")

    def run(self):
        self.print_help()
        self.refresh_process()

        while True:
            cmd = input("\n请输入命令: ")
            if cmd == "h":
                print("")
                self.print_help()
            elif cmd == "r":
                self.refresh_process()
            elif cmd == "q":
                self.quit()
                break
            elif cmd == "1":
                if not self.hProcess:
                    print("游戏未启动")
                    continue
                value = hsl.read_money_value(self.hProcess)
                if value is None:
                    print("读取金币值失败")
                else:
                    print("金币值: %d" % value)
            elif cmd == "2":
                if not self.hProcess:
                    print("游戏未启动")
                    continue
                value = input("请输入金币值: ")
                try:
                    value = int(value)
                except Exception as e:
                    print("输入的金币值无效")
                    continue
                if value < 0:
                    print("金币值不能小于0")
                    continue
                hsl.write_money_value(self.hProcess, value)
                print("设置金币值成功")
            elif cmd == "3":
                if not self.hProcess:
                    print("游戏未启动")
                    continue
                materials = hsl.list_warehouse(self.hProcess)
                print("----- 仓库总物品： %d -----" % (len(materials)))
                for i, item in enumerate(materials):
                    print("[%03d] 类型: %04X, 数量: %d" % (i, item['category'], item['count']))
            elif cmd == "4":
                if not self.hProcess:
                    print("游戏未启动")
                    continue
                category = input("请输入物品类型(16进制, 如 010D): ")
                try:
                    category = int(category, 16)
                except Exception as e:
                    print("输入的物品类型无效")
                    continue
                count = input("请输入物品数量: ")
                try:
                    count = int(count)
                except Exception as e:
                    print("输入的物品数量无效")
                    continue
                if count < 0:
                    print("物品数量不能小于0")
                    continue

                materials = hsl.list_warehouse(self.hProcess)
                is_exist = False
                idx = -1
                for item in materials:
                    idx += 1
                    if item['category'] == category:
                        is_exist = True
                        break
                if not is_exist:
                    index = input("请输入要修改的仓库物品索引，如 002: ")
                    try:
                        index = int(index)
                    except Exception as e:
                        print("输入的索引无效")
                        continue
                else:
                    index = idx
                if index < 0:
                    print("索引不能小于0")
                    continue
                hsl.set_warehouse_item(self.hProcess, category, count, index)
                print("修改仓库物品成功")
            else:
                print("未知命令: %s" % cmd)

if __name__ == '__main__':
    app = Application()
    app.run()
