from flask import Flask, request, jsonify
import requests
import datetime
import threading
import time

app = Flask(__name__)

TELEGRAM_TOKEN = '7907772455:AAGGwFsj4yO0gc9hiIeyG6R9pXFW9z7xQcg'
CHAT_ID = '6045736248'  # Замени на свой chat_id

# Пример данных для хранения количества Pomodoro циклов
pomodoro_data = {}

def save_pomodoro_count(day, count):
    pomodoro_data[day] = count

def get_yesterday_count():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    return pomodoro_data.get(yesterday.strftime("%Y-%m-%d"), 0)

def get_weekly_average():
    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=7)
    weekly_counts = [pomodoro_data.get((week_ago + datetime.timedelta(days=i)).strftime("%Y-%m-%d"), 0) for i in range(7)]
    return sum(weekly_counts) / len(weekly_counts) if weekly_counts else 0

def send_daily_report():
    today = datetime.date.today().strftime("%Y-%m-%d")
    today_count = pomodoro_data.get(today, 0)
    yesterday_count = get_yesterday_count()
    weekly_avg = get_weekly_average()

    message = (
        f"Сегодняшние Pomodoro циклы: {today_count}\n"
        f"Разница с вчера: {today_count - yesterday_count}\n"
        f"Среднее за неделю: {weekly_avg:.2f}"
    )

    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    requests.post(url, data={'chat_id': CHAT_ID, 'text': message})

def send_weekly_report():
    today = datetime.date.today()
    week_ago = today - datetime.timedelta(days=7)
    last_week = week_ago - datetime.timedelta(days=7)

    current_week_counts = sum(pomodoro_data.get((week_ago + datetime.timedelta(days=i)).strftime("%Y-%m-%d"), 0) for i in range(7))
    last_week_counts = sum(pomodoro_data.get((last_week + datetime.timedelta(days=i)).strftime("%Y-%m-%d"), 0) for i in range(7))

    message = (
        f"Pomodoro циклы за эту неделю: {current_week_counts}\n"
        f"Разница с прошлой неделей: {current_week_counts - last_week_counts}"
    )

    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    requests.post(url, data={'chat_id': CHAT_ID, 'text': message})

@app.route('/save-pomodoro', methods=['POST'])
def save_pomodoro():
    data = request.json
    day = data['date']
    count = data['count']
    save_pomodoro_count(day, count)
    return jsonify({'status': 'success'})

@app.route('/notify_id', methods=['POST'])
def notify_id():
    data = request.json
    chat_id = data['tgid']
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    text = 'ID успешно сохранён!'
    requests.post(url, data={'chat_id': chat_id, 'text': text})
    return 'ok'

def schedule_reports():
    while True:
        now = datetime.datetime.now()
        if now.hour == 22:  # 18:00 каждый день
            send_daily_report()
        if now.weekday() == 6 and now.hour == 22:  # Воскресенье, 18:00
            send_weekly_report()
        time.sleep(3600)  # Проверка каждый час

if __name__ == '__main__':
    # Запуск планировщика в отдельном потоке
    threading.Thread(target=schedule_reports, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)
