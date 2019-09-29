import requests
import lxml.html


url = "http://www.gutenberg.org/files/1400/1400-h/1400-h.htm"
def url2text(url):
    r = requests.get(url).text
    r = r.encode('utf-8')
    html = lxml.html.fromstring(r)
    elems = html.xpath('//p')
    elems = [i.text for i in elems if i.text is not None]
    return ' '.join(elems)

with open("sample.txt", "w", encoding='utf-8') as file:
    file.write(url2text(url))

