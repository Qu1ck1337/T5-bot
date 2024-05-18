## Before running the bot:

Create `.env` file:
```dotenv
# Bot authorization
TOKEN=<bot_token>

# Database
DB_NAME=<db_name>
DB_USERNAME=<username>
DB_PASSWORD=<db_pass>
DB_HOST=localhost
```

## Local run
```commandline
docker build -t t5-bot .
docker container run --rm t5-bot
```