# -*- coding: UTF-8 -*-
import scrapy
from scrapy import FormRequest,Request
from scrapy.spidermiddlewares.httperror import HttpError
import sys  
reload(sys)  
import json
sys.setdefaultencoding('utf8')   


class TeacherSpider(scrapy.Spider):
  name = "teacher"
  allowed_domains=["login.51talk.com"]
  start_urls=["https://www.51talk.com/reserve/upcourse/155890814"]
  get_course_new_url = "https://www.51talk.com/ajax/getCourseNew"
  login_url = "https://login.51talk.com/ajax/login"
  login_cookies ={
    "uuid": "3618b921c77f2687074db74519537aff",
    "SpMLdaPx_uuid": "4634820150",
    "global": "fec411e4-959d-4b11-b722-c1fee2f031ca",
    "NTKF_T2D_CLIENTID": "guest86A6A7E1-B0C8-45DC-70B2-FA038F8FC0F0",
    "uuid": "eyJpdiI6Ik55UTh4bjJONFJGdzR6cmRubXVkbWc9PSIsInZhbHVlIjoiRFZpZW5IWkxsNHJVNGpNNWNDRhvSzJaUDRBclJqRERjS1wvMVJwd1l2cU10RWNYek1BaUJPTGxlRjlvUU54a1QiLCJtYWMiOiJjMWM5Mzk2OTEyNDU0NzM1YTU5M2I3M2JjYzI3NTUzZWVjNmMxMzEzMTExOWJkODNjMWJhNDA1ZTIwNTFlM2E4In0=",
    "unique_id": "5ab18bc54e61c55a783e7c284e67dc62",
    "__utma": "108070726.1219921113.1533194769.1534315320.1534320912.7",
    "__utmz": "108070726.1534320912.7.5.utmcsr=51talk.com|utmccn=(referral)|utmcmd=referral|utmcct=/",
    "ust_v": "1",
    "user_tk_checkFg": "1",
    "SpMLdaPx_sid": "7812914912",
    "servChkFlag": "sso",
    "www_ugroup": "4",
    "user_ust": "I+0RRTHmXM1zuffuF53FtsmbLvKAmyV9fqrcc900nDHKy7gRmztvzEljnx0VY9TNwkBNDwubfes/TfHFG0kMAWGo8H4wWXvCH9wHtp0=",
    "user_usg": "MC0CFQDWFx3Ek2F8cpB3cYoU0UgCLWa/+wIUROoHfG/sc8VbX3f7UEzfRSLLFk0=",
    "visitid": "10CF479F0F91066A073C0E2E57B9E211NNDTAF30MYTWEx1rNMzjMAO0O0Ox",
    "SpMLdaPx_poid": "499",
    "SpMLdaPx_pvid": "1534484186123",
    "Hm_lvt_cd5cd03181b14b3269f31c9cc8fe277f": "1534317161,1534324635,1534484122,1534484186",
    "Hm_lpvt_cd5cd03181b14b3269f31c9cc8fe277f": "153448418"
  }
  class_name_dict = {
    545382:'经典英语青少版 Level 5',
    8594:'经典英语 Level 2',
    8595:'经典英语 Level 3',
    8770:'经典英语 Level 4',
    8771:'经典英语 Level 5',
    8899:'经典英语 Level 6',
    324263:'青少全能新概念',
    319781:'自然拼读',
    24:'商务英语・Business English Conversation',
    6961:'面试口语・Interview English',
    27:'新学科英语・New Subject English',
    28:'雅思口语・IELTS Speaking',
    440871:'分级阅读 Leveled Reading',
    23:'综合英语・Comprehensive English',
    29:'自由会话・Freetalk【适合中高级水平学员】',
    328323:'生活口语',
    328553:'旅游英语'
  }
  print class_name_dict[328553]
  # class_id=[545382,8594,8595,8770,8771,8899,324263,319781,24,6961,27,28,440871,23,29,328323,328553]
  class_id=[8594,328553]


  def start_requests(self):
    for cid in self.class_id:
      yield scrapy.FormRequest(url=self.get_course_new_url,formdata={
          'course_id':str(cid),
          'appoint_course_id':'8818'
        },callback=self.get_class_info,errback=self.errback,method='post',cookies=self.login_cookies)


  def get_class_info(self,response):
    json_class = json.loads(response.text.decode('ascii'))
    json_data = json_class['data']
    for key in json_data:
      if len(json_data[key]['children']) > 0:
        print '-------------------'+json_data[key]['name']+'-------------------'
        clss = json_data[key]['children']
        for c in clss:
          print c['name']
        print '------------------- end -------------------\n\n'
      else:
        print json_data[key]['name']

    # print json_class['data']

  def errback(self,failure):
    print '>>>>>>>>>>>>>>>request error'
    print failure


  def parse_login(self,response):
    print response.body