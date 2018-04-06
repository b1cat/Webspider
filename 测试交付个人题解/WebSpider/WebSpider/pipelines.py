# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from WebSpider.spiders.Web import GetPath
import json


class WebspiderPipeline(object):
    def process_item(self, item, spider):
        return item

    def export(self):
        """
           Export data
        :return: Webspider.txt
        """
        data = {}
        # 导入路径组和body
        getdata = GetPath()
        [paths, bodys] = getdata.mydatas()

        try:
            for path in paths:
                for index in range(len(path)):
                    # 生成需要的数据格式
                    data[path[index]] = dict(body=bodys[path[index]], children=path[index+1:], parents=path[:index])


        except:
            pass

        # 导出文件为 Webspider.json
        json_data = json.dumps(data, ensure_ascii=False)
        print(json_data)
        with open("Webspider.json", 'w', encoding='utf_8_sig') as f:
            f.write(json_data)


