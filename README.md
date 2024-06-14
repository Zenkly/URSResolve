![Logo de Castell](https://github.com/Zenkly/URSResolve/blob/main/Castell.jpg)

# Castell Bot

Castell is a Telegram bot designed by students for Universidad Rosario Castellanos that offers functionalities to solve queries, perform natural language queries in group chats, initiate satisfaction surveys, provide useful university links, and manage administrators.

## Features

- Resolves queries using natural language processing with RAG via OpenAI and COHERE.
- Group chat consultation functionality.
- Initiates satisfaction surveys.
- Displays frequently used university links.

## Commands

- `/consulta`: Utilize natural language functionalities in group chats.
- `/encuesta`: Initiate a satisfaction survey.
- `/ligas`: Display frequently used university links.
- `/radmin`: Register administrators by mentioning them (admin-only).
- `/rmvadmin`: Remove administrators by metioning them(admin-only).
- `/start`: Introduction command for the bot.
- `/dsurvey`: Download survey data (admin-only).

## Development

The bot is developed in Python using the `python-telegram-bot` library and integrates with the APIs of OpenAI and COHERE for natural language query resolution.

## Execution

To run the bot, use the following command:

```
python main_bot.py
```
