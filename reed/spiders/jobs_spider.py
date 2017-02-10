import scrapy

class JobsSpider(scrapy.Spider):
	name = "jobs"
	start_urls = [
	'https://www.reed.co.uk/jobs/it-jobs',
	]

	def parse(self, response):
		for href in response.css('h3.title a::attr(href)').extract():
			yield scrapy.Request(response.urljoin(href), callback=self.parse_detail)
		
		# next page
		next_page = response.xpath('//a[@title=$next]/@href',next = "Go to next page").extract_first()
		if next_page is not None:
			next_page = response.urljoin(next_page)
			yield scrapy.Request(next_page, callback=self.parse)
	
	def parse_detail(self, response):
		def extract_with_css(query, _type = ''):
			# print response.css(query).extract(), '--------------------------------------'
			res = response.css(query).extract()

			if _type == 'salary':
				return res[1].strip()
			elif _type == 'get_first':
				return res[0].strip()
			else:
				return res

		yield {
			'url': extract_with_css('link[rel=canonical]::attr(href)','get_first'),
			'title':extract_with_css('h1[itemprop=title]::text', 'get_first'),
			'date': extract_with_css('div.posted meta::attr(datetime)', 'get_first'),
			'salary': extract_with_css('#content div.description-container div.metadata.hidden-xs > ul:nth-child(2) > li.salary::text', 'salary'),
			'job_description': extract_with_css('div.description'),
			'skills': extract_with_css('li[class*=lozenge]::text'),
		}