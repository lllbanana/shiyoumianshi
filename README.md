##problem1
###题目描述
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
