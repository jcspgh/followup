import logging
import os
import dateparser
from apscheduler.schedulers.background import BackgroundScheduler
from slack_sdk import WebClient
from flask import Flask, jsonify, request
from command_processor import CommandProcessor, parse_arguments, process_reminder

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(message)s'
)

s = BackgroundScheduler()

app = Flask(__name__)

command_parser = CommandProcessor()

client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])


@command_parser.add_command("followup")
@command_parser.add_argument("message")
@command_parser.add_argument("time")
def parse_followup_command(**kwargs):
    message, date = parse_arguments(kwargs['text'])

    timestamp = dateparser.parse(date)

    if timestamp:
        s.add_job(process_reminder, "date", run_date=timestamp, args=[message, client, kwargs['user_id']])

    return message, date


@app.route('/followup', methods=['POST'])
def followup_command():
    data = request.form
    message, _ = parse_followup_command(**data)
    payload = {'text': f'Got "{message}". I will remind you!'}
    return jsonify(payload)


def run():
    app.run(host='0.0.0.0', port=8080)


s.start()
run()
