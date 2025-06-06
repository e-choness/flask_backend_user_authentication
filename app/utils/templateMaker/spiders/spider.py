import requests
from bs4 import BeautifulSoup
import html5lib


class Spider:
    def __init__(self, url, headers=None):
        self.url = url
        self.headers = headers
        self.soup = None
        self.response = None

    def runSpider(self, method='get', data=None, needSoup=True, manager='html5lib'):
        try:
            if method is 'get':
                self.response = requests.get(
                    url=self.url, headers=self.headers)
            elif method is 'post':
                self.response = requests.post(
                    url=self.url, data=data, headers=self.headers)
        except Exception as e:
            print(e)
            return

        if needSoup:
            htmlData = self.response.text
            self.soup = BeautifulSoup(htmlData, manager)
        return self

    def getElementByClassName(self, className):
        return self.soup.find(class_=className).text

    def getAllElementByClassName(self, className):
        return self.soup.find_all(class_=className)
