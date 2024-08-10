# import nltk
# nltk.download('averaged_perceptron_tagger')
import json
from tqdm import tqdm
from textblob import TextBlob
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer



entities = {}
with open("entities.json", "r") as file:
    for type, entity_dict in json.load(file).items():
        entities.update(entity_dict)

# Function to calculate sentiment score using TextBlob
def calculate_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    return sentiment_score

def find_entities(text, entities):
    
    text = text.lower()

    found_entities = {}
    i=0
    while i < len(text):
        entity_found = False
        for entity, synonyms in entities.items():
            entity_found = False
            for synonym in synonyms:
                if text[i:].startswith(synonym):
                    if text[i+len(synonym)].isalpha():
                        continue
                    y = text.find(". ", i)
                    if y == -1:
                        y = len(text) - 2
                    x = text.rfind(". ", 0, i)
                    if x == -1:
                        x = 0
                    else:
                        x+=2
                    found_entities[entity] = text[x:y+1]
                    i += len(synonym)
                    entity_found = True
                    break
            if entity_found:
                break
        if entity_found:
            i+=1
        else:
            next_i = text.find(" ", i)
            if next_i == -1:
                break
            i = next_i+1
        
    return found_entities

with open("articles/etArticles.json", "r") as file:
    articles = json.load(file)
    
for year, months in articles.items():
    print(year)
    for month, days in months.items():
        print("  "+str(month))
        # for day, indices in tqdm(days.items(), desc="Processing Sentiment", unit="Articles"):
        for day, indices in days.items():
            print("    day",day)
            # for index, news in indices.items():
            prev_text = None
            for index, news in tqdm(indices.items(), desc="    Processing...", unit=' Articles'):
                text = news["news"]
                if text.strip() == "" or (prev_text != None and text.strip() == prev_text):
                    continue
                found_entities = find_entities(text,  entities)
                
                for entity, news in found_entities.items():
                    found_entities[entity] = round(calculate_sentiment(news)*5, 2)
                
                with open("output.json", "r") as file:
                    output = json.load(file)
                if year not in output:
                    output[year] = {}
                if month not in output[year]:
                    output[year][month] = {}
                if day not in output[year][month]:
                    output[year][month][day] = {}
                # found_entities["news"] = text
                output[year][month][day][index] = found_entities
                with open("output.json", "w") as file:
                    json.dump(output, file)

print("Done!!")

# python sntmnt 
        

