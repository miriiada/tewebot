from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
import aiohttp
import logging
from datetime import datetime

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# My Token
TOKEN = "8095737556:AAGXGYpSHsysEayBrN5NpC_0fcn81hp-xpg"
# OpenWeatherMap API Key
WEATHER_API_KEY = "09462269509148564219f8fd1dd2a88a"

# Initialize the bot
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Main menu
main_menu = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="Weather"), types.KeyboardButton(text="Forecast")],
        [types.KeyboardButton(text="Info"), types.KeyboardButton(text="About")],
        [types.KeyboardButton(text="Help"), types.KeyboardButton(text="Contact")]
    ],
    resize_keyboard=True
)

# Weather emoji mapping
WEATHER_EMOJI = {
    "clear": "☀️",
    "clouds": "☁️",
    "rain": "🌧️",
    "snow": "❄️",
    "thunderstorm": "⛈️",
    "drizzle": "🌦️",
    "mist": "🌫️",
    "fog": "🌫️"
}

# Handler for the /start command
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    logger.info(f"User {message.from_user.id} started the bot")
    await message.reply("Hello! I can show you the weather or help you.", reply_markup=main_menu)

# Handler for /weather command (e.g., /weather Moscow)
@dp.message(Command("weather"))
async def weather_command(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply("Please provide a city name, e.g., /weather Moscow")
        return
    city = args[1]
    await get_weather_data(message, city)

# Handler for "Weather" button
@dp.message(lambda message: message.text == "Weather")
async def weather_button(message: types.Message):
    logger.info(f"User {message.from_user.id} requested weather")
    await message.reply("Please send me a city name (e.g., London) to get the weather!")

# Handler for "Forecast" button
@dp.message(lambda message: message.text == "Forecast")
async def forecast_button_prompt(message: types.Message):
    logger.info(f"User {message.from_user.id} requested forecast")
    await message.reply("Please send me a city name (e.g., London) to get the 3-day forecast!")

# Handler for city weather or forecast
@dp.message(lambda message: message.text not in ["Weather", "Forecast", "Info", "Help", "About", "Contact"])
async def get_weather_or_forecast(message: types.Message):
    city = message.text
    if message.reply_to_message and "3-day forecast" in message.reply_to_message.text.lower():
        await get_forecast_data(message, city, days=3)
    else:
        await get_weather_data(message, city)

# General function for current weather
async def get_weather_data(message: types.Message, city: str):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    logger.info(f"Fetching current weather for {city}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                temp = data["main"]["temp"]
                desc = data["weather"][0]["description"].lower()
                wind = data["wind"]["speed"]
                feels_like = data["main"]["feels_like"]
                pressure = data["main"]["pressure"]
                humidity = data["main"]["humidity"]
                weather_icon = data["weather"][0]["icon"]
                icon_url = f"http://openweathermap.org/img/wn/{weather_icon}@2x.png"
                emoji = next((e for w, e in WEATHER_EMOJI.items() if w in desc), "🌍")
                weather_text = (
                    f"Weather in {city}:\n"
                    f"Temp: {temp}°C\n"
                    f"Feels like: {feels_like}°C\n"
                    f"{emoji} {desc}\n"
                    f"Wind: {wind} m/s\n"
                    f"Pressure: {pressure} hPa\n"
                    f"Humidity: {humidity}%"
                )
                keyboard = types.InlineKeyboardMarkup(
                    inline_keyboard=[
                        [types.InlineKeyboardButton(text="Back to Menu", callback_data="back"),
                         types.InlineKeyboardButton(text="3-Day Forecast", callback_data=f"forecast_{city}"),
                         types.InlineKeyboardButton(text="5-Day Forecast", callback_data=f"forecast5_{city}")]
                    ]
                )
                await message.reply_photo(photo=icon_url, caption=weather_text, reply_markup=keyboard)
            else:
                await message.reply("Sorry, I couldn't find that city. Try again!")

# General function for forecast
async def get_forecast_data(message: types.Message, city: str, days: int):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_API_KEY}&units=metric"
    logger.info(f"Fetching {days}-day forecast for {city}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                forecast_text = f"{days}-Day Forecast for {city}:\n"
                last_date = None
                for item in data["list"][:min(days * 8, len(data["list"]))]:  # Не превышаем длину данных
                    time = datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S")
                    date_str = time.strftime("%d:%m %H hour")
                    temp = item["main"]["temp"]
                    desc = item["weather"][0]["description"].lower()
                    emoji = next((e for w, e in WEATHER_EMOJI.items() if w in desc), "🌍")
                    current_date = time.strftime("%d:%m")
                    if last_date and last_date != current_date:
                        forecast_text += "----------------\n"
                    forecast_text += f"{date_str}: {temp}°C, {emoji} {desc}\n"
                    last_date = current_date
                keyboard = types.InlineKeyboardMarkup(
                    inline_keyboard=[[types.InlineKeyboardButton(text="Back to Menu", callback_data="back")]]
                )
                await message.reply(forecast_text, reply_markup=keyboard)
            else:
                await message.reply("Sorry, I couldn't fetch the forecast.")

# Handler for 3-day forecast from inline button
@dp.callback_query(lambda query: query.data.startswith("forecast_"))
async def forecast_button(query: types.CallbackQuery):
    city = query.data.split("_")[1]
    await get_forecast_data(query.message, city, days=3)
    await query.answer()

# Handler for 5-day forecast from inline button
@dp.callback_query(lambda query: query.data.startswith("forecast5_"))
async def forecast5_button(query: types.CallbackQuery):
    city = query.data.split("_")[1]
    await get_forecast_data(query.message, city, days=5)
    await query.answer()

# Handler for "Info" button
@dp.message(lambda message: message.text == "Info")
async def info_button(message: types.Message):
    await message.reply("I am a bot created to help!")

# Handler for "Help" button
@dp.message(lambda message: message.text == "Help")
async def help_button(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="Weather Info", callback_data="weather_help")]
        ]
    )
    await message.reply("With this bot you can find out the weather of any city in the world!", reply_markup=keyboard)

# Handler for "Weather Info" inline button
@dp.callback_query(lambda query: query.data == "weather_help")
async def weather_help(query: types.CallbackQuery):
    await query.message.reply("Enter a city name or use /weather <city> to get current weather.")
    await query.answer()

# Handler for "About" button
@dp.message(lambda message: message.text == "About")
async def about_button(message: types.Message):
    await message.reply("This is my first version bot by Miriada, v1.0")

# Handler for "Contact" button
@dp.message(lambda message: message.text == "Contact")
async def contact_button(message: types.Message):
    await message.reply("Write to @YourUsername")

# Handler for "Back" inline button
@dp.callback_query(lambda query: query.data == "back")
async def back_button(query: types.CallbackQuery):
    await query.message.reply("Back to main menu!", reply_markup=main_menu)
    await query.answer()

# Start bot
async def main():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())