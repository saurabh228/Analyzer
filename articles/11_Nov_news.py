import csv
import json
import time
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

optionsE = webdriver.EdgeOptions()
optionsE.page_load_strategy = 'eager'
optionsE.add_argument("--headless")
optionsE.add_argument("--log-level=3")
optionsE.add_argument("--no-sandbox")
# Initialize the browser
driver = webdriver.Edge(options=optionsE)

for d in range(28, 31):
    print(d)
    with open('etLinks.json', 'r') as file:
        links_data = json.load(file)
    links = links_data["2021"]["nov"][str(d)]

    # if d == 12:
    #     i=260
    # else:
    i=1
    # j=0
    # for link in links:
    for link in tqdm(links, desc="Processing links", unit="link"):
        # j+=1
        # if d == 12 and j < 266:
        #     continue

        driver.get(link)
        article_section = None
        try:
            article_section = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='pageContent flt']"))
            )
        except Exception as e:
            # with open('errors.txt', 'a') as file:
            #     file.write("error in pageContent: "+str(e)+"\nat: "+ link+"\n\n")
            # print("\npageContent not found in")
            continue
        article = {}

        try:
            # synopsys = article_section.find_element(by=By.XPATH, value="//div[@class='artSyn bgPink']")
            news = article_section.find_element(by=By.XPATH, value="//div[@class='artText medium']")

            try:
                news_text = news.text + " "
                news_text = news_text.replace("(You can now subscribe to our Economic Times WhatsApp channel)", "")
                news_text = news_text.replace(".\n\n\n\n\n\n\n\n\n\n", ". ").replace(".\n\n\n\n\n\n\n\n\n", ". ").replace(".\n\n\n\n\n\n\n\n", ". ").replace(".\n\n\n\n\n\n\n", ". ").replace(".\n\n\n\n\n\n", ". ").replace(".\n\n\n\n\n", ". ").replace(".\n\n\n\n", ". ").replace(".\n\n\n", ". ").replace(".\n\n", ". ").replace(".\n", ". ").replace("\n\n\n\n\n\n\n\n\n\n", ". ").replace("\n\n\n\n\n\n\n\n\n", ". ").replace("\n\n\n\n\n\n\n\n", ". ").replace("\n\n\n\n\n\n\n", ". ").replace("\n\n\n\n\n\n", ". ").replace("\n\n\n\n\n", ". ").replace("\n\n\n\n", ". ").replace("\n\n\n", ". ").replace("\n\n", ". ").replace("\n", ". ")
                
                if news_text.strip() == "":
                    continue
                article["news"] = news_text
            except Exception as e:
                # with open('errors.txt', 'a') as file:
                #     file.write("error occurred in news segment:\n"+str(e)+"\n\n")
                # print("\nerror occurred in news segment")
                continue
        except Exception as e:
            # with open('errors.txt', 'a') as file:
            #     file.write("error in artText medium: "+str(e)+"\nat: "+link+"\n\n")
            # print("\nerror in artText medium")
            continue
        
        
        article["link"] = link

        with open('etArticles6.json', 'r') as file:
            articles = json.load(file)

        if "2021" not in articles:
            articles["2021"] = {}
        if "nov" not in articles["2021"]:
            articles["2021"]["nov"] = {}
        if str(d) not in articles["2021"]["nov"]:
            articles["2021"]["nov"][str(d)] = {}

        articles["2021"]["nov"][str(d)][str(i)] = article
        i+=1
        with open('etArticles6.json', 'w') as file:
            json.dump(articles, file, indent=4)

input("Press Enter to close the browser...")
