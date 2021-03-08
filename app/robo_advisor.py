
import requests
import json 
import csv
import os


from dotenv import load_dotenv
load_dotenv()


#from professor michael rozetti's project walkthrough
def to_usd(my_price): 
    return "${0:,.2f}".format(my_price)
    

#info inputs

global symbol
symbol = ""
symbol = input("Please input stock symbol here (EX: MSFT): ")

api_key = os.environ.get("ALPHAVANTAGE_API_KEY", "demo")

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"


response = requests.get(request_url)
#print(type(response)) #response
#print(response.status_code) #200
#print(response.text) 

parsed_response = json.loads(response.text)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"] 

tsd = parsed_response["Time Series (Daily)"]

dates = list(tsd.keys())

latest_day = dates[0] #first item in dates' list

latest_close = tsd[latest_day]["4. close"]

#maximum of all high prices 
high_prices = []
low_prices = []

for date in dates:
    high_price = tsd[date]["2. high"]
    low_price = tsd[date]["3. low"]
    high_prices.append(float(high_price))
    low_prices.append(float(low_price))
recent_high = max(high_prices)
recent_low = min(low_prices)

#csv_file_path = "data/prices.csv" # a relative filepath

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")


csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]
with open(csv_file_path, "w") as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
    writer.writeheader() # uses fieldnames set above

    for date in dates: 
         daily_prices = tsd[date]

         writer.writerow({
            "timestamp": date,
            "open": daily_prices["1. open"],
            "high": daily_prices["2. high"],
            "low": daily_prices["3. low"],
            "close": daily_prices["4. close"],
            "volume": daily_prices["5. volume"]
         })

#info outputs 

print("-------------------------")
print(f"SELECTED SYMBOL: {symbol} ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")

print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")

print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print("RECOMMENDATION: BUY!") # write code to determine whether the user should buy or sell
print("RECOMMENDATION REASON: TODO") #This price is lower than the recent price low! or #This price is higher than the recent high, maybe you should wait
print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path}...")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")
