from os import getenv

from dotenv import load_dotenv

from DiscordBot import DiscordBot

load_dotenv()
DISCORD_GUILD = getenv("DISCORD_GUILD")
DISCORD_TOKEN = getenv("DISCORD_TOKEN")
print(DISCORD_GUILD)
print(DISCORD_TOKEN)

bot_instance = DiscordBot(DISCORD_GUILD, DISCORD_TOKEN)

if __name__ == "__main__":
    bot_instance.run_bot()
