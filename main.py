import logging
import os
import re

import dateparser
from apscheduler.schedulers.background import BackgroundScheduler

from collections import defaultdict

from slack import RTMClient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(message)s'
)
BOT_ID = None

s = BackgroundScheduler()


def parse_arguments(data):
    return [word.strip('"') for word in re.findall('\".*?\"', data)]


class CommandProcessor(object):
    def __init__(self):
        self.handlers = []
        self.arguments = defaultdict(list)

    def add_command(self, pattern):
        def compile_handlers(function):
            self.handlers.append((re.compile(pattern), function))
            return function
        return compile_handlers

    def add_argument(self, arg_value):
        def compile_arguments(function):
            self.arguments[function].append(arg_value)
            return function
        return compile_arguments

    def process(self, command, kwargs):
        for regex, handler in self.handlers:
            matched = regex.search(command)
            if matched:
                if self.validate_arguments(regex.pattern, self.arguments[handler], **kwargs):
                    handler(**kwargs)
                return
        respond_to_thread("Command not recognized", **kwargs)

    @staticmethod
    def validate_arguments(command, expected_arguments, **kwargs):
        provided_arguments = parse_arguments(kwargs['data']['text'])

        if len(expected_arguments) != len(provided_arguments):
            error_message = f'Invalid format: -{command} '
            for argument in reversed(expected_arguments):
                error_message += f'[{argument}]'
            respond_to_thread(error_message, **kwargs)
            return False
        return True


def process_reminder(message, web_client, channel):
    web_client.chat_postMessage(
        channel=channel,
        text=message,
    )


command_parser = CommandProcessor()


@RTMClient.run_on(event="error")
def bot_connected(data: dict, **kwargs):
    print("ERROR", data, kwargs)


@RTMClient.run_on(event="open")
def bot_connected(data: dict, **kwargs):
    global BOT_ID
    BOT_ID = data['self']['id']
    print(BOT_ID)
    logging.info("Bot connected to the server")


@RTMClient.run_on(event='message')
def on_message(**kwargs):
    command = kwargs['data'].get("text", "")
    if command.startswith(f"!followup"):
        command_parser.process(command, kwargs)


@command_parser.add_command("followup")
@command_parser.add_argument("message")
@command_parser.add_argument("time")
def followup_command(**kwargs):
    web_client = kwargs['web_client']
    message, date = parse_arguments(kwargs['data']['text'])

    timestamp = dateparser.parse(date)

    s.add_job(process_reminder, "date", run_date=timestamp, args=[message, web_client, kwargs['data']['channel']])
    respond_to_thread("OK I will remind you!", **kwargs)


def respond_to_thread(message: str, **kwargs):
    web_client = kwargs['web_client']
    data = kwargs['data']
    web_client.chat_postMessage(
        channel=data['channel'],
        text=message,
        thread_ts=data['ts']
    )


if __name__ == "__main__":
    client = RTMClient(token=os.environ['SLACK_BOT_TOKEN'])
    s.start()
    client.start()
