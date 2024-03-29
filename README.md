# 目標
以 python 實現子網段計算小工具

# 計算子網路方法
[參考連結1](https://bluemuta38.pixnet.net/blog/post/45543389)

[參考連結2](https://github.com/tehmaze/ipcalc/blob/master/ipcalc.py)

假設某處 ip 地址為 `140.113.215.35`，想要配置 30 台主機 ip，那我們的主機 bit 數為 5 個 bits，這樣才可以配置夠 30 台，也可以 log2(30) 取上高斯(floor)得 5 bits。

`32 bits = 27 網路 bits + 5 主機 bits`

所以我們可以求得 subnet mask 為
```
     255 .      255 .      255 .      224
11111111 . 11111111 . 11111111 . 11100000
------------------------------------*****
                                    ^---^
                                     Host
```

我們可以從某主機 IP 及 配置數得知子網路遮罩，反之，我們也可以從子網路遮罩就告訴我們此網段的配置主機個數，只要知道
* 某台 ip
* 子網路遮罩
就可以推算出此網段的所有主機 ip 及個數

最後，怎麼求 Network ID，Host ID 呢 ? 也很簡單:

```
Network ID = IP & mask  (主機 bit 全設成 0，代表的是一個網段，為網路地址)
Host ID    = IP & ~mask (主機 bit 全設成 1，代表是廣播地址)
```

舉個例子:  已知某主機IP為 `140.113.215.41`，子網路遮罩為 `255.255.255.224`

1. 求 Network ID
```
   10001100.01110001.11010111.00101001
&) 11111111.11111111.11111111.11100000
---------------------------------------------
   10001100.01110001.11010111.00100000
        140.     113.     215.      32
```

```
10001100.01110001.11010111.00100000 (140.113.215.32) 網路地址
10001100.01110001.11010111.00111111 (140.113.215.63) 廣播地址
之間的範圍 IP 為所有子網路的 IP
```

2. 求 Host ID
先將 subnet Mask 做 NOT 運算，可以得出主機 bit 遮罩
```
00000000.00000000.00000000.00011111
```

然後再和 IP 做 AND 運算，就可以得到 Host ID，以`140.113.215.41`為例
```
   10001100.01110001.11010111.00101001
&) 00000000.00000000.00000000.00011111
---------------------------------------------
   00000000.00000000.00000000.00001001
          0.       0.       0.       9
```


換成十進位就成 : 0.0.0.9。表示是該網域從 .32 開始數第 9 個數字，所以為網段第 9 個 IP
(32, 33, 34, 35, 36, 37, 38, 39, 40, 41...)

所以可配置主機IP為 140.113.215.33 ~ 140.113.215.62，都屬於同一個網段，所以 140.113.215.(33~62) / 27 結果都相同

----
其實我們只要知道下面其中一項
* 其中一台主機的 IP 跟 子網路遮罩
* 其中一台主機的 IP 跟 該網段配置主機個數

我們可以求得網段的所有IP跟地址範圍、主機個數 
酷吧 😆😆😆

## 問題
已知 ip = 140.113.215.56, subnet mask = 255.255.255.224，求同網段 ip 範圍及主機個數，Host ID

```
1. 由 subnet mask 知 總共有 32 - 2 (網路、廣播) 個主機，表示法為 140.113.215.56 / 27(網路地址 bit 數)
2. ip & mask = 140.113.215.32 為網路地址，140.113.215.63(後主機bits全1) 為廣播地址。 
3. 所以合法 ip 為 140.113.215.33 ~ 140.113.215.62
4. Host ID = ip & ~mask = 0.0.0.24，為同網段第24個 IP
```

最後補充
1. `Gateway` 主要功能是用來"連接兩個不同的網段"。也就是說，如果系統判定目的端為不同網段，就會將封包丟給 `Gateway` 來做轉送，反之，如果判定為相同網段，即直接傳到目的端，不會經由 `Gateway`
2. `Subnet mask` 是用來判斷是否為同一個網域，假設 ip_A, ip_B
```
net_X = ip_A & mask  
net_Y = ip_B & mask
if net_X == net_Y : same net # (同網路ID  ，不用通過閘道轉送)
else : different net         # (不同網路ID，需要通過閘道轉送)
```

## 範例執行
```bash
sh test.sh
```
