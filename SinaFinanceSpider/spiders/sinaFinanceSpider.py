#sinaFinanceSpider.py
#! /usr/bin/env python
'''
@author: siyao
'''
from scrapy import Spider
from scrapy import Request
from SinaFinanceSpider.items import SinaFinanceSpiderItem 
import re, os
class sinaFinanceSpider(Spider):
	name = "sinaFinance"
	allowed_domains = ["http://vip.stock.finance.sina.com.cn","money.finance.sina.com.cn"]
	start_urls = [
	"http://money.finance.sina.com.cn/corp/go.php/vDOWN_ProfitStatement/displaytype/4/stockid/600004/ctrl/all.phtml"
    ]
	def __init__(self):
		pass
	def parse(self, response):
		for url in self.url_generator():
			print "------------------------------------"
			print "now industry:", self.current_industry
			print "now stockId:", self.current_stockid
			print "now item:", self.current_finance_item
			print "now url", url
			print "------------------------------------"
			request = Request(url, callback=self.parse_and_save)
			request.meta['save_stock_path'] = self.save_stock_path
			request.meta['finance_item'] = self.current_finance_item
			request.meta['industry'] = self.current_industry
			request.meta['stockid'] = self.current_stockid
			yield request
		#open("test_Profit.execel", "w").write(response.body)

	def parse_and_save(self, response):
		item = TestfiledownloadItem()
		item['industry'] = response.meta['industry']
		item['stockid'] = response.meta['stockid']
		item['finance_item'] = response.meta['finance_item']
		item['url'] = response.url
		file_contents = response.body
		#print file_contents
		item_file_path = os.path.join(response.meta['save_stock_path'], response.meta['finance_item']) + ".xls"
		print item_file_path
		try:
			f = open(item_file_path, "w")
			f.write(file_contents)
		finally:
			f.close
		yield item

	def url_generator(self):
		base_dir = os.path.join("testfiledownload", "spiders")
		listIndustries = os.listdir(os.path.join(base_dir, "urls"))
		for industry in listIndustries:
			self.current_industry = industry
			save_industry_path = os.path.join(os.path.join(base_dir,"finance_db"), self.current_industry)
			os.mkdir(save_industry_path)
			industry_path = os.path.join(os.path.join(base_dir, "urls"), industry)
			stockList = open(industry_path, "r").readlines()


			for stockId in stockList:
				stockId = stockId.strip("\n")
				self.current_stockid = stockId
				self.save_stock_path = os.path.join(save_industry_path, stockId)
				os.mkdir(self.save_stock_path)
				self.current_finance_item = "BalanceSheet"
				yield self.makeBalanceSheetUrl(stockId)
				self.current_finance_item = "CashFlow"
				yield self.makeCashFlowStatementUrl(stockId)
				self.current_finance_item = "ProfitStatement"
				yield self.makeProfitStatementUrl(stockId)

	def makeBalanceSheetUrl(self,stockId):
		'''
		sample url:
		http://money.finance.sina.com.cn/corp/go.php/vDOWN_BalanceSheet/displaytype/4/stockid/600004/ctrl/all.phtml
		'''
		prefix = "http://money.finance.sina.com.cn/corp/go.php/vDOWN_BalanceSheet/displaytype/4/stockid/"
		postfix = "/ctrl/all.phtml"
		stockId = re.sub("\D", "", stockId)
		url = prefix+stockId+postfix
		return url

	def makeCashFlowStatementUrl(self,stockId):
		'''
		sample url:
		http://money.finance.sina.com.cn/corp/go.php/vDOWN_CashFlow/displaytype/4/stockid/600004/ctrl/all.phtml
		'''
		prefix = "http://money.finance.sina.com.cn/corp/go.php/vDOWN_CashFlow/displaytype/4/stockid/"
		postfix = "/ctrl/all.phtml"
		stockId = re.sub("\D", "", stockId)
		url = prefix+stockId+postfix
		return url

	def makeProfitStatementUrl(self,stockId):
		'''
		sample url:
		#http://money.finance.sina.com.cn/corp/go.php/vDOWN_ProfitStatement/displaytype/4/stockid/600004/ctrl/all.phtml
		'''
		prefix = "http://money.finance.sina.com.cn/corp/go.php/vDOWN_ProfitStatement/displaytype/4/stockid/"
		postfix = "/ctrl/all.phtml"
		stockId = re.sub("\D", "", stockId)
		url = prefix+stockId+postfix
		return url

##print makeBalanceSheetUrl("sz00002")
#test = sinaFinanceSpider()
#test.parse("aaa")
