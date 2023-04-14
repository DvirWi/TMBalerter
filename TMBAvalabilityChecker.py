from datetime import datetime, timedelta
import requests
import re
import json
from typing import List

SITE_URL = "https://etape-rest.for-system.com/"
ENDPOINT_INDEX = "index.aspx"
REF_PARAMETER_VALUE = "json-planning-refuge"
DATETIME_FORMAT = '%Y-%m-%d'
RESPONSE_ENCODING = 'UTF-8'


class TMBAvalabilityChecker(object):
    def __init__(self, refugee_id: int, date: datetime, num_of_guests: int = 2, days_range: int = 0):
        self.refugee_id = refugee_id
        self.date = date
        self.num_of_guests = num_of_guests
        self.days_range = days_range
        self.get_url = f"{SITE_URL}/{ENDPOINT_INDEX}?ref={REF_PARAMETER_VALUE}&q={self.refugee_id},{self.date.strftime(format=DATETIME_FORMAT)}"

    def _parse_response(self, content: bytes):
        return json.loads(re.search("\\(.*", content.decode(RESPONSE_ENCODING))[0][2:-2])['planning']

    def refine_response_to_desired_dates(self, json_response: dict):
        return [entree for entree in json_response if abs(entree['d']) <= abs(self.days_range)]

    def _extract_avaliable_dates(self, json_response: dict):
        refined_json_response = self.refine_response_to_desired_dates(json_response)
        return [self.date - timedelta(days=entree['d']) for entree in refined_json_response if entree['s'] >= self.num_of_guests]

    def check(self) -> List[datetime]:
        response = requests.get(self.get_url)
        return self._extract_avaliable_dates(self._parse_response(response.content))
