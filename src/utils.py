from googletrans import Translator
import cv2
import urllib
import numpy as np
import pytesseract
import requests
from src.parameters import HEADERS
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time
import pandas as pd
import os
import json
import re
import csv

# генератор случайных чисел
generator = np.random.default_rng()

# переводчик
translator = Translator()


def translateRU(text):
    result = translator.translate(text, src='en', dest='ru')
    return (result.text)


def translateEN(text):
    result = translator.translate(text, src='ru', dest='en')
    return (result.text)


def meke_prompt(cat_words, item, name, sostav, rangeDescription, keyWords):
    if sostav != '':
        return f"Сделай описание товара {item}, который называется {name} на маркетплейсе, с составом: {sostav}. Товар находиться в категориях : {cat_words}. Используй ключевые слова : {keyWords}. Также дай продуктовое обещание. Максимальная длина {rangeDescription} слов"
    return f"Сделай описание товара {item} на маркетплейсе, используя все слова из списка : {cat_words}. "


def make_feedback_prompt(discription):
    prompt = f"Напиши очень короткий отзыв от пользователя, который использовал продукт {discription}. Не пиши название товара в отзыве."
    return prompt


def prepare_test_HG(text):
    text = text.replace("«", '"')
    idx = text.find('"')
    idx += 1
    return (text[idx:])


def read_img_from_url(url):
    req = urllib.request.urlopen(url)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr, -1)
    return img


def read_text_on_img(img):
    text = pytesseract.image_to_string(img)
    return text


def get_top_words_browser(word_):
    url = f'https://www.bukvarix.com/keywords/?q={word_}'
    req = requests.get(url, HEADERS)
    src = req.text
    idx0 = src.find("[[")
    idx1 = src.find("]]")
    data = src[idx0+2:idx1]
    data = data.replace('"', '')

    data = data.split('],[')

    word_dict = {}
    for wordAN in data:
        word, _, _, count, _ = wordAN.split(',')
        word_dict[float(count)+generator.random()] = word
    sort_wd = list(word_dict.keys())
    sort_wd = sorted(sort_wd)[::-1]
    # возрвращает словарь {кол-во встреч запроса : запрос} и отсортированые в порядке возрастания массив со кол-вом встреч
    return ([word_dict, sort_wd])


def get_top_words_Wildberries(word_):
    with sync_playwright() as playwright:
        webkit = playwright.firefox
        browser = webkit.launch(headless=True)
        page = browser.new_page()
        page.goto(f"https://wb.moytop.com/?search={word_}&page=1")
        time.sleep(5)
        # page.wait_for_load_state('load')
        text = page.content()
    soup = BeautifulSoup(text, 'lxml')
    elements = soup.find_all('tr')
    elements = str(elements)
    elements = elements.replace('<tr>', '')
    elements = elements.replace('<td>', '')
    elements = elements.replace(',', '')
    elements = elements.replace('<td class="lider n">', '')
    listel = elements.split('</tr>')
    word_dict = {}
    for word in listel[1:-1]:
        signs = word.split('</td>')
        # слово/сколько запросов/сколько товаров/выгода
        word_dict[signs[0]] = [int(signs[1]), int(signs[3]), signs[4]]
    return word_dict


def get_requests_Wildberries(item, count=5):
    word_dict = get_top_words_Wildberries(item)
    req = []
    for word, countw in list(word_dict.items())[:count]:
        req.append([word, countw[0]])
    return req


def get_requests_Internet(item, count=5):
    word_dict, sort_wd = get_top_words_browser(item)
    req = []
    for i in range(count):
        req.append([word_dict[sort_wd[i]], int(sort_wd[i])])
    return req


def get_category():
    url = 'https://catalog.wb.ru/catalog/shealth2/catalog?appType=1&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&spp=0&sort=null&cat=10327&uclusters=8'
    response = requests.get(url=url)
    return response.json()


def prepare_items(response, limit=30):
    products = []
    products_raw = response.get('data', {}).get('products', None)
    if products_raw is not None and len(products_raw) > 0:
        for product in products_raw[:limit]:
            products.append({
                'id': product.get('id', None),
                'product_link': f'https://www.wildberries.ru/catalog/{product.get("id")}/detail.aspx'
            })
    return products


def save_urls_to_file(products, filename):
    with open(filename, 'w') as f:
        for product in products:
            f.write(product['product_link'] + '\n')


