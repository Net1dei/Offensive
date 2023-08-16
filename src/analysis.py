from catboost import CatBoostRegressor
from src.parameters import *
import pandas as pd
import matplotlib.pyplot as plt
from colorthief import *
from src.utils import *
import re
from src.parameters import HEADERS

modelD = CatBoostRegressor()
modelD.load_model(WAY_TO_MODEL)

#предсказание продаж
def get_predict(X):
    y=modelD.predict(X)
    print(y)
    if y<0: y=0
    return(y)

import urllib.request
from PIL import Image

# модернизация класса библиотеки colorthief
class ColorThief(object):
    def __init__(self, url):      
        urllib.request.urlretrieve(url,"./storage/items.jpg")
        self.image = Image.open("./storage/items.jpg")

    def get_color(self, quality=10):
        palette = self.get_palette(5, quality)
        return palette[0]

    def get_palette(self, color_count=10, quality=10):
        image = self.image.convert('RGBA')
        width, height = image.size
        pixels = image.getdata()
        pixel_count = width * height
        valid_pixels = []
        for i in range(0, pixel_count, quality):
            r, g, b, a = pixels[i]
            if a >= 125:
                if not (r > 250 and g > 250 and b > 250):
                    valid_pixels.append((r, g, b))


        cmap = MMCQ.quantize(valid_pixels, color_count)
        return cmap.palette
    

#выявление доминирующих цветов
def analyze_image(url,quality=1,palette=False):
  color_thief = ColorThief(url)
  if palette:
    palette = color_thief.get_palette(color_count=6)
    return palette
  else:
    dominant_color = color_thief.get_color(quality)
    return dominant_color
  
def analitic_colors(csv_im,quality=1,palette=False):
    colors=[]
    for img in csv_im:
        color = analyze_image(img,quality,palette)
        colors.append(color)
    return colors

def plot_hist(column):
    _ , ax = plt.subplots(figsize=(12, 6))
    ax.hist(sorted(column.values))
    ax.set_title(f"{column.name}")
    plt.savefig(f"./storage/graphs/hist_{column.name}.png")

#обрезание имени до двух слов
def cut_name(csv):
    items=[]
    for item in csv['название']:
        item= item.replace('-',' ')
        idx=[i for i, ltr in enumerate(item) if ltr == ' ']
        word=re.findall('[^0-9]',item[:idx[1]])
        items.append(''.join(word))
    csv['название']=items
    return csv

#Выводит таблицу с количеством запросов по товару в интернете
def get_main_request_Internet(csv):
    #вход : таблица
    #выход : таблица с новым стобцом запросов
    browser_count_item=[]
    for item in csv['название']:
        _ , sort_wd=get_top_words_browser(item)
        browser_count_item.append(int(sort_wd[0]))
    csv['Число запросов в Интернете за месяц'] = browser_count_item
    return csv

#Выводит таблицу с количеством запросов по товару в Wildberries
def get_main_request_Wildberries(csv):
    #вход : таблица
    #выход : таблица с новым стобцом запросов
    browser_count_item=[]
    for item in csv['название']:
        word_dict =get_top_words_Wildberries(item)
        try:
            browser_count_item.append(list(word_dict.values())[0][0])
        except: browser_count_item.append(0)
    csv['Число запросов в Wildberries за 3 месяца'] = browser_count_item
    return csv

def get_len_discription(csv):
    csv['длина описания']=[len(x) for x in csv['описание']]
    return csv

#рисует цвета в rgb пространстве
def plot_colors(column):
    xs=[]
    ys=[]
    zs=[]
    colors=[]
    for color in column:

      xs.append(color[0])
      ys.append(color[1])
      zs.append(color[2])
      colors.append([color[0]/255,color[1]/255,color[2]/255])
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(projection='3d')
    ax.scatter(xs, ys, zs,depthshade=False,c=colors,s = [100 for n in range(len(colors))])
    ax.scatter([0,0,255], [0,255,0], [255,0,0],depthshade=False,c=[[0,0,1],[0,1,0],[1,0,0]],s = [500,500,500])
    plt.savefig(f"./storage/graphs/цвета.png")

#анализ топа товаров
def analitic_top(path_csv):
    csv = pd.read_csv(path_csv, sep=';',encoding="cp1251")#"cp1251"
    csv=cut_name(csv)
    csv = get_main_request_Internet(csv)
    csv = get_main_request_Wildberries(csv)
    csv=csv.drop(['название'], axis=1)
    csv=get_len_discription(csv)
    csv=csv.drop(['описание'], axis=1)
    csv['цвет']=analitic_colors(csv['изображения'])
    plot_colors(csv['цвет'])
    csv=csv.drop(['цвет'],axis=1)
    csv=csv.drop(['изображения'], axis=1)
    csv.to_csv('data')
    for sign in csv.columns:
        plot_hist(csv[sign])


