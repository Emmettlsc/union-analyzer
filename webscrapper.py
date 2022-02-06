import requests
from bs4 import BeautifulSoup



URL = "https://www.britannica.com/topic/list-of-cities-and-towns-in-the-United-States-2023068"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find_all("a", {"class": "md-crosslink"})

for i in range(len(results)):
	results[i] = results[i].text

print(results)
