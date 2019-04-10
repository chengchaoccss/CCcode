import requests
from lxml import etree
from multiprocessing import Pool


def getonepage(url):
    try:
        r=requests.get(url)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        html=r.text
        return html
    except Exception as err:
        print(str(err))

def parsehtml(html):
    try:
    # print('cc')
        result=etree.HTML(html)
        # rs=result.xpath('//a[@title]//text()')
        href=result.xpath('//a[contains(@href,"/d") and contains(@href,"epub_down")]/@href')


        for i in range(len(href)):
            url='http://www.ixdzs.com/'+href[i]
            # print(url)
            htm=getonepage(url)
            dange=etree.HTML(htm)
            link=dange.xpath('//a[contains(@href,"down?id=") and contains(@href,"p=6")]/@href')
            name = dange.xpath('//h1[@itemprop="name"]/text()')
            # for j in range(len(link)):
            url='http://www.ixdzs.com/'+link[0]
            with open('link.txt','a') as f:
                f.write(url+'\n')
                f.close()
        print('ok')
    except:
        print('异常，跳过！')


def main(offset):
    url='https://www.ixdzs.com/sort/1/index_0_2_0_'+str(offset)+'.html'
    html=getonepage(url)
    parsehtml(html)
    # epubdown(url)

if __name__=='__main__':
    for x in range(1,101):
        main(x)
    # count=0
    # pool=Pool()
    # pool.map(main,[i for i in range(3)])