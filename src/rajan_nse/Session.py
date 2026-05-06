import requests

class Session:
    headers = {
        "Host": "www.nseindia.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:150.0) Gecko/20100101 Firefox/150.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "https://www.nseindia.com/",
        "Connection": "keep-alive",
        "Cookie": "bm_sv=5D49023AFCD060523A3913960F99DAF5~YAAQV/EBFxRIyPGdAQAANfuu+R+9bmrKEcasNzbfFYx5s3iC0qE48M0jt9zZP+B5istzzT1Mv3p13M+jvN8RKDE/NzRQXMWVDivb4KEqyUnwWUH2z66Y23MKTtNPDYX3B3cUwZFW7oaGHZVtGJh3x77ztGid4eC3/STOnVeRUQskYZzYYr1kHHjBWEDXdK8MkhO+4Hxa+X87Uv0+dB3eX4iopcuviYZvgJ4t8P/eZiHCpi2YXqkCbTKl8UvAyskKYfg=~1; _abck=2A89C3B3616704EB68BDEB3E1EA6CB71~-1~YAAQV/EBF/BHyPGdAQAA4vmu+Q9QSeNOAGr+DDRPVGCbv4g1buCwuQwF8v7Td/wTScYKLBBq/T3ts6VGtLd/dd3h7Ec/tf4m6/Tju0+8cXLcgVRnMPCg3dLjgiTV96KZgANnhQbYxHKzOsa2BkRtKXLtKzgE2K0+o/Mo5Ibb8fJ4iOzS9ENMUH9HKrgf+CApgAPueshV7MgEg4WHqSyUqh5TUMneftYqmTjY6HKYsTG8ogS3aWepAJI4kkZeaA/rSototsd9TrL3f9rBiWayBGJGBT34TuKGlJ9WCV6umInnYHMkmmv++TB1eOhOgufgx5LZ33GvF+iVeCYsjh9wj0p/jzGWL0ZHhjkOoSJ2U9wc2VDbk70LhW6CVYXg5Q/O2qoiRUIaXnBxRvY//+5f0CcamhmOi4JXhdu5UkkDt7HGfCnj8DUwsnGgnTY7dVg8OcDrdnppgOXp7kHMk8VPp97lsyM3nSTrHxwdUiln5xDnUARVAUlK2k2fa5yv3/1+U+DRyDCXICQO2ebPT2r6iXpiAYg0K9FMlSHKg+LpeoEHSPUTJwwFl7nzWWyrlMwQ~-1~-1~-1~AAQAAAAF/////6iHJ1q570QsbGSquS0Rm428JzF39NqMPYKuFZ7gQNgulYXCy/jX6/Q717XK5SC6setN9DsZI89ULEbtIErMFy0RjDkIKPb/lRmA~-1; ak_bmsc=87F16815318F22D31F35E31D3E7D9781~000000000000000000000000000000~YAAQV/EBF/5HyPGdAQAAe/qu+R9JO8R7OfCQqIIzR5A2RUfxy9W+0ayHHinO+CB8Ak72yqSD9NgiEMAHvFNqhpbl7QE/897ixMz0I/sxyDM78whr8/IKrLu/Vyyh3a34AaCJfoyc00AHuO58brby2600xYRDBmrWiEGGKEeRBHoXPgvv3kmwnPkUbYeMHnMmGMhNDo5t5uWzlEgmf79/83BvYnraBEZblEpE5fDfBcOG7UO01qr27795ZJPrg7ZhZuzhJTpbshERNlO88Xi+rujVraqsa73MLFdZy6juQVY7EzH73M4VWzCoA7Lec/IALVlORHx4eHHYmvSfUFV8wkzUlZ5YFGSucqXIJgjuW6lS5pm06oGMn/zDqudkw9OE4J70VlIHDDD9uPF9ZrdzDemQqZ9WCBOvHWLLhZj7AkIMqRZK/9RTPmZts34tXmwnUaaJ89E=; AKA_A2=A; bm_sz=B555918908402B00BB81F15124056B36~YAAQV/EBF+xHyPGdAQAAYfmu+R9AYsLO0TWOkB6pkuHNz1DxHgIobeQm/9AWqgfAvflKu2K3u6QLXK3a4ZKRPgjuaaiklbNhDV2LoWRUgrS8x9rGnSFSn9RkFLbbSHXy9x6poUS+25prb1hlVUZe2JTyPr9z0piYJxQ9uDn2J9/op0fNPN0BgxLNVRHtyn8XUOszg0eHJZZBTGaEtqnu1b5iScn0alVT1F6h4UJHihFQRsjO7LzBOOZMEZ0XC0SJKDAKNBDFFJLEkEwQjluv1JZ7T7eozBhfCgHv4yTOykQtf4SQ1cNcnV9c9+IlFtCdpa+TDh6Of5kupp1yt24rn/I804o9SIQCm/NKqoPx4/Wp7rgAl/gXhxBK/Xvn0UKibs5+dEZ6fyWaAV/7m3WGTA==~3294019~3159105",
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
                r = self.session.get(url=url, headers=self.headers, cookies=self.cookies, timeout=10)
            else:
                r = self.session.get(url=url, headers=self.headers, cookies=self.cookies, params=params, timeout=10)

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
