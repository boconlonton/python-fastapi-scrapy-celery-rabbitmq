"""Defines scraping logic for UKG domain"""
import json
import requests
import re

from scrapy import Spider

from scrapy.http import FormRequest
from scrapy.http import Request

from ..items import Job


class UkgSpiderSpider(Spider):
    # Metadata
    name = 'ukg_spider'
    allowed_domains = ['ultipro.com']

    # Custom data
    _CLIENTS = {
        157991: {
            'login_url': "https://login.ultipro.com/t/HHA1000HHA/token",
            'client_id': "hha1000candidateimport",
            'client_secret': "XEIftRBsKdYmSQsLpefiyyYnYEnNxfMj"
                             "-D7PIv6joMCxn1eYiYJ3s5A0BHBBriyL"
                             "9DJ7CqJaWjqnqT3vebmajA",
            'start_url': 'https://service5.ultipro.com/talent/recruiting/v2/'
                         'HHA1000HHA/api/opportunities'
        }
    }
    _PAGE = 1
    _PER_PAGE = 20
    _GRANT_TYPE = 'client_credentials'

    def __init__(self,
                 client_id: int,
                 **kwargs):
        super().__init__(**kwargs)
        self.client_id = int(client_id)
        self.access_token = None

    def start_requests(self):
        yield FormRequest(url=self._CLIENTS[self.client_id]['login_url'],
                          method='POST',
                          formdata=self._get_query_string(),
                          callback=self._parse_login)

    def _parse_login(self, response, **kwargs):
        creds = json.loads(response.text)
        self.access_token = creds['access_token']
        yield Request(url=f"{self._CLIENTS[self.client_id]['start_url']}?"
                          f"page={self._PAGE}&per_page={self._PER_PAGE}",
                      headers={
                          'Authorization': f'Bearer {self.access_token}'
                      },
                      callback=self._parse_page)

    def _parse_page(self, response, **kwargs):
        jobs = json.loads(response.text)
        is_published_external2 = False
        if jobs:
            for job in jobs:
                if not job.get('job_boards'):
                    continue
                if len(job.get('job_boards')) == 2:
                    is_published_external2 = job['job_boards'][1][
                        'is_published_external']
                job_rid = job['id']
                job_url = job['job_boards'][0]['recruiting_apply_url']
                if job_url \
                        and (job.get('job_boards')[0][
                                 'is_published_external']
                             or is_published_external2) \
                        and job.get('status') == 'Published':
                    html_raw = requests.get(url=job_url)
                    jsonraw = re.search('CandidateOpportuni'
                                        'tyDetail\\((.+)\\)', html_raw.text)
                    if jsonraw and jsonraw.group():
                        yield Job({
                            'title': job['title']['en_us'],
                            'apply_url': job_url,
                            'rid': job_rid,
                        })
            self._PAGE += 1
            yield Request(
                url=f"{self._CLIENTS[self.client_id]['start_url']}?"
                    f"page={self._PAGE}&per_page={self._PER_PAGE}",
                headers={
                    'Authorization': f'Bearer {self.access_token}'
                },
                callback=self._parse_page)
        return

    def _get_query_string(self):
        return {
            'grant_type': self._GRANT_TYPE,
            'client_id': self._CLIENTS[self.client_id]['client_id'],
            'client_secret': self._CLIENTS[self.client_id]['client_secret'],
        }
