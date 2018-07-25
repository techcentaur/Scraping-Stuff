import re
import pprint
import requests
from lxml import html  
from time import sleep
from collections import OrderedDict

class Amazon:
    """Amazon scraper"""
    def __init__(self):
        pass

    def amazon_parser(self, url):

        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'}
        page = requests.get(url, headers=headers)
        
        try:
            doc = html.fromstring(page.content)
            XPATH_NAME = '//h1[@id="title"]//text()'
            XPATH_SALE_PRICE = '//span[contains(@id,"ourprice") or contains(@id,"saleprice")]/text()'
            XPATH_ORIGINAL_PRICE = '//td[contains(text(),"List Price") or contains(text(),"M.R.P") or contains(text(),"Price")]/following-sibling::td/text()'
            XPATH_CATEGORY = '//a[@class="a-link-normal a-color-tertiary"]//text()'
            XPATH_AVAILABILITY = '//div[@id="availability"]//text()'
            XPATH_ETA = '//div[@id="ddmDeliveryMessage"]//text()'
            buyop = '//div[@class="a-text-center a-spacing-mini"]//text()'
            delop = '//div[@id="contextualIngressPt"]//text()'
            prodinfo = '//div[@class="content"]//text()'


            RAW_NAME = doc.xpath(XPATH_NAME)
            RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)
            RAW_CATEGORY = doc.xpath(XPATH_CATEGORY)
            RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)
            RAW_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY)
            RAW_ETA = doc.xpath(XPATH_ETA)

            try:
                buyopval = doc.xpath(buyop)
                buyopval = " ".join(buyopval)
                buyopval = buyopval.replace('\xa0', '')
            except Exception as e:
                buyopval = None

            try:
                delopval = doc.xpath(delop)
                _del = ' '.join(''.join(delopval).split()) if delopval else None
            except Exception as e:
                _del = None

            ll = []
            try:
                raw_prodinfo = doc.xpath(prodinfo)
                l = raw_prodinfo
                l = ' '.join(''.join(l).split()) if l else None
                l = re.sub(r'\{[^}]*\}', '', l)
                l = l.split()
                for i in l:
                    if not i.startswith('.'):
                        ll.append(i)
                ll = " ".join(ll)
            except Exception as e:
                ll = "None available"

            NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
            SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
            CATEGORY = ' > '.join([i.strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None
            ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None
            AVAILABILITY = ''.join(RAW_AVAILABILITY).strip() if RAW_AVAILABILITY else None
            ETA = ' '.join(''.join(RAW_ETA).split()) if RAW_ETA else None

            if not ORIGINAL_PRICE:
                ORIGINAL_PRICE = SALE_PRICE

            data = OrderedDict()
            data = {
                    'NAME': NAME,
                    'SALE PRICE': SALE_PRICE,
                    'CATEGORY': CATEGORY,
                    'ORIGINAL PRICE': ORIGINAL_PRICE,
                    'AVAILABILITY': AVAILABILITY,
                    'URL': url,
                    'ETA': ETA,
                    'BUY OPTIONS': buyopval + " | " + _del,
                    'Product Info': ll
                    }
 
            return data
        except Exception as e:
            return {"Exception": e}
     

    # If ASIN given (Amazon specific)
    def amazon_parser_from_asin(self, asin):
        url = "http://www.amazon.com/dp/" + asin
        return self.amazon_parser(url)
     

class Ebay:
    """Ebay scraper"""
    def __init__(self):
        pass

    def ebay_parser(self, link):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'}
        page = requests.get(link, headers=headers)
        try:
            doc = html.fromstring(page.content)
            TITLE = '//h1[@id="itemTitle"]//text()'
            CAT = '//td[@id="vi-VR-brumb-lnkLst"]//text()'
            SHIPPING_COST = '//span[@id="fshippingCost"]//text()'
            SHIPPING_SVC = '//span[@id="fShippingSvc"]//text()'
            PAY = '//div[@id="payDet1"]//text()'
            SOLD = '//span[@class="w2b-sgl"]//text()'

            RAW_TITLE = doc.xpath(TITLE)
            RAW_CAT = doc.xpath(CAT)
            RAW_SHIP_COST = doc.xpath(SHIPPING_COST)
            RAW_SHIP_SVC = doc.xpath(SHIPPING_SVC)
            RAW_PAY = doc.xpath(PAY)
            RAW_SOLD = doc.xpath(SOLD)

            _title = RAW_TITLE[1]
            _cat = "".join(RAW_CAT)
            for i in ['\n', '\t', '\xa0']:
                _cat = _cat.replace(i, '')

            _ship_cost = ' '.join(''.join(RAW_SHIP_COST).split()) if RAW_SHIP_COST else None
            _ship_svc = ' '.join(''.join(RAW_SHIP_SVC).split()) if RAW_SHIP_SVC else None
            
            _paystr = "".join(RAW_PAY)
            for i in ['\n', '\t', '\xa0']:
                _paystr = _paystr.replace(i, '')

            _sold = " | ".join(RAW_SOLD)

            data = OrderedDict()
            data = {
            'TITLE': _title,
            'CATEGORY': _cat,
            'SHIPPING COST': _ship_cost,
            'SHIPPING SERVICE': _ship_svc,
            'PAYMENT': _paystr,
            'SOLD DETAILS': _sold
            }

            return data

        except Exception as e:
            print(e)
        return True


if __name__=="__main__":
    a = Amazon().amazon_parser("https://www.amazon.in/Esquire-Spin-mop-2-Refills/dp/B071JWBFDT/ref=lp_15185218031_1_2?s=home-improvement&ie=UTF8&qid=1532165388&sr=1-2")
    e = Ebay().ebay_parser("https://www.ebay.in/itm/portable-rugby-wireless-bluetooth-mini-stereo-speaker-fm-radio-usb-microsd/292105966607?hash=item4402df540f")

