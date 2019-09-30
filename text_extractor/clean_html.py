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
    data = data.replace('—', '')
    return data

"""
使い方
url = "http://www.gutenberg.org/files/1400/1400-h/1400-h.htm"
data = url2text(url)
print(data)
でテキストデータ出てくるヨ

"""
url_list = ["http://www.gutenberg.org/files/1400/1400-h/1400-h.htm",
            "http://www.gutenberg.org/files/31847/31847-h/31847-h.htm",
            "http://www.gutenberg.org/files/14893/14893-h/14893-h.htm",
            "http://www.gutenberg.org/files/2148/2148-h/2148-h.htm",
            "http://www.gutenberg.org/files/564/564-h/564-h.htm"
            ]
for i, url in enumerate(url_list):
    print("url # %s" %(i+1))
    data = url2text(url)
    with open("text2send_%s" % (i+1), 'w', encoding='utf-8') as file:
        file.write(data)






