from src.analysis import *
from src.generate_text import *
from src.P2JS import *

#get_requests_Internet('топ',count=5)
#analitic_top('./storage/DATA1.csv')
#get_requests_Wildberries('топ',count=5)

#generate_text('мой товар - БАД для снижения веса. Найди ключевые слова связанные с ним. Слова: сильные таблетки для похудения, таблетки для похудения, голдлайн ,таблетки от живота ,фермент ,от вздутия, коллаген для суставов, мультивитамины, гиалуроновая кислота капсулы, коллаген питьевой, мультивитамины для женщин, капсулы для волос')
eel.init('front')
eel.start('index.html', mode="default")