# Patch the event loop
import nest_asyncio
nest_asyncio.apply()

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests
import random

# Replace with your Telegram bot token
BOT_TOKEN = ""

# Function to fetch a random coding challenge from Codeforces
def get_coding_challenge():
    url = "https://codeforces.com/api/problemset.problems"
    response = requests.get(url)
    if response.status_code == 200:
        problems = response.json()["result"]["problems"]
        # Filter problems with difficulty level (optional)
        filtered_problems = [p for p in problems if "rating" in p]
        if filtered_problems:
            problem = random.choice(filtered_problems)  # Pick a random problem
            problem_name = problem.get("name", "Unknown Problem")
            problem_rating = problem.get("rating", "Unknown Difficulty")
            problem_url = f"https://codeforces.com/problemset/problem/{problem['contestId']}/{problem['index']}"
            return f"Today's Coding Challenge:\n\n{problem_name}\nDifficulty: {problem_rating}\nLink: {problem_url}"
    return "Could not fetch a coding challenge. Try again later!"

# Function to recommend resources
def get_resources(topic):
    resources = {
        "python": ["https://realpython.com", "https://docs.python.org/3/"],
        "javascript": ["https://javascript.info", "https://developer.mozilla.org/en-US/docs/Web/JavaScript"],
        "react": ["https://reactjs.org/docs/getting-started.html", "https://www.freecodecamp.org/news/tag/react/"],
    }
    if topic.lower() in resources:
        return f"Here are some great resources for {topic}:\n" + "\n".join(resources[topic.lower()])
    return f"Sorry, I don't have resources for {topic} yet. Try Python, JavaScript, or React!"

# Handle the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "👋 Welcome to the Programmer's Learning Companion Bot!\n\n"
        "Here’s what I can do:\n"
        "/challenge - Get a daily coding challenge\n"
        "/resources <topic> - Get learning resources\n"
        "/help - Show this message again"
    )
    await update.message.reply_text(welcome_message)

# Handle the /challenge command
async def challenge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    challenge_text = get_coding_challenge()
    await update.message.reply_text(challenge_text)

# Handle the /resources command
async def resources(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = " ".join(context.args) if context.args else ""
    if topic:
        resource_text = get_resources(topic)
        await update.message.reply_text(resource_text)
    else:
        await update.message.reply_text("Please specify a topic. Example: /resources python")

# Handle the /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

# Main function to start the bot
def main():
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("challenge", challenge))
    application.add_handler(CommandHandler("resources", resources))
    application.add_handler(CommandHandler("help", help_command))

    # Start the bot
    print("Bot is running...")
    application.run_polling()

# Run the bot
if __name__ == "__main__":
    main()
