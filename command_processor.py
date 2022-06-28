from collections import defaultdict
import re

from utils.responses import respond_to_thread


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


def parse_arguments(data):
    return [re.sub('[\"“”]', '', word) for word in re.findall('[”“\"].*?[\"“”]', data)]


def process_reminder(message, web_client, channel):
    web_client.chat_postMessage(
        channel=channel,
        text=message,
    )
