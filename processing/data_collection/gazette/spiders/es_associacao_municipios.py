from dateparser import parse
import datetime as dt

import scrapy

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class EsAssociacaoMunicipiosSpider(BaseGazetteSpider):
    MUNICIPALITY_ID = '3200000'
    name = 'es_associacao_municipios'
    allowed_domains = ['diariomunicipales.org.br']
    start_urls = ['https://diariomunicipales.org.br/?r=site/edicoes&Edicao_page=1']

    def parse(self, response):
        """
        @url https://diariomunicipales.org.br/?r=site/edicoes&Edicao_page=1
        @returns items 15 15
        @returns requests 1 1
        @scrapes date file_urls is_extra_edition municipality_id power scraped_at
        """
        for gazette_node in response.css('.items tbody tr'):
            url = gazette_node.css('[download]::attr(href)').extract_first()
            date = gazette_node.css('td::text')[1].extract()
            date = parse(date, languages=['pt']).date()
            yield Gazette(
                date=date,
                file_urls=[url],
                is_extra_edition=False,
                municipality_id=self.MUNICIPALITY_ID,
                power='executive',
                scraped_at=dt.datetime.utcnow(),
            )

        css_path = '.pagination .next:not(.disabled) a::attr(href)'
        next_page_url = response.css(css_path).extract_first()
        if next_page_url:
            yield response.follow(next_page_url)
