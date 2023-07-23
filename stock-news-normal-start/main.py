import requests
import datetime
from twilio.rest import Client

account_sid = 'AC86fb88996cf76537790175f9a149a189'
auth_token = 'd63dbd107c7407f322fc692dbdd6f0ae'
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_APIKEY = 'K7PNFAWFN8F86SDG'
NEWS_APIKEY = '1aa42b8fbb0e4b8ba7021d2760417661'

yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
formatted_yesterday = yesterday.strftime('%Y-%m-%d')
day_before = datetime.datetime.today() - datetime.timedelta(days=2)
formatted_day_before = day_before.strftime('%Y-%m-%d')
print(formatted_yesterday)
print(formatted_day_before)
stock_parameter = {'apikey': STOCK_APIKEY,
                   'symbol': STOCK_NAME,
                   'function': 'TIME_SERIES_DAILY'}
news_parameter = {'apiKey': NEWS_APIKEY,
                  'q': COMPANY_NAME,
                  'language': 'en'}

all_news = requests.get(NEWS_ENDPOINT, params=news_parameter)
all_news.raise_for_status()
news = all_news.json()['articles'][:-4:-1]
list_of_title = [article['title'] for article in news]
list_of_description = [article['description'] for article in news]

response = requests.get(STOCK_ENDPOINT, params=stock_parameter)
response.raise_for_status()
data = response.json()['Time Series (Daily)']
yesterday_closed_at = float(data[formatted_yesterday]['4. close'])
day_before_closed_at = float(data[formatted_day_before]['4. close'])
difference = abs(yesterday_closed_at - day_before_closed_at)
difference_percentage = (difference / 100) * yesterday_closed_at


def messages(i):
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body=f"{STOCK_NAME}: {int(difference_percentage)}%\nHeadline: {list_of_title[i]}\nBrief: {list_of_description[i]}",
        from_="+15393287787",
        to='+916392543054'
    )
    print(message.sid)


if difference_percentage > 5:
    for i in range(0, 3):
        messages(i)

    ## STEP 2: https://newsapi.org/
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

# TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.

# TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation


## STEP 3: Use twilio.com/docs/sms/quickstart/python
# to send a separate message with each article's title and description to your phone number.

# TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.

# TODO 9. - Send each article as a separate message via Twilio.


# Optional TODO: Format the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
