import re
import random
import requests

from config import CONFIG

class MailTM:
    def __init__(self) -> None:        
        self.base_url = 'https://api.mail.tm'
        
        with open(CONFIG.PROXY_LIST, 'r', encoding='utf-8') as f:
            self.proxies = f.read().split('\n')

    def get_proxy(self):
        proxy = random.choice(self.proxies)
        
        if proxy == '':
            return None
        elif len(proxy.split(':')) == 2:
            proxy = {
                'http': f'http://{proxy}',
                'https': f'http://{proxy}'
            }
        elif len(proxy.split(':')) == 4:
            user = proxy.split(':')[2]
            password = proxy.split(':')[3]
            ip = proxy.split(':')[0]
            port = proxy.split(':')[1]

            proxy = {
                'http': f'http://{user}:{password}@{ip}:{port}',
                'https': f'http://{user}:{password}@{ip}:{port}'
            }
        else:
            return None

        return proxy
    

    # get mailtm domains
    def get_domains(self):
        url = self.base_url + '/domains'
        rq = requests.get(url, proxies=self.get_proxy())
        data = rq.json()
        
        domain = data['hydra:member'][0]['domain']
        return domain

    def create_account(self, domain: str, password: str):
        url = self.base_url + '/accounts'
        user = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz1234567890') for i in range(15))
        payload = {
            'address': f'{user}@{domain}',
            'password': password
        }
        rq = requests.post(url, json=payload, proxies=self.get_proxy())
        data = rq.json()
        
        if data['@context'] == '/contexts/Account':
            address = data['address']
            address_id = data['id']
            return address, address_id
        else:
            return False, False


    def get_messages(self, token: str):
        url = self.base_url + '/messages'
        header = {
            'Authorization': f'Bearer {token}'
        }
        rq = requests.get(url, headers=header, proxies=self.get_proxy())
        data = rq.json()
        
        messages_data = data['hydra:member']
        for message in messages_data:
            if message['from']['name'] == 'Facebook':
                code = re.findall(r'\d+', message['subject'])
                return code[0]
            else:
                return False


    def account_me(self):
        url = self.base_url + '/me'
        rq = requests.get(url, proxies=self.get_proxy())
        data = rq.json()
        print(data)


    def get_token(self, user: str, password: str):
        url = self.base_url + '/token'
        payload = {
            'address': user,
            'password': password
        }
        rq = requests.post(url, json=payload, proxies=self.get_proxy())
        data = rq.json()
        
        if rq.status_code == 200:
            return data['token']
        else:
            return False
