from scrapy import signals
from scrapy import Spider
import datetime
import logging
import csv

contracts_by_month = {1: 'F', 2: 'G', 3: 'H', 4: 'J', 5: 'K', 6: 'M', 7: 'N', 8: 'Q', 9: 'U', 10: 'V', 11: 'X', 12: 'Z'}


class QuotesSpider(Spider):
    name = "cboe"

    def __init__(self):

        self.month_int = datetime.date.today().month
        self.year_int = datetime.date.today().year
        self.base_url = 'http://www.cboe.com/delayedquote/advanced-charts?ticker='
        self.data = {}

        self.tickers = [
            'VIX',
            'VXST',
            'VIX3M',
            'VVIX',
            'VXMT'
        ]

        # Get front months
        front_months = self.get_front_month_names()

        # Attach front months
        for ticker in front_months:
            self.tickers.append(ticker)
            pass

        # Create URLs
        urls = self.create_urls(tickers=self.tickers)

        self.start_urls = urls

        pass

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(QuotesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        print ('||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||')
        self.write_to_file()

        pass

    def get_front_month_names(self):

        current_month = self.month_int
        current_year = self.year_int

        one_month = current_month + 1
        two_month = one_month + 1

        con_length = len(contracts_by_month)

        contracts = []

        months = [one_month, two_month]

        y = current_year

        for x in months:

            # If Month increments out of year
            if x > len(contracts_by_month):
                x = x - con_length
                y = current_year + 1
                pass
            pass

            # Amend year
            y = y % 10

            contracts.append('VIX/' + str(contracts_by_month.get(x)) + str(y))

            pass

        return contracts

    def parse(self, response):

        ticker = response.url.split("=")[-1]

        data = response.css('div.meta span::text').extract_first()

        price = float(data.strip())

        self.data[ticker] = price

        pass

    def create_urls(self, tickers):
        urls = []

        for ticker in tickers:
            urls.append(self.base_url + ticker)
            pass

        return urls

    def write_to_file(self):

        # time = datetime.date.today()
        # filename = 'quote-scrape-%s.txt' % time

        with open('../data/quote_scrap.csv', 'w') as csvfile:
            fieldnames = self.tickers

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(self.data)

            print (self.data)

            pass

        pass

    pass
