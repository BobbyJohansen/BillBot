"""bill translate to <language-code> <message>"""
from bs4 import BeautifulSoup
import re
from urllib import quote, unquote
import urllib2
import requests

def google(q):
    query = quote(q)
    url = "http://www.translate.google.com?q={0}".format(query)
    soup = BeautifulSoup(requests.get(url).text)

    answer = soup.findAll("h3", attrs={"class": "r"})
    if not answer:
        return ":crying_cat_face: Sorry, google doesn't have an answer for you :crying_cat_face:"

    return unquote(re.findall(r"q=(.*?)&", str(answer[0]))[0])



def translate(to_translate, to_langage="auto", langage="en"):
	'''Return the translation using google translate
	you must shortcut the langage you define (French = fr, English = en, Spanish = es, etc...)
	if you don't define anything it will detect it or use english by default
	Example:
	print(translate("salut tu vas bien?", "en"))
	hello you alright?'''
	agents = {'User-Agent':"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)"}
	before_trans = 'class="t0">'
	link = "http://translate.google.com/m?hl=%s&sl=%s&q=%s" % (to_langage, langage, to_translate.replace(" ", "+"))
	request = urllib2.Request(link, headers=agents)
	page = urllib2.urlopen(request).read()
	result = page[page.find(before_trans)+len(before_trans):]
	result = result.split("<")[0]
	return result

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.match(r"bill translate to (([a-z]{2})|(zh-CN)|(zh-TW)), (.*)", text)
    if not match: return

    return translate(match.group(5),match.group(1))

if __name__ == '__main__':
    query = 'bill translate to de, hello world'
    match = re.match(r"bill translate to (([a-z]{2})|(zh-CN)|(zh-TW)), (.*)", query)
    print translate(match.group(5),match.group(1))
    
