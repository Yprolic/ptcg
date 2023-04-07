import requests
import utils


class Jhs:
    def __init__(self):
        self.host = 'dZZmh://xmV.eVdIxthdT.rza'.translate(utils.decoder)

    def get_min_price(self, name, rate):
        url = self.host + '/api/market/search/match-product'
        params = {
            'game_key': 'pkm',
            'game_sub_key': 'sc',
            'page': 1,
            'keyword': name,
        }
        return requests.get(url, params=params).json()


if __name__ == '__main__':
    jhs = Jhs()
    print(jhs.get_min_price('莉莉艾', 'ur'))
