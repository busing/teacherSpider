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
import traceback
from PyPDF2 import PdfFileReader
from scrapy import log
sys.setdefaultencoding('utf8')   


class TeacherSpider(scrapy.Spider):
  stopCrawl = False
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
    # 8594:u'经典英语 Level 2',
    # 8595:u'经典英语 Level 3',
    # 8770:u'经典英语 Level 4',
    8771:u'经典英语 Level 5',
    # 8899:u'经典英语 Level 6',
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
      log.msg('start crawl class '+self.class_name_dict[cid],level=log.INFO)
      if self.stopCrawl:
        log.msg('退出下载',level=log.INFO)
        return
      yield scrapy.FormRequest(url=self.get_course_new_url,formdata={
          'course_id':str(cid),
          'appoint_course_id':'8818'
        },callback=self.get_class_info,errback=self.errback,method='post',cookies=self.login_cookies)


  def get_class_info(self,response):
    json_class = json.loads(response.text.decode('ascii'))
    # log.msg(json_class,level=log.INFO)
    json_data = json_class['data']
    for key in json_data:
      if self.stopCrawl:
        log.msg('退出下载',level=log.INFO)
        return
      tree_parent_id = json_data[key]['tree_parent_id']
      class_name_path = self.class_path+'/'+self.class_name_dict[tree_parent_id]
      self.check_folder(class_name_path)
      if len(json_data[key]['children']) > 0:
        try:
          folder_name = class_name_path+'/'+self.replaceSymbol(json_data[key]['name'])
          self.check_folder(folder_name)
          clss = json_data[key]['children']
          for c in clss:
            if self.stopCrawl:
              log.msg('退出下载',level=log.INFO)
              return
            # log.msg(c['name'],level=log.INFO)
            lession_path=folder_name+'/'+c['name']
            self.check_folder(lession_path)
            fo = open(lession_path+'/info.txt','w')
            fo.write('id:%s\n' % c['id'])
            fo.write('name:%s\n' % c['name'])
            fo.write('student_book:%s\n' % c['student_book'])
            fo.write('student_book_url:%s\n' % (self.book_download_url+c['id']))
            for i in range(0,3):
              fo.write('audio_url:%s\n' % (self.audio_download_url+str(i)+c['id']+'.zip'))
            fo.write('teacher_book:%s\n' % c['teacher_book'])
            fo.write('teacher_book_prefix:%s\n' % c['teacher_book_prefix'])

            pdf_path = lession_path+'/'+c['student_book']
            if self.isValidPDF_pathfile(pdf_path):
              log.msg('%s is exists, skiped ' % pdf_path,level=log.INFO)
              continue
            ## download files
            pdfRequest= Request(
                cookies=self.login_cookies,
                url=self.book_download_url+c['id'],
                callback=self.save_pdf,
                errback = self.save_pdf_err
            )
            pdfRequest.meta['savePath'] = pdf_path
            yield pdfRequest
            time.sleep(2)
            pass
        except BaseException as e:
          log.msg(e.message,level=log.INFO)
      else:
        folder_name = class_name_path+'/'+self.replaceSymbol(json_data[key]['name'])
        self.check_folder(folder_name)
        # log.msg(json_data[key]['name'],level=log.INFO)
    # log.msg(json_class['data'],level=log.INFO)

  def errback(self,failure):
    log.msg('>>>>>>>>>>>>>>>request error',level=log.INFO)
    log.msg(failure,level=log.INFO)


  def parse_login(self,response):
    log.msg(response.body,level=log.INFO)


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
    log.msg('save pdf :'+save_path,level=log.INFO)
    if '您的预览教材数量已超过上限' in response.body:
      self.stopCrawl = True
      log.msg('您的预览教材数量已超过上限,下载失败',level=log.INFO)
      return

    if '登陆' in response.body:
      self.stopCrawl = True
      log.msg('登陆失效,下载失败',level=log.INFO)
      return

    with open(save_path, 'wb') as f:
      f.write(response.body)
    pass

  def save_pdf_err(self,response):
    log.msg('save_pdf_err',level=log.ERROR)


  def isValidPDF_pathfile(self,pathfile):
    bValid = True
    try:
        reader = PdfFileReader(pathfile)
        if reader.getNumPages() < 1:    #进一步通过页数判断。
          bValid = False
    except:
        bValid = False
        log.msg(pathfile+' is not a pdf ',level=log.ERROR)
    return bValid