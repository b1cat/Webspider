import requests
import re
import csv
from bs4 import BeautifulSoup as Soup


s_time = ''
urls_list = datas = []
url = "http://www.nmgepb.gov.cn/ywgl/hjpj/xmslqk/"
csv_header = ["项目名称", "建设地点", "建设单位", "环境影响评价机构", "受理日期", "url"]


def getUrls():
    """
    Getting data after 2015/1/1
    :return: url_list :["201709/t20170921_1548589.html", ... ]
    """

    for num in range(20):

        r = ("" if num == 0 else "_" + str(num))                                           # Generating url

        req = requests.get(url + "index{r}.html".format(r=r))

        urls = re.findall('<a href="./(.*?html)"', req.text)

        if "t2014" in urls[0]:                                                             # Getting data after 2015/1/1
            break

        [urls_list.append(x) for x in urls if "t2014" not in x]

    return urls_list


def getDatas(target):
    """
    Getting data from url
    :param target: Target url : "201709/t20170921_1548589.html"
    :return: list : ['内蒙古胜利矿区胜利西二号露天煤矿', '内蒙古锡林郭勒盟锡林浩特市宝力根苏木伊利勒特嘎查',
                    锡林郭勒盟锡林浩特煤矿', '中煤科工集团北京华宇工程有限公司', '2017年10月9日',
                    'http://www.nmgepb.gov.cn/ywgl/hjpj/xmslqk/201710/t20171009_1548925.html']
    """

    Values = values = []

    URL = re.sub('\/\s+.html', '', url) + target                                            # Splicing target url
    # print(URL)

    req = requests.get(URL)
    soup = Soup(req.content, 'lxml')

    if int(target.split('/')[0]) > 201607:                                                  # Method based on date

        Values = re.findall('<strong>(.*?)</strong>(.*?)<', req.content.decode("utf-8"), re.I)  # Regular datas
        for i in Values[3:-1]:
            values.append(i[1])

    else:

        TB = soup.find("table")                                                             # Find table as object

        for Tr in TB.tr.next_siblings:                                                      # Gets tag contains data
            for Td in Tr:                                                                   # Further acquisition
                if not isinstance(Td, str) != False:                                            # Wipe off type of str
                    [Values.append(x) for x in Td.strings]                                  # Gets data add to list

        values = list(("".join(Values).split()))[-5:]                                       # Gets the required data

        if len(values) < 5:                                                                 # Adopt other table types
            values = Values[-5:]

    datas = {'s_name': values[0], 's_place': values[1], 's_company': values[2], 's_organ': values[3],
             's_time': values[4], 'url': URL}
    print(datas, '\n')

    data = list(dict.values(datas))                                                         # Translate  CSV data types
    # print(data)
    return data


def main():

    urls_list = getUrls()

    with open('内蒙古自治区环评数据.csv', 'w', encoding='utf_8_sig') as f:                   # 以utf_8_sig 编码形式打开文件
                                                                                                    # 防止输出到文件乱码
        csv_writer = csv.writer(f)

        csv_writer.writerow(csv_header)

        for i in urls_list:

            data = getDatas(i)

            csv_writer.writerow(data)


if __name__ == "__main__":
    main()













