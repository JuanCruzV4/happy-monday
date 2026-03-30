import datetime as dt
import random
import smtplib
import pandas
import requests
import os
import html

my_mail = os.environ.get("MY_MAIL")
password = os.environ.get("MY_PASSWORD")
my_lat = os.environ.get("MY_LAT")
my_lon = os.environ.get("MY_LON")
my_appid = os.environ.get("MY_APPID")

parameters = {
    "lat": my_lat,
    "lon": my_lon,
    "appid": my_appid,
    "cnt": 4
}

response = requests.get(url="https://api.openweathermap.org/data/2.5/forecast", params=parameters)
response.raise_for_status()

weather_data = response.json()

rain = False

for item in weather_data["list"]:
    condition_code = item["weather"][0]["id"]
    if condition_code < 700:
        rain = True

now = dt.datetime.now()
day_of_week = now.weekday()
data = pandas.read_csv("mails.csv")
mails_dict = {(data_row["name"], data_row["email"]): data_row for (index, data_row) in data.iterrows()}
if day_of_week == 0:
    with open("quotes.txt", "r", encoding="utf-8") as file:
        file = file.readlines()
        quote = random.choice(file)
        for clave, valor in mails_dict.items():
            try:
                if rain:
                    with smtplib.SMTP("smtp.gmail.com") as connection:
                        connection.starttls()
                        connection.login(user=my_mail, password=password)
                        connection.sendmail(
                            from_addr=my_mail,
                            to_addrs=clave[1],
                            msg=f"Subject:Monday Motivation to {clave[0]}\n\n{html.unescape(quote)}\n\n Hoy llueve! Llevate paraguas".encode("utf-8")
                        )
                else:
                     with smtplib.SMTP("smtp.gmail.com") as connection:
                        connection.starttls()
                        connection.login(user=my_mail, password=password)
                        connection.sendmail(
                            from_addr=my_mail,
                            to_addrs=clave[1],
                            msg=f"Subject:Monday Motivation to {clave[0]}\n\n{quote}".encode("utf-8")
                        )
            except Exception as e:
                print("Error sendind email",e)
else:
    if rain:
        for clave, valor in mails_dict.items():
            try:
                with smtplib.SMTP("smtp.gmail.com") as connection:
                    connection.starttls()
                    connection.login(user=my_mail, password=password)
                    connection.sendmail(
                        from_addr=my_mail,
                        to_addrs=clave[1],
                        msg=f"Subject:Ojota que hoy llueve\n\n Hoy llueve! Llevate paraguas".encode("utf-8")
                        )
            except Exception as e:
                print("Error sendind email",e)
    
