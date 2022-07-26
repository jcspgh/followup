from datetime import datetime

def generate_followup_view():
    return {
        "type": "modal",
        "callback_id": "followup-modal",
        "title": {"type": "plain_text", "text": "Followup", "emoji": True},
        "submit": {"type": "plain_text", "text": "Submit", "emoji": True},
        "close": {"type": "plain_text", "text": "Cancel", "emoji": True},
        "blocks": [
            {
                "type": "section",
                "block_id": "followup-datepicker",
                "text": {"type": "mrkdwn", "text": "Pick a date for the reminder."},
                "accessory": {
                    "type": "datepicker",
                    "initial_date": datetime.now().strftime("%Y-%m-%d"),
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a date",
                        "emoji": True,
                    },
                    "action_id": "datepicker-action",
                },
            },
            {
                "type": "section",
                "block_id": "time_section",
                "text": {"type": "mrkdwn", "text": "Pick a time for the reminder."},
                "accessory": {
                    "type": "timepicker",
                    "action_id": "timepicker",
                    "initial_time": "11:40",
                    "placeholder": {"type": "plain_text", "text": "Select a time"},
                },
            },
            {
                "type": "input",
                "block_id": "text_input",
                "element": {
                    "type": "plain_text_input",
                    "multiline": True,
                    "action_id": "plain_text_input-action",
                },
                "label": {
                    "type": "plain_text",
                    "text": "Reminder Message",
                    "emoji": True,
                },
            },
        ],
    }
