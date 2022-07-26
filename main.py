import logging
import os
import dateparser
from apscheduler.schedulers.background import BackgroundScheduler
from slack_sdk import WebClient
from flask import Flask, jsonify, request, make_response
from command_processor import CommandProcessor, parse_arguments, process_reminder
from slack_sdk.errors import SlackApiError
import json

from views.followup_view import generate_followup_view

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

s = BackgroundScheduler()

app = Flask(__name__)

command_parser = CommandProcessor()

client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])


@command_parser.add_command("followup")
@command_parser.add_argument("message")
@command_parser.add_argument("time")
def parse_followup_command(date, time, text, timezone="UTC", **kwargs):

    # TODO: Account for timezones
    timestamp = dateparser.parse(date + " " + time, settings={"TIMEZONE": timezone})

    if timestamp:
        s.add_job(
            process_reminder,
            "date",
            run_date=timestamp,
            timezone=timezone,
            args=[text, client, kwargs["user"]["id"]],
        )

        return

    raise Exception("Problem occurred while processing command")


@app.route("/followup", methods=["POST"])
def followup_command():
    data = request.form
    if data:
        payload = json.loads(data.get("payload", "{}"))
        if not payload:
            if not data.get("type"):
                trigger_id = data["trigger_id"]
                # Open a new modal by a global shortcut
                try:
                    api_response = client.views_open(
                        trigger_id=trigger_id, view=generate_followup_view()
                    )
                    return make_response("", 200)
                except SlackApiError as e:
                    code = e.response["error"]
                    return make_response(f"Failed to open a modal due to {code}", 200)
        elif (
                payload["type"] == "view_submission"
                and payload["view"]["callback_id"] == "followup-modal"
        ):
            # Handle a data submission request from the modal
            # {'followup': {'datepicker-action': {'type': 'datepicker', 'selected_date': '2022-07-22'}},
            # 'time_section': {'timepicker': {'type': 'timepicker', 'selected_time': '11:40'}},
            # 'text_input': {'plain_text_input-action': {'type': 'plain_text_input', 'value': 'asdasd'}}}
            submitted_data = payload["view"]["state"]["values"]

            user_id = payload["user"]["id"]
            response = client.users_info(user=user_id, include_locale=True)

            date = submitted_data["followup-datepicker"]["datepicker-action"][
                "selected_date"
            ]
            time = submitted_data["time_section"]["timepicker"]["selected_time"]
            text = submitted_data["text_input"]["plain_text_input-action"]["value"]

            parse_followup_command(
                date, time, text, timezone=response["user"]["tz"], **payload
            )

            # Close this modal with an empty response body
            return make_response("", 200)
        elif payload["type"] == "block_actions":
            return make_response("", 200)

    return make_response("Meep", 500)


@command_parser.add_command("followup")
@command_parser.add_argument("message")
@command_parser.add_argument("time")
def parse_old_followup_command(**kwargs):
    message, date = parse_arguments(kwargs["text"])

    timestamp = dateparser.parse(date)

    if timestamp:
        s.add_job(
            process_reminder,
            "date",
            run_date=timestamp,
            args=[message, client, kwargs["user_id"]],
        )

    return message, date


@app.route("/followup/old", methods=["POST"])
def followup_command_old():
    data = request.form
    message, _ = parse_old_followup_command(**data)
    payload = {"text": f'Got "{message}". I will remind you!'}
    return jsonify(payload)


def run():
    app.run(host="0.0.0.0", port=8080)


s.start()
run()
