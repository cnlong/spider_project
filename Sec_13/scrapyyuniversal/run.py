import sys
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scrapyyuniversal.utils import get_config
from scrapyyuniversal.spiders.universal import UniversalSpider


def run():
    # 提取当前执行的spider名称
    name = sys.argv[1]
    # 提取spider对象的json配置
    custom_settings = get_config(name)
    # 从自定义配置文件中获取使用的Spider名称（字典）
    spider = custom_settings.get('spider', 'universal')
    # 获得setting.py文件中的配置，字典形式返回
    project_settings = get_project_settings()
    settings = dict(project_settings.copy())
    #将json中自定义的配置合并到系统配置
    settings.update(custom_settings.get('settings'))
    # 新建CrawlerProcess类，用于执行爬取任务，传入配置
    process = CrawlerProcess(settings)
    # 向爬取任务对象中传入爬虫，并传入参数以便前面的spider使用
    process.crawl(spider, **{'name': name})
    # 启动爬虫
    process.start()


if __name__ == '__main__':
    run()

