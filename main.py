import smtplib
import requests
import lxml
from bs4 import BeautifulSoup
import os

USER_AGENT=os.environ["USER_AGENT"]
ACCEPT_LANG="en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7"
URL=os.environ["URL"]
USER_NAME=os.environ["user_name"]
PASSWORD=os.environ["PASSWORD"]


header = {
    "User-Agent": USER_AGENT,
    "Accept-Language": ACCEPT_LANG
}

response = requests.get(URL, headers=header)

soup = BeautifulSoup(response.content, "lxml")
# print(soup.prettify())

price = soup.find(class_="a-offscreen").get_text()
title=soup.find(id="productTitle").get_text()
price_without_currency = price.split("$")[1]
price_as_float = float(price_without_currency)
# print(price_as_float)
# print(title)



if price_as_float< 100:
    message=f"{title}is now {price}"
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=USER_NAME, password=PASSWORD)
        connection.sendmail(from_addr=USER_NAME,
                            to_addrs="TO_ADDRESS",
                            msg=f"subject: Amazon Price Alert!! \n\n{message}\ntrack your product :{URL}".encode("utf-8")
                            )