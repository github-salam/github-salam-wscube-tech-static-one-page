import requests
from bs4 import BeautifulSoup
import pandas as pd


res = requests.get("https://webscraper.io/test-sites/e-commerce/allinone/computers/tablets")

soup = BeautifulSoup(res.text, "lxml")

titles = soup.find_all('a',class_ = "title")
title_list = []

for t in titles:
    title_list.append(t.text)

prices = soup.find_all("h4", {"class": "price float-end card-title pull-right"})
price_list = []

print("\n")

for p in prices:
    price_list.append(p.text)

descriptions = soup.find_all("p", class_ = "description card-text")
description_list = [d.text for d in descriptions]

ratings = soup.find_all("p", class_ = "review-count float-end")
rating_list = [r.text for r in ratings]

df = pd.DataFrame({"Titles ": title_list, "Description ": description_list, "Review ": rating_list, "Price ": price_list})

print(df)

df.to_csv("data.csv", index=False)