# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TeacherspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # 姓名
    name = scrapy.Field()
    # 被收藏次数
    collectTimes = scrapy.Field()
    # 被评价次数
    appraiseTimes = scrapy.Field()
    # 教龄
    teachYears = scrapy.Field()
    # 适合学员
    suitableStudents= scrapy.Field()
    # 擅长
    skilledIn= scrapy.Field()
    # 自我介绍 英文
    inteoduceEnglish= scrapy.Field()
    # 自我介绍 中文翻译
    inteoduceChinese= scrapy.Field()
    # 头像地址
    avatar= scrapy.Field()
    pass
