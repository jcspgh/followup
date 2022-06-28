from slack_sdk import WebClient


def respond_to_thread(web_client: WebClient, message: str, **kwargs):
    data = kwargs['data']
    web_client.chat_postMessage(
        channel=data['channel'],
        text=message,
        thread_ts=data['ts']
    )
