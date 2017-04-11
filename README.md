# slack-webex-python-plugin
A slack webex slash command implementation in python.
Basically a webhook that will be called by slack whenever the /webex slash command is used in slack chat.
Users can start a webex session using "/webex start" or join a user's webex room using "/webex join @slackuser"

For example,

`/webex start` - When a slack user with slack username "krangaraju" executes this slash command, the following message is sent(via a bot) to the same channel where the command was executed: `@krangaraju has started a webex session. Join: http://company.webex.com/meet/krangaraju`

`/webex join @slackuser` - When a slack user with slack username "krangaraju" executes this slash command to join another slack user's webex say "svishwakarma", It will generate the following message that is only visible to you(via a bot): `Click here to join svishwakarma's webex room: http://castlighthealth.webex.com/meet/svishwakarma`

# Note
This is based on the assumption that your slack and webex account in your company both use a common LDAP username. 

# Installation
Setup the following environment variables

`export SLACK_TOKEN=""`

The OAuth access token from: https://api.slack.com/apps/<your_app_id>/oauth

`export SLACK_WEBHOOK_SECRET=""`

The verification token from https://api.slack.com/apps/<your_app_id/general under App Credentials

`export ENTERPRISE_WEBEX_URL="http://yourcompany.webex.com/meet/"`

Your company specific URL that will be used to generate meeting URLs. For example, when a slack user
uses "/webex join @someuser" slash command, http://company.webex.com/meet/someuser will be generated and returned
to the user.

# Running the server
`python app.py`



krangaraju-15mbpr:slack-webex-python-plugin krangaraju$ python app.py
 
 \* Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)

# Running unit tests
`python webex_slash_command_controller_test.py`
