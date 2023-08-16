from playwright.sync_api import Page
from playwright.async_api import async_playwright
import time
import asyncio
import urllib.request 
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

def create_txt(imgB64):
    with open("./storage/a.txt", "a") as file:
        file.write(f"{imgB64}")
    lll = open('./storage/a.txt', 'r') 
    www = lll.read()
    return(www)

async def gen_imag():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://snipp.ru/tools/base64-img-decode")
        await page.locator("//textarea[@class='snp-form-textarea font-pre']").fill(create_txt())
        time.sleep(15)
        await page.get_by_role('button').click()

        async with page.expect_download() as download_info:
            await page.locator("//div[@id='fid-result-img']//a[1]").click()
        download = await download_info.value
        print(await download.path())
        await download.save_as("./storage/1.jpg")  
    
async def downloadurl(prompt):
    async with async_playwright() as p: 
        browser = await p.firefox.launch(headless=False)
        page = await browser.new_page()
        await page.goto("https://imgcreator.zmo.ai/tools/background-changer")
        await page.set_input_files("input[type='file']", './storage/1.jpg')
        await page.get_by_role("textbox", name="Email*").fill('kekw171@outlook.com')
        await page.get_by_role("textbox", name="Password*").fill('Trof9911')
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
                result = await page.query_selector("(//img[contains(@class,'relative h-full')])[1]")
            except:
                pass

        image_url = await result.get_attribute("src") 
        url = image_url.replace(" ", "%20")
        urllib.request.urlretrieve(url, './storage/2.webp')  

def img_and_border():
    backgroung_img = Image.open("./storage/2.webp")

    foreground_img=Image.open('./storage/ramka.png')
    crop_width = 600
    crop_height = 800
    img_width, img_height = backgroung_img.size
    lk = backgroung_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))
    foreground_img = foreground_img.resize((lk.width, lk.height))
    lk.paste(foreground_img, (0,0), foreground_img)
    lk.save('./storage/3.png')

def srift(txt):
    img = Image.open('./storage/3.png')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('arial.ttf', 20, encoding='UTF-8')
    w, h = draw.textsize(txt)
    a = 600
    draw.text(((a-w)/2, 10), txt, (255, 255, 255), font=font)
    img.save('./storage/3.png')

def gen_img(imgB64, prompt, txt):
    create_txt(imgB64=imgB64)
    asyncio.run(gen_imag())
    asyncio.run(downloadurl(prompt=prompt))
    img_and_border()
    srift(txt=txt)
