# -*- coding: utf-8 -*-
import re
import scrapy

"""
  Paths 用于记录页面完整路径二维数组，默认入口页面url为起始父页面url，每次添加子页面的url到数组
  Bodys 用于记录页面url与body的字典
"""
Paths = [['http://127.0.0.1:8080/main.html']]
Bodys = {}


class WebSpider(scrapy.Spider):
    name = 'Web'
    allowed_domains = ['127.0.0.1']
    start_urls = ['http://127.0.0.1:8080/main.html']  # 如需修改，请一同修改Paths 变量

    def parse(self, response):

        # print(response.url + "==========+++=======")
        body = response.xpath('//body').extract()
        Bodys[response.url] = body[0]  # 向Bodys 添加页面url与body

        metas = response.meta  # 获取从request 发起的JS 标志
        if 'flag' in metas.keys():  # 获取发起JS 请求的url

            print(metas['req_url'])
            JSurl = GetPath()
            JSurl.foxc(metas['req_url'], response.url)  # 更新路径

        for href in response.xpath('//a/@href').extract():  # 获取子页面的超链接
            if href is not None:
                url = response.urljoin(href)  # 将相对路径换为绝对路径
                NewURL = GetPath()
                NewURL.foxc(response.url, url)  # 更新路径

                request = scrapy.Request(url, callback=self.parse)

                try:
                    """
                      若页面以JavaScript做页面跳转，则获取JS代码 并设置为JS的标志
                      以webdrive + phantomjs 发起JS请求
                    """
                    flag = re.findall("javascript: (.*?);", body[0])[0]
                    if flag:

                        request.meta['req_url'] = request.url
                        request.meta['flag'] = flag
                        request.meta['PhantomJS'] = True
                        request.dont_filter = True  # 由于二次请求会过滤重复url，这里设为不过滤

                except:
                    pass

            yield request  # 爬取


class GetPath():
    """
      用于获取页面完整路径的类
      期望获取的为一条路径完整序列数组构成的数组
      :return [[mian.html, p1l1.html, p2l1.html,...], [main.html, p2l1.html, p2l2.html....] ..... ]
    """

    def __init__(self):
        """
        Paths 由多条路径构成二维数组，用于记录页面完整路径
        每条路径的前一个都是后一个的父页面url，同样后一个都是前一个的子页面url
a        """
        global Paths

    def compare(self, List, url, child):
        """
           当前父页面的url与路径中最后一位的相比，若相等，直接在路径后面添加子页面的url
           若和最后一位的前一位url相等，则新增一条路径，即用子页面url替换原路径的最后一位

        :param List: 路径组里的一条路径
        :param url: 父页面的url
        :param child: 子页面的url
        :return: 添加（更新）子页面url的一条路径
        """
        if child in List:  # 去重
            return

        try:
            if List[-1] == url:
                List.append(child)

            elif List[-2] == url:
                new_list = List[:-1]
                new_list.append(child)
                Paths.append(new_list)

        except:
            pass

    def foxc(self, current_url, current_child):
        """
            用于获取页面完整路径的方法
        :param current_url:   父页面的url
        :param current_child: 子页面的url
        :return:  添加到路径数组 Paths
        """
        for i in range(len(Paths)):
            self.compare(Paths[i], current_url, current_child)

    def mydatas(self):
        """
           用于提供输出的数据
        :return: Paths, Bodys
        """
        return Paths, Bodys
