import requests

class Session:
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                'like Gecko) '
                                'Chrome/80.0.3987.149 Safari/537.36',
                'accept-language': 'en,gu;q=0.9,hi;q=0.8', 'accept-encoding': 'gzip, deflate, br'}
    cookies = {}

    def __init__(self, base_url):
        """This class is used to set new browser session for requested url.

        Keyword arguments:
        base_url -- The base url of the website.
        """
        self.session = requests.Session()
        self.base_url = base_url
        self.createNewSession()

    def createNewSession(self):
        """This method is used to create a new browser session for the requested url."""
        session = requests.Session()
        request = self.makeRequest(self.base_url)

    def makeRequest(self, url, params=None, responseType='json'):
        """This method is used to make a request to the url and set response cookies

        Keywork arguments:
        url -- The url to make the request to.
        params -- The parameters to be passed in the url.
        responseType -- json|text
        """
        try:
            if params == None:
                r = self.session.get(url=url, headers=self.headers, cookies=self.cookies)
            else:
                r = self.session.get(url=url, headers=self.headers, cookies=self.cookies, params=params)

            self.cookies = dict(r.cookies)

            if responseType == 'json':
                return r.json()
            elif responseType == 'content':
                return r.content
            elif responseType == 'text':
                return r.text
            else:
                return r
        except Exception as e:
            # print(e)
            return
