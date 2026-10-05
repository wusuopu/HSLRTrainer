#!/usr/bin/env python
# encoding: utf-8

import os
import sys

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(ROOT_PATH)

import hsl
import memory

"""
一些物品的代码：

B9 白光之翼 (全)行动二次
BA 幸运缎带 (全)经验2倍
BB 彩霞的圣石 (全)免疫全部异常状态
BC 黄金的圣杯 (全)金钱2倍
BD 追风之羽 (全)移动距离+1
BE 冥晦之轮 (全)移动后可使用魔法
BF 奥义之证 (全)攻击距离+1
C0 火红水晶 (全)抗火+32%
C1 穹苍之炼 (剑弓祭法翼魔剑)移动距离+1 攻击距离+1 移动后可使用魔法 职业限制：祭师、剑士、魔法师、翼战士、魔剑士
010C 神秘小礼物 神秘商人赠送的小礼物，听说是99999号客人才能获得的极稀有奖品
010D 奥汀徽章 一枚神秘徽章，其由来的古老与神秘，甚至连那位流浪商人也一无所知，唯一的线索便是其表面镌刻的一行古代符文，隐约显现着“致未来的你”

E0 力之源
E1 御之源
E2 魔之源
E3 速之源
E4 土之源
E5 火之源
E6 水之源
E7 风之源
E8 灵之源
E9 会心之素
EA 铁壁之素
ED 通行证
EF 剑之魂
F0 福音之书
F1 圣水晶
F8 染血的披风 <转职道具>染血的披风
F9 法兰克的日志 <转职道具>法兰克的日志
FC 擎的戒指 <转职道具>擎的戒指
FD 仿制的破坏神内核 <转职道具>仿制的破坏神内核
FE 漆黑的羽毛 <转职道具>漆黑的羽毛
100 妖精王的手札 <转职道具>妖精王的手札
"""

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
