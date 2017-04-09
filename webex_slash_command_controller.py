import os
import re
from flask import request, Response
from slackclient import SlackClient
from flask_classy import FlaskView, route
from urlparse import urljoin

class WebexSlashCommandController(FlaskView):
    route_base = '/'

    __slack_token = os.environ.get('SLACK_TOKEN')
    __slack_webhook_secret = os.environ.get('SLACK_WEBHOOK_SECRET')
    __webex_url = os.environ.get('ENTERPRISE_WEBEX_URL')
    __bot_user_name = os.environ.get('SLACK_BOT_USER_NAME')

    __join_regex = re.compile("[jJ]oin @.*")
    __start_regex = re.compile("[sS]tart")

    __slack_client = SlackClient(__slack_token)

    @route('/webex_slash_command_web_hook', methods=['POST'])
    def webex_slash_command_web_hook(self):
        if request.form.get('token') == self.__slack_webhook_secret:
            channel_id = request.form.get('channel_id')
            slash_command_user_name = request.form.get('user_name')
            text = request.form.get('text')

            if self.__join_regex.match(text):
                webex_host_user_name = text.split("@")[1]
                return Response("Click here to join " + webex_host_user_name + "'s webex room: "
                                + urljoin(self.__webex_url, webex_host_user_name)), 200

            elif self.__start_regex.match(text):
                message = ''
                channel_name = request.form.get('channel_name')
                if channel_name != "directmessage":
                    message += "<!here> "

                message += "@" + slash_command_user_name + " has started a webex session. Join: " \
                        + urljoin(self.__webex_url, slash_command_user_name)
                self.__send_message(channel_id, message)
                return Response(), 200

            else:
                return Response("Usage: /webex start OR /webex join @slackuser"), 200

        return Response(), 200

    def __send_message(self, channel_id, message):
        self.__slack_client.api_call("chat.postMessage", channel=channel_id,
                              text=message, username=self.__bot_user_name)