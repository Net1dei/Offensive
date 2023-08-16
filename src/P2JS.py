from src.generate_text import generate_text
from src.utils import meke_prompt, make_feedback_prompt, prepare_test_HG, get_requests_Wildberries, get_requests_Internet, parse_top_WB
from src.analysis import get_predict, analitic_top
import eel
from src.generate_img import gen_img


@eel.expose
def generate_descriptionJS(chat, cat_words, item, name, sostav, rangeDescription, keyWords):
    return generate_text(meke_prompt(cat_words, item, name, sostav, rangeDescription, keyWords), chat)


@eel.expose
def generate_feedbackJS(chat, discription):
    return prepare_test_HG(generate_text(make_feedback_prompt(discription), chat))


@eel.expose
def get_predictJS(requestCount, inStock, FeedbackCount, rating, cost, categoryPosition, discount):
    args = [int(requestCount), int(inStock), int(FeedbackCount), float(
        rating), int(cost), int(categoryPosition), int(discount)]
    return get_predict(args)


@eel.expose
def analitic_topJS():
    parse_top_WB(limit=10)
    analitic_top('./storage/data.csv')


@eel.expose
def get_requests_WildberriesJS(item, count=5):
    return get_requests_Wildberries(item, count=5)


@eel.expose
def get_requests_InternetJS(item, count=5):
    return get_requests_Internet(item, count=5)


@eel.expose
def gen_imgJS(imgB64, prompt, txt):
    gen_img(imgB64, prompt, txt)
