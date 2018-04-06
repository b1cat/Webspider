from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from WebSpider.pipelines import WebspiderPipeline



# 运行爬虫
settings = get_project_settings()
process = CrawlerProcess(settings=settings)

process.crawl("Web")

process.start()

# 导出文件为 Webspider.json
pipeline = WebspiderPipeline()
pipeline.export()