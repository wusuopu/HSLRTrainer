# CE 内存地址分析

GameAssembly.dll -> 0x7ffc1de50000 （需要动态获取）

基础： "GameAssembly.dll"+0559B7E0 = 0x7ffc1de50000 + 0x0559B7E0 = 0x7ffc233eb7e0  
金币地址指针： "GameAssembly.dll"+0559B7E0 -> B8 -> 100 -> 40

## 仓库地址指针

- 首个物品类型(4Bytes)： "GameAssembly.dll"+0559B7E0 -> B8 -> 100 -> 68 -> 18 -> 28
- 首个物品数量(4Bytes)： "GameAssembly.dll"+0559B7E0 -> B8 -> 100 -> 68 -> 18 -> 2C


### 仓库内存结构

```
                            首个物品
下一物品类型                当前物品类型  当前物品数量
XX XX XX XX | FF FF FF FF | XX XX XX XX | XX XX XX XX |                 《-  重复该行内容
00 00 00 00 | 00 00 00 00 | 《- 表示没有物品了
```


物品代码： https://www.bilibili.com/video/BV1FfYY6mE8G/?vd_source=a8c77ce2ed14bce7fd4480e2f0bc9502


## 人物

- HP: 8Bytes
- MP: 8Bytes          ; HP + 0x08
- SP: 2Bytes          ; MP + 0x0C 最大 9999 (0x270f)

```
HP                        MP                        SP  
XX XX XX XX 00 00 00 00 | YY YY YY YY 00 00 00 00 | 00 00 00 00 0F 27 00 00  
```

例子：  
BC 00 00 00 00 00 00 00 45 00 00 00 00 00 00 00 00 00 00 00 0F 27 00 00  
A5 00 00 00 00 00 00 00 87 00 00 00 00 00 00 00 00 00 00 00 0F 27 00 00  

- 防御力  4Bytes 连续
- ???: 00 00 00 00
- ???: 00 00 00 00
- 敏捷度
- 移动
- 攻击力
- 魔击力
- 火抗
- 水抗
- 风抗
- 土抗
- 心抗
- 物理命中率
- 魔法命中率

- 力量  4Bytes 连续
- 反应
- 精神
- 体质

