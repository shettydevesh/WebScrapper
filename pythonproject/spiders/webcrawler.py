import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess
import os

global res
res = []

class WebcrawlerSpider(scrapy.Spider):
    name = 'webcrawler'
    custom_settings = {"FEEDS": {"results.csv": {"format": "csv"}},'CONCURRENT_REQUESTS': 10}
    headers = {
        'user-agent' :
        'User-Agent: Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)'
        }
    start_urls = [
        'https://www.rottentomatoes.com/top/bestofrt/top_100_action__adventure_movies/']

    try:
        os.remove('results.csv')
        os.remove('movies.xlsx')
    except OSError:
        pass
    
    def parse(self, response):

        container = response.css('.table tr')
        for item in container: 
            try:
                    rank = item.css('td.bold::text').get()
                    title = item.css('a.unstyled.articleLink::text').get().strip()
                    rating = item.css('span.tMeterScore::text').get().replace('\xa0', '')
                    number_of_views = item.css('td.right.hidden-xs::text').get()
                    link = 'https://www.rottentomatoes.com' + item.css('td a.unstyled.articleLink::attr(href)').get()
                    url = item.css('td a.unstyled.articleLink::attr(href)').get()
                    yield response.follow(url, callback=self.parser, meta={'rank': rank, 'title': title, 'rating': rating, 'nov': number_of_views, 'link': link})

            except:
                continue
    def parser(self, response):
        rank = response.meta.get('rank')
        title = response.meta.get('title')
        rating = response.meta.get('rating')
        number_of_views = response.meta.get('nov')
        link = response.meta.get('link')
        n = response.css('div.movie_synopsis.clamp.clamp-6.js-clamp::text').get().strip()

        rug = {
            'Rank': rank,
            'Title': title,
            'Rating': rating,
            'Synopsis': n,
            'Link': link,
            'Number of reviews': number_of_views
        }
        res.append(rug)
        df = pd.DataFrame(res)
        df["Rank"] = pd.to_numeric(df["Rank"]) 
        df.sort_values(by = ['Rank'], ascending = True, inplace=True)
        df.to_excel("movies.xlsx", index=False)
    
    
    
if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(WebcrawlerSpider)
    process.start()