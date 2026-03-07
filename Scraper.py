from selenium import webdriver
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome()

def get_product_list():
    url = "https://www.amazon.com.mx/s?k=computadora&__mk_es_MX=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=KO6YXVDX4XHK&sprefix=computadora+%2Caps%2C117&ref=nb_sb_noss_2"
    driver.get(url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "lxml")

    a_class = "a-link-normal s-line-clamp-4 s-link-style a-text-normal"
    a_tags = soup.find_all("a", class_=a_class)

    for a in a_tags[:10]:
        title = a.text.replace("\n", "").strip()
        link = a.get("href")

        print("titulo:", title)
        print("link:", link)
        print()

        detail_link = "https://www.amazon.com.mx" + link if "https" not in link else link
        get_details(detail_link)

def get_details(url):
    driver.get(url)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "lxml")

    try:
        price_class = "a-offscreen"
        price = soup.find("span", class_=price_class).text
        print("price:", price)
    except:
        print("price: no encontrado")

    try:
        description_id = "feature-bullets"
        description = soup.find("div", id=description_id).text
        print("description:", description)
    except:
        print("description: no encontrada")

    print("=" * 50)

get_product_list()
driver.quit()