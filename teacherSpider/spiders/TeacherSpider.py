# coding: utf-8
import scrapy
from scrapy import FormRequest,Request
from scrapy.spidermiddlewares.httperror import HttpError
import os
import re
import time
import sys  
reload(sys)  
import json
sys.setdefaultencoding('utf8')   


class TeacherSpider(scrapy.Spider):
  book_download_url='http://www.51talk.com/download/book?course_id='
  audio_download_url='https://static.51talk.com/upload/efl_audio/zip/talk'
  replace_pattern = '[\\~|\\!|\\@|\\#|\\$|\\%|\\^|\\&|\\(|\\)|\\_|\\+|\\?|\\>|\\<|\u3002]*'
  name = "teacher"
  allowed_domains=["login.51talk.com","www.51talk.com"]
  start_urls=["https://www.51talk.com/reserve/upcourse/155890814"]
  get_course_new_url = "https://www.51talk.com/ajax/getCourseNew"
  login_url = "https://login.51talk.com/ajax/login"
  login_cookies ={
    "price_show_type":"1",
    "remember_user":"y",
    "uuid":"280c8665-8b8b-4a17-a7e1-09798469e305",
    "www_ugroup":"4",
    "ust_v":"1",
    "talk_user_id":"NNDTAF30MYTWEx1rNMzjMAO0O0Ox",
    "SpMLdaPx_uuid":"4492958313",
    "__utma":"108070726.35460673.1532522898.1532522898.1534247745.2",
    "__utmz":"108070726.1534247745.2.2.utmcsr=51talk.com|utmccn=(referral)|utmcmd=referral|utmcct=/",
    "aliyungf_tc":"AQAAACLmNmyXTwQAO/pBMQIMmxQJmcV3",
    "Hm_lvt_cd5cd03181b14b3269f31c9cc8fe277f":"1534754640,1535023092,1535368448,1535439999",
    "SpMLdaPx_sid":"6967973318",
    "PHPSESSID":"4mam4nrv2rjc53h17glm3t2ff5",
    "servChkFlag":"sso",
    "user_ust":"I%2B0RRTHmXM1zuffuF53FtsmbLvKAmyV9fqrcc900nDHKy7gRmztvzElsqLYGIJ5T4ZTr4faiM%2FHJeOYrRyPsejgZ3AUw09sWBFMtrSw%3D",
    "user_usg":"MC0CFFvBD6L7JMU6Tn%2FYsh3GpHy2Scc2AhUAhZ6RRQB8qchpXOFanrP%2FoRSj9W4%3D",
    "visitid":"A02B1018A3E5F5E28252BC10468D1245NNDTAF30MYTWEx1rNMzjMAO0O0Ox",
    "SpMLdaPx_poid":"47",
    "SpMLdaPx_pvid":"1535440010199",
    "Hm_lpvt_cd5cd03181b14b3269f31c9cc8fe277f":"1535440010"
  }
  class_name_dict = {
    8594:u'经典英语 Level 2',
    8595:u'经典英语 Level 3',
    8770:u'经典英语 Level 4',
    8771:u'经典英语 Level 5',
    8899:u'经典英语 Level 6',
    # 324263:u'青少全能新概念',
    # 319781:u'自然拼读',
    # 24:u'商务英语・Business English Conversation',
    # 6961:u'面试口语・Interview English',
    # 27:u'新学科英语・New Subject English',
    # 28:u'雅思口语・IELTS Speaking',
    # 440871:u'分级阅读 Leveled Reading',
    # 23:u'综合英语・Comprehensive English',
    # 328323:u'生活口语',
    # 328553:u'旅游英语'
  }
  # class_name_dict = {
  #   28:u'雅思口语・IELTS Speaking'
  # }
  class_path =u'/Users/taiyuan/Documents/51talkClass'


  def start_requests(self):
    if not os.path.exists(self.class_path):
      os.mkdir(self.class_path)
      pass
    for cid in self.class_name_dict:
      print 'start crawl class '+self.class_name_dict[cid]
      yield scrapy.FormRequest(url=self.get_course_new_url,formdata={
          'course_id':str(cid),
          'appoint_course_id':'8910'
        },callback=self.get_class_info,errback=self.errback,method='post',cookies=self.login_cookies)


  def get_class_info(self,response):
    json_class = json.loads(response.text.decode('ascii'))
    # print json_class
    json_data = json_class['data']
    for key in json_data:
      tree_parent_id = json_data[key]['tree_parent_id']
      fo = open(('%s/%s.txt' % (self.class_path,self.class_name_dict[tree_parent_id])),'a')
      fo.write('-----------'+self.class_name_dict[tree_parent_id]+'-----------\n')
      if len(json_data[key]['children']) > 0:
        try:
          clss = json_data[key]['children']
          fo.write(self.replaceSymbol('['+json_data[key]['name'])+']'+'\n\n')
          for c in clss:
            # print c['name']
            fo.write('id:%s\n' % c['id'])
            fo.write('name:%s\n' % c['name'])
            fo.write('student_book_url:%s\n' % (self.book_download_url+c['id']))
            for i in range(0,3):
              fo.write('audio_url:%s\n' % (self.audio_download_url+str(i)+c['id']+'.zip'))
            fo.write('\n\n')
            pass
        except BaseException as e:
          # print json_data
          print e.message
      else:
        pass
        # print json_data[key]['name']
    # print json_class['data']
  
  def errback(self,failure):
    print '>>>>>>>>>>>>>>>request error'
    print failure


  def parse_login(self,response):
    print response.body


  def replaceSymbol(self,str):
    str = str.strip()
    str= re.sub(self.replace_pattern,'',str)
    str= re.sub(' ','-',str)
    return str


  def check_folder(self,path):
    if not os.path.exists(path):
      os.mkdir(path)


  def save_pdf(self,response):
    save_path = response.meta['savePath']
    print 'save pdf :'+save_path
    with open(save_path, 'wb') as f:
      f.write(response.body)
    pass

  def save_pdf_err(self,response):
    print 'save_pdf_err'