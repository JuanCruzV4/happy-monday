import datetime as dt
import random
import smtplib
import pandas
import os

my_mail = os.environ.get("MY_MAIL")
password = os.environ.get(MY_PASSWORD")

now = dt.datetime.now()
day_of_week = now.weekday()
data = pandas.read_csv("mails.csv")
mails_dict = {(data_row["name"], data_row["email"]): data_row for (index, data_row) in data.iterrows()}
if day_of_week == 3:
    with open("quotes.txt", "r", encoding="utf-8") as file:
        file = file.readlines()
        quote = random.choice(file)
        for clave, valor in mails_dict.items():
            try:
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
