"""
slack-alarm , 플랫폼팀 주간 업무 보고
"""
import requests
import sys
import json
import datetime
import schedule
import time


def send_message():
    # 생성한 웹훅 주소
    hook = 'https://hooks.slack.com/services/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'
    # 현재 '서비스_오류_노티' 채널로 메세지 전송 가게 구현 됨.

    message = ("\n " + datetime.datetime.now().strftime(
        # '* Date: [%m월%d일 %H:%M:%S]*\n'))
        '[ %m월%d일 ]\n'))

    # 메시지 전송
    slack_data = {
        "username": "alert-bot",                    # 보내는 사람 이름
        "icon_emoji": ":checkered_flag:",            # 사용할 emoji 정의
        "channel": "C0437NX2VPD",                   # 전송할 채널 아이디 -> hook 권한을 가진 Channel 이어야 함.
        "attachments": [
            {
                "color": "#4c4cff",
                "fields": [
                    {
                        "title": ':checkered_flag: 플랫폼팀 주간 업무보고',
                        "value": message,
                        "short": "false"
                    }
                ]
            }
        ]
    }

    byte_length = str(sys.getsizeof(slack_data))

    headers = {
        'Content-Type': "application/json",
        'Content-Length': byte_length
    }

    response = requests.post(hook, data=json.dumps(slack_data), headers=headers)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)

    print("Message sent. Clearing schedule.")
    schedule.clear('send_message_job')


job = schedule.every().monday.at("17:50").do(send_message)      # schedule 뒤에 요일 지정 후 + at 뒤에 시간 지정 하기!
job.tag('send_message_job')

while True:
    schedule.run_pending()
    time.sleep(1)
