import random
import time

import requests
import json
from hashlib import sha1
import utils


class PtcgApi():
    def __init__(self):
        self.host = 'dZZmh://xmm-xmV.mzgTazt-ZrW.rt'.translate(utils.decoder)
        self.salt = 'hORbovb2heDpEfspDYEQEXhdkisaiUUIkZVkewZk'.translate(utils.decoder)

    def _sign(self):
        ts = str(int(time.time()) * 1000 - 24 * 3600 * 1000)
        nonce = '{:0>6d}'.format(random.randint(0, 999999))
        sign = sha1((ts + nonce + self.salt).encode()).hexdigest()
        return {
            'timestamp': ts,
            'signature': sign,
            'nonce': nonce,
            # TODO 抓个查一下
            # 'api-access-token': '123',
        }

    def get_card_list(self, tp):
        # req = {"pageNum": 1, "pageSize": 50, "commoditySelectedList": [selected[tp]],
        #        "commodityIds": str(selected[tp]["id"]),
        #        "banCardFlag": 0}
        url = self.host + "/app-api/v1/app/card/query"
        resp = requests.post(url=url, json={}, headers=self._sign()).json()
        if resp.get('code') != 0:
            raise resp.get('message')
        return resp.get('data')

    def get_card_detail(self, card_id):
        url = self.host + '/app-api/v1/app/card/get?id={}'.format(card_id)
        resp = requests.get(url=url, headers=self._sign()).json()
        print(resp)
        if resp.get('code') != 0:
            raise resp.get('message')
        return resp.get('data')

    def get_coll_list(self):
        url = self.host + '/app-api/v1/app/card/queryCollectionList'
        resp = requests.get(url, headers=self._sign()).json()
        return resp


if __name__ == '__main__':
    pass
