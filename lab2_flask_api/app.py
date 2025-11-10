from flask import Flask, request, jsonify, Response
import requests
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

# [Easy] Простий сервер
@app.route('/')
def hello_world():
    return "Hello World!"

# [Easy-Medium] GET з параметрами
@app.route('/currency')
def get_currency_static():
    # Отримуємо параметри запиту
    key = request.args.get('key', 'no-key')
    today = request.args.get('today')
    if today:
        return f"USD - 41.5 (key={key})"
    return "No valid parameter provided"

# [Medium] Обробка заголовків
@app.route('/headers')
def handle_headers():
    content_type = request.headers.get('Content-Type', '')
    data = {"currency": "USD", "rate": 41.5}

    if content_type == "application/json":
        return jsonify(data)
    elif content_type == "application/xml":
        xml = f"<data><currency>{data['currency']}</currency><rate>{data['rate']}</rate></data>"
        return Response(xml, mimetype='application/xml')
    else:
        return f"Currency: {data['currency']}, Rate: {data['rate']}"

# [Medium-Hard] Отримання курсу з API НБУ
@app.route('/currency_dynamic')
def get_currency_dynamic():
    param = request.args.get('param')
    base_url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=USD&json"

    if param == "today":
        url = base_url
    elif param == "yesterday":
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
        url = f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=USD&date={yesterday}&json"
    else:
        return "Invalid param. Use 'today' or 'yesterday'."

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()[0]
        return f"{data['exchangedate']}: {data['cc']} - {data['rate']}"
    else:
        return "Error fetching data from NBU"

# [Hard] POST запит – збереження у файл
@app.route('/save_text', methods=['POST'])
def save_text_to_file():
    text_data = request.data.decode('utf-8')
    with open('data.txt', 'a', encoding='utf-8') as f:
        f.write(text_data + '\n')
    return "Data saved to file"

# [Hard2] POST запит – збереження у базу SQLite
@app.route('/save_db', methods=['POST'])
def save_to_db():
    text_data = request.data.decode('utf-8')
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, text TEXT, created TIMESTAMP)''')
    c.execute('INSERT INTO messages (text, created) VALUES (?, ?)', (text_data, datetime.now()))
    conn.commit()
    conn.close()
    return "Data saved to database"

if __name__ == '__main__':
    app.run(port=8000)
