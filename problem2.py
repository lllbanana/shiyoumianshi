##
# 第二题
#
# 给你一个字符串，如果一个字符在它前面k个字符中已经出现过了，就把这个字符改成’-’。
#
# 比如
#
# Input: abcdefaxc 10
#
# Output abcdef-x-
#
# Input: abcdefaxcqwertba 10
#
# Output abcdef-x-qw-rtb-
##

def replace_chars(input_str, k):
    str_list = list(input_str)
    # 遍历字符串中的每个字符
    for i in range(len(input_str)):
        # 检查当前字符是否在前面的k个字符中出现过
        if str_list[i] in input_str[max(i - k, 0):i]:
            # 如果出现过，则替换为'-'
            str_list[i] = '-'
            # 将列表转换回字符串并返回
    return ''.join(str_list)


# 测试函数
user_input = input("请输入一个字符串: ")
# print("你输入的字符串是:", user_input)
a=user_input.split(' ')[0]
k=user_input.split(' ')[1]
k=int(k)

print(replace_chars(a,k))
# print(replace_chars("abcdefaxc", 10))  # 输出: abcdef-x-
# print(replace_chars("abcdefaxcqwertba", 10))  # 输出: abcdef-x-qw-rtb-