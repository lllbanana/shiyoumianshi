import requests
from lxml import etree
import re
import math

def getRate(dateb,name):
    #key 为币种 value为 中国银行外汇牌价 币种代码 name为对应缩写
    pjcodes = [
        # USD HKD JPY EUR GBP AUD CHF SGD
        {"key": "美元", "value": 1316, "name": "USD" },
        {"key": '港币', "value": 1315, "name": "HKD" },
        {"key": "日元", "value": 1323, "name": "JPY" },
        {"key": "欧元", "value": 1326, "name": "EUR" },
        {"key": '英镑', "value": 1314, "name": "GBP" },
        {"key": "澳大利亚元", "value": 1325,"name": "AUD" },
        {"key": "瑞士法郎", "value": 1317, "name": "CHF" },
        {"key": "新加坡元", "value": 1375, "name": "SGD" },
    ];
    lists = [];
    for pjcode in pjcodes:
        if pjcode['name' ] != name:
            continue

        rate_09 = crow(dateb, dateb, pjcode['key'], None);
        if (len(rate_09)) != 0:
            # print("正在获取"+rate_09[0]+" 汇率")
            rate_dic = {};
            rate_dic['currency'] = rate_09[0];#币种
            rate_dic['rate_xhr'] = rate_09[1];#现汇买入价
            rate_dic['rate_xcr'] = rate_09[2];#现钞买入价
            rate_dic['rate_xhc'] = rate_09[3];#现汇卖出价
            rate_dic['rate_xcc'] =rate_09[4];#现钞卖出价
            rate_dic['rate_zs'] = rate_09[5];#中行折算价
            rate_dic['dateb'] = rate_09[6];#发布时间
            # lists.append(rate_dic);
            # print(rate_09[3])
            # 仅存储现汇卖出价  发布时间  以及货币种类
            lists.append(float(rate_09[3]))
            lists.append(str(dateb))
            lists.append(str(name))
            # lists.append(pjcode['key'])
            with open('result.txt', 'a') as f:
                for list in lists:
                    f.write(str(list) + ' ')
                f.write('\n')
    # print("---------------------------")
    return lists;

# 返回html对象
def getHtml(erectDate, nothing, pjname, page):
    # 定义要传的json  formdata 内容 通过post 请求 拿到 html代码 erectDate开始时间 nothing结束时间  pjname货币代码 page页数 时间一般 开始和结束为同一天
    pyload = {"erectDate": erectDate,
              "nothing": nothing, "pjname": pjname, "page": page, "head": "head_620.js", "bottom": "ottom_591.js"}

    # 定义浏览器头部 防止被拦截
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://srh.bankofchina.com",
        "Referer": "https://srh.bankofchina.com/search/whpj/search_cn.jsp",
        "Upgrade-Insecure-Requests": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "User-Agent": "Mozilla / 5.0(WindowsNT 10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 68.0.3440.106 Safari / 537.36"
    }
    # response = requests.post("http://srh.bankofchina.com/search/whpj/search.jsp", data=pyload, headers=headers)
    response = requests.post("https://srh.bankofchina.com/search/whpj/search_cn.jsp", data=pyload, headers=headers)
    # 转化为html对象
    html = etree.HTML(response.text);
    return (html, response.text)


def crow(erectDate, nothing, pjname, page):
    coutnt = 0;
    if (page == None):
        page = getPageCount(erectDate, nothing, pjname);  # 拿到总页数 只需要抓九点30第一条数据 往往出现在最后一页 所以优先抓最后一页数据
    html = getHtml(erectDate, nothing, pjname, page)[0];
    # 抓取 class 为 BOC_main publish 的talbel 下 所有tr
    datas = html.xpath('//div[@class="BOC_main publish"]/table/tr')
    arr = [];
    for index in range(1, len(datas) - 1):  # 第一个tr 和最后一个tr 无用, 剔除
        ratelist = datas[index].xpath('td')
        tds6 = [];
        for rates in ratelist:
            tds6.append(rates.xpath('text()')[0] if (len(rates.xpath(
                'text()')) != 0) else 0)  # 因为 有些 td里为空, 直接用datas[index].xpath('td/text()') 为空的td 会没有坐标 导致后面数组越界
        if (len(tds6)) != 0:
            if (int(tds6[6][11:13]) == 9 and int(tds6[6][14:16]) >= 30):  # 只要大于九点30的数据
                arr.append(tds6)
            elif (int(tds6[6][11:13]) > 9):
                arr.append(tds6)
    rate_09 = [];
    if (len(arr) != 0):
        rate_09 = arr[len(arr) - 1];  # 只要大于九点30 最小的一条数据 由于排序为倒序  即最后一条 为最小
    if (len(rate_09) == 0):  # 说明 当页未找到 大于九点的数据 需要往下一页查找
        if (page - 1 > 0):
            rate_09 = crow(erectDate, nothing, pjname, page - 1);  # 递归 找到便往上抛
    return rate_09  # 返回九点30最后一条数据 由于排序为倒序,最后一条即为 九点最早的汇率

def getPageCount(erectDate, nothing, pjname):
    html = getHtml(erectDate, nothing, pjname, 1)[1]  # 第一次先抓 总页数
    reg = re.compile(r"(?<=var m_nRecordCount = )\d+")
    match = reg.search(html);
    pageAll = 1;
    if (int(match.group(0)) > 20):  # 每页20条数据 算最大页
        pageAll = math.ceil(int(match.group(0)) / 20);  # 向上取整数
    return pageAll

if __name__ == '__main__':
    # 20211231 USD
    user_input = input("请输入日期和币种（例如20211231 USD）：")
    date=user_input.split(' ')[0]
    index=4
    date = date[:index] + '-' + date[index:]
    index=7
    date = date[:index] + '-' + date[index:]
    # print(date)

    name=user_input.split(' ')[1]
    print(getRate(date,name))
