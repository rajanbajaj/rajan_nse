import requests

class Session:
    headers = {
        "Host": "www.nseindia.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:137.0) Gecko/20100101 Firefox/137.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://www.nseindia.com/",
        "Connection": "keep-alive",
        "Cookie": "defaultLang=en; _abck=DFB61A853261BC9D58B7F9597DA90023~0~YAAQjc8uF6qy2eaWAQAAIQOwIg2r7J4BCf+9gQPiyJeaJRc8B3YsQl5zpRTycmAGfS5K8mGMwYpPqP3Z/nc2/DaM7MTplnp3d7mtanxyLYQ+lrd6JTAV82zawJXCymAHExhXkIsSN1g2T3jzBpnh1BNJtjz5XQA8JUxBoWw1UwOuo52ynn6ar8leuhOPc8L9O10sYDIKv+wfE0PIeX3pKAqD4Y+HHYq4MxlMALJui95S6418kidNHqm1Xs3RsNBp/fzTBwEPMn8aIUJAtzcn9t6C88JjHfkM6gudlOO2Y4JrYzkfXDp0IOnSnj0CHuqTsNUmyZZLVyAoKZ679uAes+EpsLCLhur6SJCMMSOCkbpaJ1Lu2RmKBNKtSkk1QQNMEL8BS3lyv1V3oKV1LYZ8Ium+fgHQE94yY1a0xxX6kp97CLTAsNpFNXlS8tNAtWKLx90DRkCDeYYnBcdfd3wckozckvGKEGintOHl5z/RSwZfXXlNB82wmEyJNySMlEZSNXRCxaPiFW8FH5mpck84lj0LF+pVXYAbOqs2in8QfUqDfsH/ZWowi5OAatU34as7raUpRnBkYKoYICYZzhhM7aA77QahaL50+cXp4wXeywt1DdxcIyQr6jz0Ibd96g==~-1~-1~-1; bm_sz=55E3FA418368D6788CF0B86B4458848A~YAAQhc8uF0ZHLNGWAQAAQvf8IRvGgkJCRk0Zc3XELiUNYeZGX1vDL/RyqBwNNxmrKpxCLnK4ZupW0GWWDHr+56mVztH2jubdheTYhu/VdXeqAOBXxOaVFOuuS96uPIOu2G5eHQYqi0DBaXDwmKrA9z+sMtQWAz3LkEVlWGMUupOYSTF6SCHb40fzWCbjhuyrCrLeiFF1O7uKJ6Ch/xkdssnvogqO/CJE76GxFnuYij2BLD1xTB+VHkAHiwu/bEazT7j5s9XhVJXO0a/sqRdm49ES5toz/WpLsFoDRCC4T0SBvfolZIoDDllxyt8C2KtJMHAdvdpW9h6eM2f++sf3ZprgXjcTn2GQ38sjIREP9H6WvcqPM7OnhvMzatpgNTufYEh0/tnkkyQuF5CpNwodCGwpJW+lbkoy5vCGg8Qu5po=~3159856~3617604; ak_bmsc=9296125DD1C308EBBEE39E36EEBA1CF6~000000000000000000000000000000~YAAQjc8uF/1Kt+aWAQAANtJpIht7lbqfv4dC9AsfobBLZ283xrhhnnDfAhyAB+hwnlwcUHyFYB6UjvJlzfek71Am3zsdrnZM4klHim/7Yuz/pITF9cO0d+9z7/Cf1UO0sg0LXLENb9okqQU45KI3VP+ao9O3W1Y6517dK6CwsWeJGBK5b0He5uIskt4Eb1c7oxMlXqnZKxaxPuJ4XhjKH0IP7XLi8S8w8QglszTYmeZzuqFkpwxuR5tRp6yg0URc6JAzVU7n6QG70lj4Xcl+CcK0uLKCtI0ePNJ0DjU7l9jAtUnC4EjTzMReaRwvz1WBxdEliuJzj4PZna9hl2nnbgcqYQYXwWZE+RcFmiD4AT76JjiLaRoBqkBgjl/UGoW+PPm99DhpvTKfwQbv; bm_sv=B597C9F33452E64475032D051D42D587~YAAQjc8uFwm82eaWAQAABhOwIhtSG/o2bG7aebQ+P17S/+pJJ3mNTrzU3dX164hk4zs+EtQEJqMv/9OVA96qe3XMp3pvraiur1VX4Fl3vzxe473nMGaSd87/C1Z8tXMGURV/jcFaKcDA9MFUk40c8i8gmROw45E9r/v8UPIEU2nNKzpv9DOL4hUV8ViJvKnM2X2umAoOvxARegvWuSVUOcHMjCkWUqpItqXMMBU/bJ5sJJVRqx2gSHlDDFapRFKHD8MyLg==~1; AKA_A2=A; bm_mi=A70754BC6EAD491E87419FE145D72347~YAAQjc8uFwSy2eaWAQAA/wGwIhsx63a+HU2eTV58jLKWAi3MeKfwAOJtus7SXVpS4M41wW4vpVEC+TzWsIP7Wnt0E/pew8QSX6zRyEEXRD6n6vtues1BS7h09VyyT772W+0ZeJC2YrkQOQZU3bteYAw21N/ZF6FEAlTN9GZHof8rjqvY9xna98hE2T7y6r5Mlxe0ssVaiLNlgC5TybFZ6xzyKHzwSHRVkMUkjCSucuLVZ/RuQZbgByWQ5fGnMN60UIGjGpEBdANW26ROaEYDtU1GmjrEU6EixB2N/CMwU6DBk0K+45MZ7nMPfEF6+W0=~1; nsit=IgH6AWUW87i6bauDaw8lbMfV; nseappid=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcGkubnNlIiwiYXVkIjoiYXBpLm5zZSIsImlhdCI6MTc0ODYzMzY1MCwiZXhwIjoxNzQ4NjQwODUwfQ.2Wwgq-cKP1XJjSKWkmFLMvBB0XDOkw6Aunxky_7GVAU",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "DNT": "1",
        "Sec-GPC": "1",
        "Priority": "u=4",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "TE": "trailers"
    }
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
