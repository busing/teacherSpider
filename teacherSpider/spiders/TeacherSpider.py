import scrapy

class TeacherSpider(scrapy.Spider):
  name = "teacher"
  allowed_domains=["51talk.com"]
  start_urls=["https://www.51talk.com/ReserveNew/index"]
  login_url = "https://login.51talk.com/login/index"


  # def parse(self,response):


  # def start_requests(self):


  def login(self,response):
    formdata={
      'username':'13815412201',
      'password':'79134646852'
    }

    yield FormRequest.form_response(response,formdata=formdata,callback=self.parse_login)


  def parse_login(self,response):
    print ('>>>>>>>>>>>>>'+response.text)