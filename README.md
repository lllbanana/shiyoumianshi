problem1
--
一、题目描述
--

外汇牌价查询

这是中国银行外汇牌价网站：https://www.boc.cn/sourcedb/whpj/

请使用python3 和 selenium库写一个程序，实现以下功能：

输入：日期、货币代号

输出：该日期该货币的“现汇卖出价”

示例：

python3 yourcode.py 20211231 USD

输出：

636.99

该日期有很多个价位，只需要输出任意一个时间点的价位即可。

货币代号为USD、EUR这样的三位英文代码，请参考这里的标准符号：https://www.11meigui.com/tools/currency

要求：

1， 将selenium爬到的数据打印到一个result.txt 文件里

2， 代码规范，注释清晰，变量命名合理易读，无不必要的冗余

3，有适当的异常处理

完成后，请将py文件放在一个公开的github repo里

请将repo链接发送至：core@dreamschool.uk

二、代码解释：
--
由于货币种类太多，这里仅实现了如下七种货币：

USD HKD JPY EUR GBP AUD CHF SGD

分别对应：

美元 港元 日元 欧元 英镑 澳大利亚元 瑞士法郎 新加坡元

tips：

1、result.txt文件需要提前创建好；

2、输出会有现汇卖出价，日期，币种三项内容（与原要求不同）；

problem2
--
一、题目描述
--
给你一个字符串，如果一个字符在它前面k个字符中已经出现过了，就把这个字符改成’-’。

比如

Input: abcdefaxc 10

Output abcdef-x-

Input: abcdefaxcqwertba 10

Output abcdef-x-qw-rtb-

二、代码解释
--
题目中的k应该是输入的时候指定的，例如用例为10，即k=10。