def get_product_data(url):
    jsonData = None
    article = int((re.findall(r'\d+', url))[0])

    _short_id = article // 100000
    if 0 <= _short_id < 144:
        basket = '01'
    elif 144 <= _short_id < 288:
        basket = '02'
    elif 288 <= _short_id < 432:
        basket = '03'
    elif 432 <= _short_id < 720:
        basket = '04'
    elif 720 <= _short_id < 1008:
        basket = '05'
    elif 1008 <= _short_id < 1062:
        basket = '06'
    elif 1062 <= _short_id < 1116:
        basket = '07'
    elif 1116 <= _short_id < 1170:
        basket = '08'
    elif 1170 <= _short_id < 1314:
        basket = '09'
    elif 1314 <= _short_id < 1602:
        basket = '10'
    elif 1602 <= _short_id < 1656:
        basket = '11'
    elif 1656 <= _short_id < 1920:
        basket = '12'
    else:
        basket = '13'
    rating = 0
    feedbacks = 0
    url = f"https://basket-{basket}.wb.ru/vol{_short_id}/part{article // 1000}/{article}/info/ru/card.json"
    res = requests.get(url=url)
    if res.status_code == 200:
        jsonData = json.loads(res.text)

        imt_id = jsonData["imt_id"]
        try:
            description = jsonData["description"]
        except:
            description = "No description available"
        try:
            brand = jsonData["selling"]["brand_name"]
        except:
            brand = "NULL"
        supplier_id = jsonData["selling"]["supplier_id"]
        photo_count = jsonData["media"]["photo_count"]
    url = f"https://feedbacks1.wb.ru/feedbacks/v1/{imt_id}"
    res = requests.get(url=url)
    if res.status_code == 200:
        jsonData = json.loads(res.text)
    url = f"https://card.wb.ru/cards/detail?appType=1&curr=rub&dest=-1257786&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,22,1,31,66,110,48,71,114&spp=0&nm={article}"
    res = requests.get(url=url)
    if res.status_code == 200:
        jsonData = json.loads(res.text)
        rating = jsonData['data']['products'][0]["reviewRating"]
        sale = jsonData['data']['products'][0]["sale"]
        feedbacks = jsonData['data']['products'][0]["feedbacks"]
        name = jsonData['data']['products'][0]["name"]
        qty = jsonData['data']['products'][0]['sizes'][0]['stocks'][0]["qty"]
        price = jsonData['data']['products'][0]["salePriceU"]/100
    url = f"https://product-order-qnt.wildberries.ru/by-nm/?nm={article}"
    res = requests.get(url=url)
    if res.status_code == 200:
        jsonData = json.loads(res.text)
        buysNum = jsonData[0]["qnt"]
    url = f"https://basket-{basket}.wb.ru/vol{_short_id}/part{article // 1000}/{article}/images/big/1.jpg"
    res = requests.get(url=url)
    if res.status_code == 200:
        image_link = "".join([
            f"https://basket-{basket}.wb.ru/vol{_short_id}/part{article // 1000}/{article}/images/big/1.jpg "])
    return [{
        "imt_id": imt_id,
        "feedbacks": feedbacks,
        "brand": brand,
        "name": name.replace(";", ","),
        "stars": rating,
        "qty": qty,
        "sale": sale,
        "price": price,
        "buysNum": buysNum,
        "image_link": image_link,
        "description": re.sub(r'\n', '', description.replace(";", ","))
    }]


def parse_top_WB(limit=30):
    response = get_category()
    products = prepare_items(response, limit=limit)

    project_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(project_dir, 'urls.txt')

    save_urls_to_file(products, file_path)

    data = []
    time_list = []
    strN = 0

    with open(file_path) as rf:
        with open("./storage/data.csv", 'w', encoding="cp1251", errors='replace', newline='') as csvfile:
            url = rf.readline()
            spamwriter = csv.writer(csvfile, delimiter=';', quotechar='|')

            column_names = [
                "цена",
                "название",
                "скидка",
                "рейтинг float",
                "в наличии",
                "Кол-во отзывов",
                "описание",
                "Куплено за год",
                "изображения",
                "Отзывы символы"
            ]
            spamwriter.writerow(column_names)

            while url:
                timer_begin = time.time()
                dataGet = get_product_data(url)
                spamwriter.writerow([
                    dataGet[0]["price"],
                    dataGet[0]["name"],
                    dataGet[0]["sale"],
                    dataGet[0]["stars"],
                    dataGet[0]["qty"],
                    dataGet[0]["feedbacks"],
                    dataGet[0]["description"],
                    dataGet[0]["buysNum"],
                    dataGet[0]["image_link"],
                    len(dataGet[0]["description"])
                ])
                data = data + [dataGet]
                timer_end = time.time()
                timer_secs = timer_end - timer_begin
                time_list.append(timer_secs)
                strN += 1
                url = rf.readline()

    jsonStr = json.dumps(data, sort_keys=False,
                         ensure_ascii=False, separators=(',', ': '))
    with open("./storage/data.json", "a", encoding='utf-8') as f:
        f.write(jsonStr)
