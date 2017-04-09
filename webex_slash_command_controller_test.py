import unittest
import mock
from flask import Flask, request, Response
from webex_slash_command_controller import WebexSlashCommandController

class WebexSlashCommandControllerTest(unittest.TestCase):
    __webex_slash_command_controller = None
    __app = Flask(__name__)
    WebexSlashCommandController.register(__app)

    def setUp(self):
        self.__webex_slash_command_controller = WebexSlashCommandController()
        self.__webex_slash_command_controller._WebexSlashCommandController__slack_token = 'slacktoken123'
        self.__webex_slash_command_controller._WebexSlashCommandController__slack_webhook_secret = 'token123'
        self.__webex_slash_command_controller._WebexSlashCommandController__webex_url = 'http://mycompany.webex.com'
        self.__webex_slash_command_controller._WebexSlashCommandController__slack__bot_user_name = 'mycompanybot'

    def test_command_mismatch(self):
        with self.__app.test_request_context():
            request.form = {
                'token': 'token123',
                'channel_id': 123,
                'user_name': 'krangaraju',
                'text': 'jalsdkaj'
            }

            raw_response = self.__webex_slash_command_controller.webex_slash_command_web_hook()
            response = self.__app.make_response(raw_response)

            self.assertEqual("200 OK", response.status)
            self.assertEqual("Usage: /webex start OR /webex join @slackuser", response.data)

    def test_token_mismatch(self):
        with self.__app.test_request_context():
            request.form = {
                'token': 'token234',
                'channel_id': 123,
                'user_name': 'krangaraju',
                'text': 'jalsdkaj'
            }

            raw_response = self.__webex_slash_command_controller.webex_slash_command_web_hook()
            response = self.__app.make_response(raw_response)

            self.assertEqual("200 OK", response.status)
            self.assertEqual("", response.data)

    def test_join_command(self):
        with self.__app.test_request_context():
            request.form = {
                'token': 'token123',
                'channel_id': 123,
                'user_name': 'krangaraju',
                'text': 'join @krangaraju'
            }

            raw_response = self.__webex_slash_command_controller.webex_slash_command_web_hook()
            response = self.__app.make_response(raw_response)

            self.assertEqual("200 OK", response.status)
            self.assertEqual("Click here to join krangaraju's webex room: http://mycompany.webex.com/krangaraju",
                             response.data)

    def test_start_command_in_direct_message(self):
        with self.__app.test_request_context():
            request.form = {
                'token': 'token123',
                'channel_id': 123,
                'channel_name': 'directmessage',
                'user_name': 'krangaraju',
                'text': 'start'
            }

            with mock.patch.object(self.__webex_slash_command_controller, '_WebexSlashCommandController__send_message') \
                    as mock_send_message:
                raw_response = self.__webex_slash_command_controller.webex_slash_command_web_hook()
                response = self.__app.make_response(raw_response)

                mock_send_message.assert_called_once_with(123, "@krangaraju has started a webex session. "
                                                               "Join: http://mycompany.webex.com/krangaraju")
                self.assertEqual("200 OK", response.status)
                self.assertEqual("", response.data)

    def test_start_command_in_channel(self):
        with self.__app.test_request_context():
            request.form = {
                'token': 'token123',
                'channel_id': 123,
                'channel_name': 'testchannel',
                'user_name': 'krangaraju',
                'text': 'start'
            }

            with mock.patch.object(self.__webex_slash_command_controller, '_WebexSlashCommandController__send_message') \
                    as mock_send_message:
                raw_response = self.__webex_slash_command_controller.webex_slash_command_web_hook()
                response = self.__app.make_response(raw_response)

                mock_send_message.assert_called_once_with(123, "<!here> @krangaraju has started a webex session. "
                                                               "Join: http://mycompany.webex.com/krangaraju")
                self.assertEqual("200 OK", response.status)
                self.assertEqual("", response.data)

if __name__ == '__main__':
    unittest.main()