import time
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename="log.txt",
                    filemode="a")
logger = logging.getLogger(__name__)


def en_and_de(s):
    return str(s).encode("utf-8").decode("utf-8")

def date_strptime(date: str):
    yy = date.find("年")
    mm = date.find("月")
    dd = date.find("日")
    tt = date.split()[1]
    return "{}-{}-{}_{}-{}".format(date[0: yy], date[yy + 1: mm], date[mm + 1: dd], tt[0: 2], tt[3: 5])


def get_zone(qq: str, driver: webdriver.Chrome):
    url = "https://user.qzone.qq.com/{}?source=friendlist".format(qq)
    driver.get(url)

    while True:
        flag = input("scan to log in[Y/N]")
        if flag == "Y":
            break
        if flag == "N":
            return

    cnt = 0

    while True:
        for j in range(1, 5):
            driver.execute_script("window.scrollBy(0,5000)")

        time.sleep(5)

        driver.switch_to.frame("QM_Feeds_Iframe")
        bs = BeautifulSoup(driver.page_source.encode('GBK', 'ignore').decode('gbk'), "html.parser")

        pres = bs.find_all('li', attrs={"class": "f-single f-s-s"})

        for i in range(cnt, len(pres)):
            pre = pres[i]



            publish_date = pre.find("div", attrs={"class": "info-detail"}).span
            info = pre.find("div", attrs={"class": "f-info"})
            publish_date = en_and_de(publish_date.text)

            full_element = driver.find_element("id", pre["id"])
            file_path = ".\\screen\\{}.png".format(date_strptime(publish_date))
            full_element.screenshot(file_path)


            if info:
                info = en_and_de(info.text)
                logger.info("{}: {}".format(publish_date, info))
            else:
                logger.info("{}: {}".format(publish_date, "NULL"))

        if cnt == len(pres):
            break
        cnt = len(pres)
        driver.switch_to.default_content()





if __name__ == "__main__":
    qq = "xxxxx"
    get_test(qq, webdriver.Chrome())