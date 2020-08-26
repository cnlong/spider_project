# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, Spider
import json
from weibo.items import UserItem, UserRelationItem, WeiBoItem


class WeibocnSpider(scrapy.Spider):
    name = 'weibocn'
    allowed_domains = ['m.weibo.cn']
    # 不定义start_urls，通过start_request生成
    # start_urls = ['http://m.weibo.cn/']
    # 定义几个微博的Ajax的URL
    user_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&luicode=10000011&containerid=100505{uid}'
    follow_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{uid}&page={page}'
    fan_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{uid}&since_id={id}'
    weibo_url = 'https://m.weibo.cn/api/container/getIndex?containerid=230413{uid}_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03&page={page}'
    # 起始微博用户的ID
    start_users = ['1798590865', '1674166903']

    def start_requests(self):
        for uid in self.start_users:
            yield Request(self.user_url.format(uid=uid), callback=self.parse_user)

    def parse_user(self, response):
        """解析用户详情页的数据"""
        result = json.loads(response.text)
        # 判断是否获取到用户的数据信息
        if result.get('data').get('userInfo'):
            user_info = result.get('data').get('userInfo')
            # 实例化useritem对象
            user_item = UserItem()
            # 通过查看传回的数据信息，可以得知返回的数据中有哪些数据
            # 根据返回数据和自定义的item对象定义一个key-value的字典
            # 便于给user_item进行赋值，key为item中的字段，value为返回数据中的字段
            file_map = {
                'id': 'id', 'name': 'screen_name', 'avatar': 'profile_image_url', 'cover': 'cover_image_phone',
                'gender': 'gender', 'description': 'description', 'fans_count': 'followers_count',
                'follows_count': 'follow_count', 'weibos_count': 'statuses_count',
                'verified': 'verified',  # 是否认证
                'verified_reason': 'verified_reason',  # 认证理由
                'verified_type': 'verified_type'  # 认证类型，-1普通用户，0会员用户
            }
            for key, value in file_map.items():
                user_item[key] = user_info.get(value)
            # 当然也可以逐一赋值，但是如果属性过多，就显得代码臃肿
            # user_item['id'] = user_info.get('id')
            yield user_item
            # 根据用户详情页捕获的用户id，生成其关注列表、粉丝列表、微博的request
            uid = user_info.get('id')
            yield Request(self.follow_url.format(uid=uid, page=1), callback=self.parse_follows,
                          meta={'page': 1, 'uid': uid})
            yield Request(self.fan_url.format(uid=uid, since_id=1), callback=self.parse_fans,
                          meta={'since_id': 1, 'uid': uid})
            yield Request(self.weibo_url.format(uid=uid, page=1), callback=self.parse_weibos,
                          meta={'page': 1, 'uid': uid})

    def parse_follows(self, response):
        """关注用户数据解析"""
        result = json.loads(response.text)
        # 判断是否获取到数据,从多个维度进行判断
        # 返回的关注数据中，会有多个组，查看网页，最后一个组才是用户的关注列表
        if result.get('ok') and result.get('data').get('cards') and len(result.get('data').get('cards')) and result.get('data').get('cards')[-1].get('card_group'):
            # 获取关注用户列表
            follows = result.get('data').get('cards')[-1].get('card_group')
            # 循环遍历关注用户列表，获取用户id，并为每个用户id生成一个新的用户详情request
            for follow in follows:
                # 获取关注用户的用户信息
                if follow.get('user'):
                    uid = follow.get('user').get('id')
                    yield Request(self.user_url.format(uid=uid), callback=self.parse_user)
            # 获取request中传入的详情用户的id
            uid = response.meta.get('uid')
            # 获取关注用户的部分信息，组建成字典，用户用户相关数据的item
            followers = [{'id': follow.get('user').get('id'), 'name': follow.get('user').get('screen_name')} for follow in follows]
            # 将用户的关注用户相关信息存入到item中
            user_relation_item = UserRelationItem()
            user_relation_item['id'] = uid
            user_relation_item['follows'] = followers
            # 因为这里获取的是关注用户列表信息，无法获取到粉丝用户列表信息
            # 暂时将该字段设置为空，后续通过pipeline将其和粉丝解析的数据合并
            user_relation_item['fans'] = []
            yield user_relation_item
            # 叠加page，生成下一页的关注用户列表request
            page = response.meta.get('page') + 1
            yield Request(self.follow_url.format(uid=uid, page=page), callback=self.parse_follows,
                          meta={'uid': uid, 'page': page})

    def parse_fans(self, response):
        """粉丝用户数据解析"""
        result = json.loads(response.text)
        # 判断是否获取到数据,从多个维度进行判断
        # 返回的关注数据中，会有多个组，查看网页，最后一个组才是用户的粉丝列表
        if result.get('ok') and result.get('data').get('cards') and len(result.get('data').get('cards')) and \
                result.get('data').get('cards')[-1].get('card_group'):
            # 获取粉丝用户列表
            fans = result.get('data').get('cards')[-1].get('card_group')
            # 循环遍历关注用户列表，获取用户id，并为每个用户id生成一个新的用户详情request
            for fan in fans:
                # 获取关注用户的用户信息
                if fan.get('user'):
                    uid = fan.get('user').get('id')
                    yield Request(self.user_url.format(uid=uid), callback=self.parse_user)
            # 获取request中传入的详情用户的id
            uid = response.meta.get('uid')
            # 获取关注用户的部分信息，组建成字典，用户用户相关数据的item
            faners = [{'id': fan.get('user').get('id'), 'name': fan.get('user').get('screen_name')} for fan
                         in fans]
            # 将用户的关注用户相关信息存入到item中
            user_relation_item = UserRelationItem()
            user_relation_item['id'] = uid
            user_relation_item['follows'] = []
            # 因为这里获取的是粉丝用户列表信息，无法获取到关注用户列表信息
            # 暂时将该字段设置为空，后续通过pipeline将其和关注解析的数据合并
            user_relation_item['fans'] = faners
            yield user_relation_item
            # 叠加page，生成下一页的关注用户列表request
            since_id = response.meta.get('since_id') + 1
            yield Request(self.follow_url.format(uid=uid, since_id=since_id), callback=self.parse_fans,
                          meta={'uid': uid, 'since_id': since_id})

    def parse_weibos(self, response):
        result = json.loads(response.text)
        # 判断获取结果
        if result.get('ok') and result.get('data').get('cards'):
            # 获取微博列表
            weibos = result.get('data').get('cards')
            # 遍历微博列表
            for weibo in weibos:
                # 获取微博信息键值对的数据
                mblog = weibo.get('mblog')
                # 注意返回的微博列表中，会包含一些非微博的数据，需要剔除
                # 获取mblog字段的值，存在即为微博，不存在即不是微博
                if mblog:
                    weibo_item = WeiBoItem()
                    # 定义字典，便于存入item
                    file_map = {'id': 'id', 'attitudes_count': 'attitudes_count', 'comments_count': 'comments_count',
                                'reposts_count': 'reposts_count', 'picture': 'original_pic',
                                'pictures': 'pics', 'source': 'source', 'text': 'text', 'raw_text': 'raw_text',
                                'thumbnail': 'thumbnail_pic', 'created_at': 'created_at'}
                    for key, value in file_map.items():
                        weibo_item[key] = mblog.get(value)
                    # 获取request请求中传入的用户信息参数
                    uid = response.meta.get('uid')
                    weibo_item['user'] = uid
                    yield weibo_item
                    # 生成微博下一页请求
                    page= response.meta.get('page')
                    page = page + 1
                    yield Request(self.weibo_url.format(uid=uid, page=page), callback=self.parse_weibos, meta={'uid': uid, 'page': page})

    def parse(self, response):
        pass
