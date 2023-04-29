import json
import rsa
import requests
import utils
import base64
from aes_pkcs5.algorithms.aes_ecb_pkcs5_padding import AESECBPKCS5Padding


class Jhs:
    def __init__(self):
        self.host = 'dZZmh://xmV.eVdIxthdT.rza'.translate(utils.decoder)
        self.token = ''
        self.nonce = "R8B6l9YbLVlYoRtS"
        self.pubkey = self._get_pub_key()
        self._load_token()

    def _get_pub_key(self):
        url = 'dZZm://eVdIxthdT-Lt-hHr.eVdIxthdT.rza/rztDVWh/yxhT_rztDVW.ehzt'.translate(utils.decoder)
        r = requests.get(url).json()
        return r.get('rsa_public_key', '')

    def _check_login(self):
        url = self.host + '/api/market/auth/getUserInfo'
        r = requests.get(url, params={'token': self.token}).json()
        return r.get('code', 0) != 401

    def _load_token(self):
        try:
            with open('.token', 'r') as f:
                self.token = f.read()
        except FileNotFoundError:
            self.token = ''
        if not self.token or not self._check_login():
            self._login()

    def _login(self):
        print('您的登陆态已失效, 请重新登录')
        phone = int(input('请输入您的手机号: '))
        self._send_sms(phone)
        code = int(input('请输入您收到的验证码: '))
        r = self._login_req(phone, code)
        print(r)
        self.token = r.get('token')
        with open('.token', 'w') as f:
            f.write(self.token)

    def _login_req(self, phone, code):
        url = self.host + '/api/market/auth/login-or-signup'
        data = {
            'phone': phone,
            'code': code,
        }
        r = requests.post(url, params={'token': ''}, data=data).json()
        return r

    def _send_sms(self, phone):
        url = self.host + '/api/market/auth/send-sms'
        r = requests.post(url, params={'token': ''}, data={'phone': phone}).json()
        if r.get('message', '') != 'success':
            raise r
        return

    def _key(self):
        pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(self.pubkey)
        x = rsa.encrypt(self.nonce.encode('utf-8'), pubkey)
        return base64.b64encode(x).decode()

    def _header(self, has_key=False):
        header = {
            'User-Agent': 'eVdIxthdT_Vzh/2.3.5 (rza.eVdIxthdT.xmm; yIVPE:2; Vwc 16.4.1) vPxazDVHT/5.4.4'.translate(
                utils.decoder),
            'Authorization': 'kTxHTH '.translate(utils.decoder) + self.token
        }
        if has_key:
            header['key'] = self._key()
        return header

    def decode(self, msg):
        cipher = AESECBPKCS5Padding(self.nonce, "b64")
        return cipher.decrypt(msg)

    def encode(self, params):
        cipher = AESECBPKCS5Padding(self.nonce, "b64")
        encrypted_text = cipher.encrypt(json.dumps(params))
        return encrypted_text

    def search_card(self, name, rate, pn):
        url = self.host + '/api/market/search/match-product'
        params = {
            'game_key': 'pkm',
            'game_sub_key': 'sc',
            'page': pn,
            'keyword': name,
            # 'rarity': rate,
        }
        return requests.get(url, params=params).json()

    def card_sell_list(self, card_version_id, pn):
        url = self.host + '/api/market/card-versions/products'
        params = {
            'card_version_id': card_version_id,
            'condition': "1",
            'game_key': 'pkm',
            'game_sub_key': 'sc',
            'page': pn,
        }
        return requests.get(url, params=params).json()

    def price_history(self, card_version_id):
        url = self.host + '/api/market/card-versions/price-history'
        params = {
            'card_version_id': str(card_version_id),
            'filter': '1_month',
            'game_key': 'pkm',
        }
        data = {
            'data': jhs.encode(params)
        }
        return requests.get(url, headers=self._header(True), params=data).json()


if __name__ == '__main__':
    jhs = Jhs()
    # resp = jhs.price_history(39038)
    # print(jhs.decode(resp.get('data')))
    # print(json.dumps(jhs.card_sell_list(39038, 1), ensure_ascii=False))
