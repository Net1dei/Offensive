from playwright.sync_api import Page
from playwright.sync_api import sync_playwright
import time
def downloadurl(prompt):
    with sync_playwright() as p: 
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://imgcreator.zmo.ai/tools/background-changer")
        page.set_input_files("input[type='file']", 'test.jpg')
        time.sleep(10)
        page.get_by_role("textbox", name="Email*").fill('forvpngame069@gmail.com')
        page.get_by_role("textbox", name="Password*").fill('Trof9911')
        page.locator("(//div[contains(@class,'bg-primary cursor-pointer')])[1]").click()
        time.sleep(2)
        page.mouse.click(410, 85)
        page.get_by_placeholder("Describe the image you want to see").fill(prompt)
        page.mouse.click(254, 413)
        time.sleep(40)

        all_images = page.query_selector("(//img[contains(@class,'relative h-full')])[1]")
        image_url = all_images.get_attribute("src")
        all_images1 = page.query_selector("(//img[contains(@class,'relative h-full')])[2]")
        image_url1 = all_images1.get_attribute("src")
        all_images2 = page.query_selector("(//img[contains(@class,'relative h-full')])[3]")
        image_url2 = all_images2.get_attribute("src")
        all_images3 = page.query_selector("(//img[contains(@class,'relative h-full')])[4]")
        image_url3 = all_images3.get_attribute("src")
    return(image_url)#,'\n',image_url1,'\n',image_url2,'\n',image_url3)



