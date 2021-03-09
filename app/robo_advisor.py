
import requests
import json 
import csv
import os

from matplotlib import pyplot as plt

from dotenv import load_dotenv
load_dotenv()


#from professor michael rozetti's project walkthrough
def to_usd(my_price): 
    return "${0:,.2f}".format(my_price)
    
#info inputs

global symbol
symbol = ""

symbol = input("Please input stock symbol here (EX: MSFT): ")
check_symbol = symbol.isalpha()

if len(symbol) < 1:
     print("Please enter a valid stock symbol.")  
     exit()
elif len(symbol) > 6:
     print("Please enter a valid stock symbol.")
     exit()
elif check_symbol == False:
     print("Please enter a valid stock symbol.")
     exit()

api_key = os.environ.get("ALPHAVANTAGE_API_KEY", "demo")

request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"

response = requests.get(request_url)
#print(type(response)) #response
#print(response.status_code) #200
#print(response.text) 

if "Error Message" in response.text:
     print("Symbol not found please try again.")
     exit()

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

#extra credit https://codinginfinite.com/data-visualizing-csv-format-chart-using-python-matplotlib/

with open(csv_file_path) as f:
    reader = csv.reader(f)
    header_row = next(reader)
    closes = []
    for row in reader:
        if row[4]=='':
            continue
        close = int(float(row[4]))
        closes.append(close)  #appending closing price 
    
    #Plot Data
    fig = plt.figure(dpi = 128, figsize = (10,6))
    plt.plot(closes, c = 'blue') #Line 1
    #Format Plot
    plt.title("Stock Prices Over Time", fontsize = 24)
    plt.xlabel("Time in Days",fontsize = 16)
    plt.ylabel("Price in USD", fontsize = 16)
    plt.tick_params(axis = 'both', which = 'major' , labelsize = 16)
    plt.show()

#recommendations

calc_buy = recent_low*1.15

if float(latest_close) <= float(calc_buy): 
     recommendation = "You should buy."
     recommendation_exp = "The latest close is less than or equal to 15% above the recent low."

else: 
     recommendation = "You should not buy."
     recommendation_exp = "The latest close is more than 15% above the recent low."

calc_sell = recent_high*.85

if float(latest_close) >= float(calc_sell): 
     recommendation_2 = "You should sell."
     recommendation_exp_2 = "The latest close is less than or equal to 15% below the recent high."

else: 
     recommendation_2 = "You should not sell."
     recommendation_exp_2 = "The latest close is more than 15% below the recent high."

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


print(f"If you are trying to buy: {recommendation}") # write code to determine whether the user should buy or sell
print(f"RECOMMENDATION REASON: {recommendation_exp}")
print(f"If you are trying to sell: {recommendation_2}")
print(f"RECOMMENDATION REASON: {recommendation_exp_2}") #This price is lower than the recent price low! or #This price is higher than the recent high, maybe you should wait


print("-------------------------")
print(f"WRITING DATA TO CSV: {csv_file_path}...")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")
