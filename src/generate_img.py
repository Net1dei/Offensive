from playwright.sync_api import Page
from playwright.async_api import async_playwright
import time
import asyncio
import urllib.request
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from src.parameters import LOGIN_IMG_GENERATOR
from src.parameters import PASSWORD_IMG_GENERATOR
import io 
import base64


async def gen_imag(imgB64):
    imgB64 = imgB64[imgB64.find(','):]
    image_bytes = base64.b64decode(imgB64)
    image_buffer = io.BytesIO(image_bytes)
    image = Image.open(image_buffer)
    image.save("./storage/1.png")


async def downloadurl(prompt):
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://imgcreator.zmo.ai/tools/background-changer")
        await page.set_input_files("input[type='file']", './storage/1.jpg')
        await page.get_by_role("textbox", name="Email*").fill(LOGIN_IMG_GENERATOR)
        await page.get_by_role("textbox", name="Password*").fill(PASSWORD_IMG_GENERATOR)
        time.sleep(2)
        await page.locator("(//div[contains(@class,'bg-primary cursor-pointer')])[1]").click()
        time.sleep(2)
        await page.mouse.click(410, 85)
        await page.get_by_placeholder("Describe the image you want to see").fill(prompt)
        time.sleep(2)
        await page.mouse.click(254, 413)

        result = None
        while result is None:
            try:
                result = await page.query_selector("(//img[contains(@class,'relative h-full')])[4]")
            except:
                pass

        image_url = await result.get_attribute("src")
        url = image_url.replace(" ", "%20")
        urllib.request.urlretrieve(url, './storage/0.webp')

        result1 = await page.query_selector("(//img[contains(@class,'relative h-full')])[1]")
        image_url1 = await result1.get_attribute("src")
        url1 = image_url1.replace(" ", "%20")
        urllib.request.urlretrieve(url1, './storage/1.webp')

        result2 = await page.query_selector("(//img[contains(@class,'relative h-full')])[2]")
        image_url2 = await result2.get_attribute("src")
        url2 = image_url2.replace(" ", "%20")
        urllib.request.urlretrieve(url2, './storage/2.webp')

        result3 = await page.query_selector("(//img[contains(@class,'relative h-full')])[3]")
        image_url3 = await result3.get_attribute("src")
        url3 = image_url3.replace(" ", "%20")
        urllib.request.urlretrieve(url3, './storage/3.webp')


def img_and_border():
    for i in range(4):
        backgroung_img = Image.open(f"./storage/{i}.webp")

        foreground_img = Image.open('./storage/ramka.png')
        crop_width = 600
        crop_height = 800
        img_width, img_height = backgroung_img.size
        lk = backgroung_img.crop(((img_width - crop_width) // 2,
                                  (img_height - crop_height) // 2,
                                  (img_width + crop_width) // 2,
                                  (img_height + crop_height) // 2))
        foreground_img = foreground_img.resize((lk.width, lk.height))
        lk.paste(foreground_img, (0, 0), foreground_img)
        lk.save(f'./storage/{i}.png')


def srift(txt):
    for i in range(4):
        img = Image.open(f'./storage/{i}.png')
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('arial.ttf', 20, encoding='UTF-8')
        w, h = draw.textsize(txt)
        a = 600
        draw.text(((a-w)/2, 10), txt, (255, 255, 255), font=font)
        img.save(f'./front/img/{i}.png')


def gen_img(imgB64, prompt, txt):
    asyncio.run(gen_imag(imgB64))
    asyncio.run(downloadurl(prompt))
    img_and_border()
    srift(txt)

