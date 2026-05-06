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
        """Launch a headless browser to fetch fresh NSE session cookies,
        then prime the requests session with them."""
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=["--disable-http2"]
                )
                context = browser.new_context(
                    user_agent=self.headers["User-Agent"]
                )
                page = context.new_page()
                try:
                    page.goto(self.base_url, wait_until="domcontentloaded", timeout=30000)
                    page.wait_for_timeout(3000)
                except Exception:
                    pass
                browser_cookies = context.cookies()
                browser.close()

            if browser_cookies:
                self.cookies = {c["name"]: c["value"] for c in browser_cookies}
                self.headers["Cookie"] = "; ".join(
                    f"{c['name']}={c['value']}" for c in browser_cookies
                )
        except Exception as e:
            print(f"[Session] Playwright cookie refresh failed: {e}")

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
