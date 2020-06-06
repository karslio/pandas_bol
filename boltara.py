import csv
from selenium import webdriver
import re
import time


# amazon urun bilsi aliniyor
def get_product_info(ean):
    try:
        amazonUrl = f'https://www.amazon.nl/s?k={ean}&rh=p_85%3A16497054031%2Cp_6%3AA17D2BRD4YMT0X&dc&__mk_nl_NL=%C3%85M%C3%85%C5%BD%C3%95%C3%91&qid=1590857193&rnid=16332313031&ref=sr_nr_p_6_1'
        browser.get(amazonUrl)
        text1 = browser.find_elements_by_css_selector(
            "div.a-section.a-spacing-none.a-spacing-top-micro > div:nth-child(2) > span")
        try:
            text1 = text1[0].text
        except:
            text1 = None
        text2 = browser.find_elements_by_css_selector(
            "div.a-section.a-spacing-none.a-spacing-top-micro > div.a-row.a-size-base.a-color-secondary.s-align-children-center > div > span:nth-child(2)")
        try:
            text2 = text2[0].text
        except:
            text2 = None
        text3 = browser.find_elements_by_css_selector(
            "#div.a-section.a-spacing-none.a-spacing-top-micro > div > div > span:nth-child(2)")
        try:
            text3 = text3[0].text
        except:
            text3 = None
        text4 = browser.find_elements_by_css_selector(
            "div.a-section.a-spacing-none.a-spacing-top-micro > div > div:nth-child(2) > span")
        try:
            text4 = text4[0].text
        except:
            text4 = None

        PamazonUrl.append(amazonUrl)
        Text1.append(text1)
        Text2.append(text2)
        Text3.append(text3)
        Text4.append(text4)
        browser.get(amazonUrl)
        time.sleep(2)
        amazonPrice = browser.find_element_by_class_name('a-price-whole').text
        amazonPrice = amazonPrice.replace(',', '.')
    except:
        amazonPrice = None
    PEan.append(ean)
    PamazonPrice.append(amazonPrice)


Text1 = []
Text2 = []
Text3 = []
Text4 = []
PbolUrl = []
PbolPrice = []
PEan = []
PamazonUrl = []
PamazonPrice = []

options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:\\Users\\Lenovo Thinkpad\\AppData\\Local\\Google\\Chrome\\User Data\\")
options.add_argument('--profile-directory=Profile 2')
browser = webdriver.Chrome(options=options)

page = 1
urun = 1
while True:
    browser.get(
        f"https://www.bol.com/nl/l/sport-spel/N/10498/?page={page}")  # bol page linki
    time.sleep(2)
    nextButton = browser.find_elements_by_css_selector(
        "#js_pagination_control > ul > li.\[.pagination__controls.pagination__controls--next.\] > a")  # next button var mi yok mu ?
    links = browser.find_elements_by_css_selector(
        "div.product-title--inline > a")  # ilk sayfadaki tum urun liklerini aliyoruz
    hrefs = []
    link = 0
    while link < len(links):
        hrefs.append(links[link].get_attribute("href"))  # her linkin hrefini aliyoruz.
        link += 1
    i = 0
    while i < len(hrefs):
        PbolUrl.append(hrefs[i])
        browser.get(hrefs[i])
        time.sleep(2)
        i += 1
        urun += 1
        try:
            productPrice = browser.find_elements_by_class_name("promo-price")[0].text
        except:
            productPrice = "Niet leverbaar"
        productPrice = productPrice.replace('\n', '.').replace('-', '00')
        pageSource = browser.page_source
        productInfo = re.search(',"gtin13":"(\d*)",', pageSource)
        try:
            productEan = productInfo.group(1)
        except:
            productEan = "None"

        PbolPrice.append(productPrice)
        PEan.append(productEan)
        get_product_info(productEan)
        print(
            f"page: {page} urun:{urun - 1}, {PEan[len(PEan) - 1]}, {PbolPrice[len(PbolPrice) - 1]}, {PamazonPrice[len(PamazonPrice) - 1]}, {Text1[len(Text1) - 1]}, {Text2[len(Text2) - 1]}, {Text3[len(Text3) - 1]}, {Text4[len(Text4) - 1]}")
        with open('sport-spel.csv', mode='a', newline='') as f:
            products_writer = csv.writer(f, delimiter=',', )
            products_writer.writerow([page, urun, PEan[len(PEan) - 1],
                                      PbolUrl[len(PbolUrl) - 1], PbolPrice[len(PbolPrice) - 1],
                                      PamazonUrl[len(PamazonUrl) - 1], PamazonPrice[len(PamazonPrice) - 1],
                                      Text1[len(Text1) - 1], Text2[len(Text2) - 1], Text3[len(Text3) - 1],
                                      Text4[len(Text4) - 1]])
    time.sleep(2)
    page += 1
    if len(nextButton) == 0:
        print("Tum sayfalar bitti")
        break
