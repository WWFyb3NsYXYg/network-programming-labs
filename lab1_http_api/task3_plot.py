import json
import matplotlib.pyplot as plt

with open("results/usd_rates.json", "r", encoding="utf-8") as f:
    data = json.load(f)

dates = [item["exchangedate"] for item in data]
rates = [item["rate"] for item in data]

plt.figure(figsize=(8, 5))
plt.plot(dates, rates, marker="o")
plt.title("Динаміка курсу USD за останній тиждень (НБУ)")
plt.xlabel("Дата")
plt.ylabel("Курс, грн")
plt.grid(True)
plt.tight_layout()
plt.savefig("results/usd_plot.png")
plt.show()
