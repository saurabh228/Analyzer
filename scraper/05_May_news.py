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


for d in range(14, 32):
    print(d)

    with open('etLinks.json', 'r') as file:
        links_data = json.load(file)
    links = links_data["2021"]["may"][str(d)]

    # if d == 14:
    #     i=270
    # else:
    i=1
    # j=0
    # for link in links:
    for link in tqdm(links, desc="Processing links", unit="link"):
        # j+=1
        # if d == 14 and j < 280:
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
            # print("\npageContent not found in:\n"+link)
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
                # print("\nsummary not found in:\n"+link)
                continue
        except Exception as e:
            # with open('errors.txt', 'a') as file:
            #     file.write("error in artText medium: "+str(e)+"\nat: "+link+"\n\n")
            # print("\nartSyn not found in:\n"+link)
            continue
        
        
        article["link"] = link

        with open('etArticles.json', 'r') as file:
            articles = json.load(file)

        if "2021" not in articles:
            articles["2021"] = {}
        if "may" not in articles["2021"]:
            articles["2021"]["may"] = {}
        if str(d) not in articles["2021"]["may"]:
            articles["2021"]["may"][str(d)] = {}

        articles["2021"]["may"][str(d)][str(i)] = article
        i+=1
        with open('etArticles.json', 'w') as file:
            json.dump(articles, file, indent=4)

input("Press Enter to close the browser...")
