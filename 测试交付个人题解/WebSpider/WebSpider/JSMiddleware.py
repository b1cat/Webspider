from selenium import webdriver
from scrapy.http import HtmlResponse


class JSMiddleware(object):

    def process_request(self, request, spider):
        """
           根据request 携带的标志解析JS
        :param request:
        :param spider:
        :return: HtmlResponse
        """

        if 'PhantomJS' in request.meta.keys():
            try:
                driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])  # 容错
                driver.implicitly_wait(10)  # 隐试等待10s
                driver.get(request.url)

                flag = request.meta['flag']  # request 携带的JS代码
                driver.execute_script(flag)  # 执行JS
                body = driver.page_source
                # print(body)

                html = HtmlResponse(driver.current_url, encoding="utf-8", body=body, request=request)
                driver.quit()  # 断开
                return html

            except:
                return
