from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join, Compose


class NewsLoader(ItemLoader):
    """通用Loader"""
    # 定义通用的方法，对item数据的每个键存值的时候，使用类似extract_first()的方法取出列表中的第一个值
    # 配合response解析函数中ItemLoader的add_xpath使用
    default_output_processor = TakeFirst()


class ChinaLoader(NewsLoader):
    """数据处理loader"""
    # 定义字段，处理item数据
    # 针对item中定义的item键值，定义处理的方法
    # 名称格式，item键名_out
    text_out = Compose(Join(), lambda s: s.strip())
    source_out = Compose(Join(), lambda s: s.strip())