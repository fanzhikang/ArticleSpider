# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import JobBoleArticleItem
from ArticleSpider.utils import common
class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']


    def parse(self, response):
        posts_nodes = response.css('#archive .floated-thumb .post-thumb a')
        for post_node in posts_nodes:
            image_url = post_node.css('img::attr(src)').extract_first("")
            post_url = post_node.css('::attr(href)').extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={'front_image_url': image_url}, callback=self.parse_detail)

        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url,next_url), callback=self.parse)

    def parse_detail(self, response):

        article_item = JobBoleArticleItem()
        # title = response.xpath('//*[@id="post-110287"]/div[1]/h1/text()').extract_first("")
        # create_data = response.xpath('//*[@id="post-110287"]/div[2]/p/text()[1]').extract()[0].strip().replace('·','').strip()
        # praise_nums = response.xpath('//*[@id="110287votetotal"]/text()').extract()[0]
        # fav_nums = response.xpath('//*[@id="post-110287"]/div[3]/div[9]/span[2]/text()').extract()[0]
        # match_re = re.match(".*?(\d+).*", fav_nums)
        # if match_re:
        #     fav_nums = match_re.group(1)
        # comment_nums = response.xpath('//*[@id="post-110287"]/div[3]/div[9]/a/span/text()').extract()[0]
        # match_re = re.match(".*?(\d+).*", comment_nums)
        # if match_re:
        #     comment_nums = match_re.group(1)
        # content = response.xpath('//*[@id="post-110287"]/div[3]').extract()[0]
        # tag_list = response.xpath('//*[@id="post-110287"]/div[2]/p/a/text()').extract()
        # tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        # tags = ",".join(tag_list)



        front_image_url = response.meta.get('front_image_url','')
        title = response.css('.entry-header h1::text').extract_first("")
        create_data = response.css('.entry-meta-hide-on-mobile::text').extract()[0].strip().replace('·','').strip()
        praise_nums = response.css('.vote-post-up h10::text').extract()[0]
        fav_nums = response.css('.bookmark-btn::text').extract()[0]
        match_re = re.match('.*?(\d+).*', fav_nums)
        if match_re:
            fav_nums = int(match_re.group(1))
        else:
            fav_nums = 0
        comment_nums = response.css('a[href="#article-comment"] span::text').extract()[0]
        match_re = re.match('.*?(\d+).*', comment_nums)
        if match_re:
            comment_nums = int(match_re.group(1))
        else:
            comment_nums = 0
        content = response.css('div.entry').extract()[0]
        tag_list = response.css('.entry-meta-hide-on-mobile a::text').extract()
        tag_list = [element for element in tag_list if not element.strip().endswith('评论')]
        tags = ','.join(tag_list)
        article_item['url_object_id'] = common.get_md5(response.url)
        article_item['title'] = title
        article_item['url'] = response.url
        article_item['create_data'] = create_data
        article_item['front_image_url'] = [front_image_url]
        article_item['praise_nums'] = praise_nums
        article_item['fav_nums'] = fav_nums
        article_item['comment_nums'] = comment_nums
        article_item['content'] = content
        article_item['tags'] = tags

        yield article_item
        pass









