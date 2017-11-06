# dataworks_companyspider
爬取企查宝公司信息(分布式)

使用方法

nohup scrapy crawl qichabao_url > /opt/logs/qichabao_url_1.log 2>&1 &
nohup scrapy crawl qichabao_url > /opt/logs/qichabao_url_2.log 2>&1 &
nohup scrapy crawl qichabao_url > /opt/logs/qichabao_url_3.log 2>&1 &

nohup scrapy crawl qichabao_com > /opt/logs/qichabao_com_1.log 2>&1 &
nohup scrapy crawl qichabao_com > /opt/logs/qichabao_com_2.log 2>&1 &
nohup scrapy crawl qichabao_com > /opt/logs/qichabao_com_3.log 2>&1 &
nohup scrapy crawl qichabao_com > /opt/logs/qichabao_com_4.log 2>&1 &
nohup scrapy crawl qichabao_com > /opt/logs/qichabao_com_5.log 2>&1 &
nohup scrapy crawl qichabao_com > /opt/logs/qichabao_com_6.log 2>&1 &
nohup scrapy crawl qichabao_com > /opt/logs/qichabao_com_7.log 2>&1 &
nohup scrapy crawl qichabao_com > /opt/logs/qichabao_com_8.log 2>&1 &


nohup /opt/company_auto_input/redis_input.sh /opt/logs/redis_input.log 2>&1 &




###金融公司获取列表网站
中国保险监督管理委员会: http://www.circ.gov.cn/tabid/5254/Default.aspx <br>
中国银行业监督管理委员会: http://www.cbrc.gov.cn/chinese/jrjg/index.html <br>
中国证券监督管理委员会: http://fund.csrc.gov.cn/web/sales_show.organization?type=1

使用的xpath表达式是: <br>
//table[@bgcolor="#8197A3"]//tr[position()>1]/td[2]

//*[@id="ess_ctr16712_OrganizationList_rptCompany"]//a/text()

//*[@id="ess_ctr16713_OrganizationList_rptCompany"]//a/text()

//*[@id="ess_ctr16714_OrganizationList_rptCompany"]//a/text()

//*[@id="ess_ctr16715_OrganizationList_rptCompany"]//a/text()

//*[@id="ess_ctr16716_OrganizationList_rptCompany"]//a/text()

//*[@id="ess_ctr16720_OrganizationList_rptCompany"]//a/text()

//*[@id="ess_ctr26624_OrganizationList_rptCompany"]//a/text()
