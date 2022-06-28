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
