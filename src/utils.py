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


#генератор случайных чисел
generator = np.random.default_rng()

#переводчик
translator = Translator()

def translateRU(text):
    result = translator.translate(text, src='en', dest='ru')
    return(result.text)

def translateEN(text):
    result = translator.translate(text,src='ru', dest='en')
    return(result.text)

def meke_prompt(cat_words,item,name,sostav,rangeDescription,keyWords):
    print('______________________2')
    if sostav!='':
        return f"Сделай описание товара {item}, который называется {name} на маркетплейсе, с составом: {sostav}. Товар находиться в категориях : {cat_words}. Используй ключевые слова : {keyWords}. Также дай продуктовое обещание. Максимальная длина {rangeDescription} слов"
    return f"Сделай описание товара {item} на маркетплейсе, используя все слова из списка : {cat_words}. "


def make_feedback_prompt(discription):
    prompt=f"Напиши очень короткий отзыв от пользователя, который использовал продукт {discription}. Не пиши название товара в отзыве."
    return prompt


def prepare_test_HG(text):
    text=text.replace("«",'"')
    idx=text.find('"')
    idx+=1
    return(text[idx:])


def read_img_from_url(url):
    req= urllib.request.urlopen(url)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr, -1)   
    return img

def read_text_on_img(img):
    text = pytesseract.image_to_string(img)
    return text



def get_top_words_browser(word_):
    url=f'https://www.bukvarix.com/keywords/?q={word_}'
    req=requests.get(url,HEADERS)
    src=req.text
    idx0=src.find("[[")
    idx1=src.find("]]")
    data=src[idx0+2:idx1]
    data=data.replace('"','')
    data=data.split('],[')
    word_dict={}
    for wordAN in data:
        word, _, _, count, _ = wordAN.split(',')
        word_dict[float(count)+generator.random() ]=word
    sort_wd=list(word_dict.keys())
    sort_wd=sorted(sort_wd)[::-1]
    #возрвращает словарь {кол-во встреч запроса : запрос} и отсортированые в порядке возрастания массив со кол-вом встреч
    return([word_dict,sort_wd])


def get_top_words_Wildberries(word_):
    with sync_playwright() as playwright:
        webkit = playwright.firefox
        browser = webkit.launch(headless=True)
        page = browser.new_page()
        page.goto(f"https://wb.moytop.com/?search={word_}&page=1")
        time.sleep(5)
        #page.wait_for_load_state('load')
        text=page.content()
    soup=BeautifulSoup(text,'lxml')
    elements=soup.find_all('tr')
    elements=str(elements)
    elements=elements.replace('<tr>','')
    elements=elements.replace('<td>','')
    elements=elements.replace(',','')
    elements=elements.replace('<td class="lider n">','')
    listel=elements.split('</tr>')
    word_dict={}
    for word in listel[1:-1]:
        signs=word.split('</td>')
        #слово/сколько запросов/сколько товаров/выгода
        word_dict[signs[0]]=[int(signs[1]),int(signs[3]),signs[4]]
    return word_dict


def get_requests_Wildberries(item,count=5):
    word_dict =get_top_words_Wildberries(item)
    req=[]
    for word, countw in list(word_dict.items())[:count]:
        req.append([word,countw[0]])
    return req


def get_requests_Internet(item,count=5):
    word_dict , sort_wd=get_top_words_browser(item)
    req=[]
    for i in range(count):
        req.append([word_dict[sort_wd[i]],int(sort_wd[i])])
    return req













