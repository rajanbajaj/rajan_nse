import requests

class Session:
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                'like Gecko) '
                                'Chrome/80.0.3987.149 Safari/537.36',
                'accept-language': 'en,gu;q=0.9,hi;q=0.8', 'accept-encoding': 'gzip, deflate, br'}
    cookies = {}

    def __init__(self, base_url):
        self.session = requests.Session()
        self.base_url = base_url
        self.createNewSession()
    
    def createNewSession(self):
        session = requests.Session()
        request = self.makeRequest(self.base_url)

    def makeRequest(self, url, params=None):
        try:
            if params == None:
                r = self.session.get(url=url, headers=self.headers, cookies=self.cookies)
            else:
                r = self.session.get(url=url, headers=self.headers, cookies=self.cookies, params=params)
            
            self.cookies = dict(r.cookies)
            return r.json()
        except Exception as e:
            # print(e)
            return
