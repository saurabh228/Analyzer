from fastapi import FastAPI
import json
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

stock_companies = {
    'ADANIPORTS': 'Adani Ports',
    'ASIANPAINT': 'Asian Paints',
    'AXISBANK': 'Axis Bank',
    'BAJAJ-AUTO': 'Bajaj Auto',
    'BAJAJFINSV': 'Bajaj Finserv',
    'BAJFINANCE': 'Bajaj Finance',
    'BHARTIARTL': 'Bharti Airtel',
    'BRITANNIA': 'Britannia Industries',
    'BPCL': 'Bharat Petroleum',
    'COALINDIA': 'Coal India',
    'EICHERMOT': 'Eicher Motors',
    'DRREDDY': "Dr. Reddy's Laboratories",
    'GAIL': 'Gas Authority of India',
    'GRASIM': 'Grasim Industries',
    'CIPLA': 'Cipla Limited',
    'HCLTECH': 'HCL Technologies',
    'HDFCBANK': 'HDFC Bank',
    'HEROMOTOCO': 'Hero MotoCorp',
    'HINDUNILVR': 'Hindustan Unilever',
    'HINGALCO': 'Hindalco Industries',
    'ICIICIBANK': 'ICICI Bank',
    'INDUSINDBK': 'IndusInd Bank',
    'INFY': 'Infosys',
    'IOC': 'Indian Oil',
    'ITC': 'ITC Limited',
    'JSWSTEEL': 'JSW Steel',
    'KOTAKBANK': 'Kotak Mahindra Bank',
    'LT': 'Larsen & Toubro',
    'MARUTI': 'Maruti Suzuki',
    'MM': 'Mahindra & Mahindra',
    'NESTLEIND': 'Nestle India',
    'NTPC': 'NTPC Limited'
}

stokc_data = {}
with open('all_stocks.json') as f:
    stokc_data = json.load(f)

predictions = {}
with open('prediction.json') as f:
    predictions = json.load(f)

evaluation = {}
with open('eval.json') as f:
    evaluation = json.load(f)

@app.get("/stocks")
def read_stocks():
    return stock_companies

@app.get("/stocks/{stock_name}")
def read_stock(stock_name: str):
    return {
        "stock_companies": stock_companies,
        "actual_data": stokc_data.get(stock_name, {}).get('close', [])[-30:],
        "predictions": predictions.get(stock_name, [])[-30:],
        "evaluation": evaluation[stock_name],
        "dates": stokc_data.get(stock_name, {}).get('date', [])[-30:]
    }

@app.get("/")
def read_root():
    first_company = list(stock_companies.keys())[0]
    return {
        "stock_companies": stock_companies,
        "actual_data": stokc_data.get(first_company, {}).get('close', [])[-30:],
        "predictions": predictions.get(first_company, [])[-30:],
        "evaluation": evaluation[first_company],
        "dates": stokc_data.get(first_company, {}).get('date', [])[-30:]
    }
    

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}