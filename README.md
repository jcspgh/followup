# Followup Bot

Send followup messages 

## Usage

```
Usage: /followup "Message text" "datetime"
```

## Setup

### 1. Create Slack bot
Create <a href="https://my.slack.com/services/new/bot">legacy slack bot</a> for your slack org, install, and
go through steps to create an api key.

Note: This creates what Slack calls a legacy bot. This will not work with Slacks new "Apps".

### 2. Create .env file

Credentials used by the bot are stored in an .env file. Create file and add credentials.
```
SLACK_BOT_TOKEN=
```

### 3. Running bot locally

Run docker-compose to start the bot
```
docker-compose up -d 
```

## Running With Glitch
1. Go back to the app settings and click on Slash Commands.
2. Click the 'Create New Command' button and fill in the following:
3. Command: /followup
4. Request URL: Your server or Glitch URL + /follow
5. Short description: Sets a followup reminder
6. Usage hint: /followup "message" "time"

- If you did "Remix" on Glitch, it auto-generate a new URL with two random words, so your Request URL should be like: https://fancy-feast.glitch.me/followup.
