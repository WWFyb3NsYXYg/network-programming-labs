import requests
from datetime import datetime, timedelta
import json
import os

today = datetime.today()
week_ago = today - timedelta(days=7)

start = week_ago.strftime("%Y%m%d")
end = today.strftime("%Y%m%d")

url = (
    f"https://bank.gov.ua/NBU_Exchange/exchange_site?"
    f"start={start}&end={end}&valcode=usd&sort=exchangedate&order=asc&json"
)

print("→ Отримання курсу USD за останній тиждень...")
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    os.makedirs("results", exist_ok=True)
    with open("results/usd_rates.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    for record in data:
        print(f"{record['exchangedate']}: {record['rate']} грн")
else:
    print("Помилка запиту:", response.status_code)
