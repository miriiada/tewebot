
# 🌤️ Telegram Weather Bot

A fully asynchronous Telegram bot built with [aiogram](https://github.com/aiogram/aiogram), providing real-time weather information and forecast using the OpenWeatherMap API.

> Created by **Miriiada**, v1.0  
> Technologies: `Python`, `aiogram`, `aiohttp`, `OpenWeatherMap API`

---

## 📦 Features

- 🔍 Get **current weather** by city name
- 📅 Check **3-day** and **5-day forecast**
- 🌎 Weather data with emojis, icons, and temperature details
- 🔘 Menu with buttons for quick navigation
- 📡 Built with asynchronous requests via `aiohttp`

---

## 🛠 Requirements

- Python 3.9+
- Telegram Bot Token ([@BotFather](https://t.me/BotFather))
- OpenWeatherMap API key ([openweathermap.org](https://openweathermap.org/api))

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/weather-telegram-bot.git
cd weather-telegram-bot
```
2. Install dependencies
```bash
pip install -r requirements.txt
```
If you don't have requirements.txt, use:
```bash
pip install aiogram aiohttp
```
3. Add your API keys
Open the main Python file and replace the placeholder values:

```python
TOKEN = "your_token_telegram_bot"
WEATHER_API_KEY = "your_API_key"
```
▶️ Run the bot
```bash
python main.py
```
💡 Usage
Commands:
/start — start and show main menu

/weather <city> — get current weather

Buttons:
Weather — prompts user to enter city

Forecast — prompts for 3-day forecast

Info, About, Help, Contact — additional info & guidance

🤖 Built With

[aiogram](https://github.com/aiogram/aiogram) — modern and fast Telegram bot framework

aiohttp — async HTTP requests

OpenWeatherMap API
