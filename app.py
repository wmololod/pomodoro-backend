from flask import Flask, request
import requests

app = Flask(__name__)

TELEGRAM_TOKEN = 'ВАШ_ТОКЕН_БОТА'

@app.route('/notify_id', methods=['POST'])
def notify_id():
    data = request.json
    chat_id = data['tgid']
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    text = 'ID успешно сохранён!'
    requests.post(url, data={'chat_id': chat_id, 'text': text})
    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
