import openai
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from src.parameters import OPENAI_API_KEY
from src.utils import *


#настройка llama2
options=webdriver.EdgeOptions()
options.add_argument('--ignore-certificate-errors-spki-list')
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs",prefs)


#настройка gpt
openai.api_key = OPENAI_API_KEY




def generate_text_gpt(prompt):
  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "user", "content": prompt}
    ]
  )
  text=completion.choices[0].message.content
  return(text)



def generate_text_llama2(prompt):
    try:
        options.headless=True
        driver = webdriver.Edge(options)
        driver.get('https://huggingface.co/chat/')
        time.sleep(2)
        elText = driver.find_element(By.TAG_NAME,"textarea")
        elText.send_keys(prompt)
        ActionChains(driver) \
        .key_down(Keys.ENTER) \
        .key_up(Keys.ENTER) \
        .perform()
        time.sleep(2)
        elTextPast=""
        elText = driver.find_element(By.XPATH,"//div[contains(@class,'relative min-h-[calc(2rem+theme(spacing[3.5])*2)]')]")
        while elText.text!=elTextPast:
            elTextPast=elText.text
            elText = driver.find_element(By.XPATH,"//div[contains(@class,'relative min-h-[calc(2rem+theme(spacing[3.5])*2)]')]")
            time.sleep(1)
        if elText.text==None:
            return("wrong reqest")
        text=elText.text
        
        return(translateRU(text))
    
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()



def generate_text(prompt, chat='gpt'):
  print('____________1__________________')
  if chat=='gpt':
    text=generate_text_gpt(prompt)
  elif chat=='llama2':
    prompt=translateEN(prompt)
    text=generate_text_llama2(prompt)
  print(text)
  return(text)

