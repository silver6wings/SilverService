import requests

access_token = '1779700159:AAFv085CpiwLMy98_88sch_Y8YLmF4yLWEo'

bot_token = 'bot' + access_token

host = 'https://api.telegram.org/'

junchao_id = 1870334527


def getUpdatesUrl() :
    return '%s%s/getUpdates' % (host, bot_token)


def getSendMessageUrl():
    return '%s%s/sendMessage' % (host, bot_token)


def sendMessage(text: str):
    post_data = {
        "chat_id": junchao_id,
        "text": text,
        "parse_mode": "Markdown"
    }

    res = requests.post(
        getSendMessageUrl(),
        data=post_data
    )
    print(res.text)
    return


if __name__ == '__main__':
    sendMessage('Hello world')