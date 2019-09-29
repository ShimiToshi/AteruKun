import requests
import lxml.html
import re


def url2text(url):
    r = requests.get(url).text
    r = r.encode('utf-8')
    html = lxml.html.fromstring(r)
    elems = html.xpath('//p')
    elems = [i.text for i in elems if i.text is not None]
    return reduce_space(''.join(elems))


def reduce_space(data):
    data = re.sub('\s+', ' ', data)
    data = data.replace("\n\n", '')
    return data

"""
使い方
url = "http://www.gutenberg.org/files/1400/1400-h/1400-h.htm"
data = url2text(url)
print(data)
でテキストデータ出てくるヨ

"""



