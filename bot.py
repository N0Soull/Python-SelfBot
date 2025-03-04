import discord
import os
import json
from discord.ext import commands
from dotenv import load_dotenv
from colorama import Fore as F
from cogs.banner import banner

# please note that this damn god forbidden load .env function can only work with properly set up libraries
# if you try to do it otherwise and not like it says in README then it´s your fault and you can fuck with that on your own
# note aswell that i am not planning to fix it becouse it´s your own fault if you dont set up you´r enviroment right and dont know what you are doing
os.environ.clear()
load_dotenv()
# Get token from environment variables
token = os.getenv('TOKEN')

# Define default configuration dictionary
default_config: dict = {
    "debug": False,
    "command_prefix": ">"
}

# Set path to the primary configuration file
primary_config_file_path: str = "./cfg/config.json"

# Initialize configuration dictionary with default settings
config: dict = default_config

# If user-defined configuration file exists, merge it with default configuration
if os.path.exists(primary_config_file_path):
    with open(primary_config_file_path, "r") as config_file:
        user_config = json.load(config_file)
        config.update(user_config)
else:
    print(f"'{primary_config_file_path}' is not found. Using default configuration.")

# Assign extracted configuration values to separate variables
debug: bool = config.get("debug")
cfg_prefix: str = config.get("command_prefix")


# bot intialization
class Bot(commands.Bot):
    def __init__(self, command_prefix, self_bot):
        super().__init__(
            command_prefix=command_prefix,
            self_bot=self_bot
        )
        # Initialization tasks performed after instantiation
        self.cogs_folder = "cogs"
        self.remove_command("help")
        self.debug = debug

    async def setup_hook(self):
        # Perform initialization tasks required during cog loading
        cog_files = [f[:-3] for f in os.listdir(self.cogs_folder) if f.endswith(".py" ) and f != "banner.py"]

        for cog_file in cog_files:
            cog_path = f"{self.cogs_folder}.{cog_file}"
            try:
                await self.load_extension(cog_path)
                print(f"{F.GREEN}[+]{F.LIGHTWHITE_EX} Loaded {cog_file}")

            except Exception as e:
                print(f"{F.RED}[-]{F.LIGHTWHITE_EX} Failed to load {cog_file}.\n  Error: {F.RED}{e}{F.RESET}")
                exit()
        print(f"{F.YELLOW}[?]{F.LIGHTWHITE_EX} Connecting...")

    # on ready message
    async def on_ready(self):
        # Callback executed upon successful connection to Discord server
        # sets standart presense (status: idle activity: listenting)
        await self.change_presence(
            status=discord.Status.idle,
            activity=discord.Activity(
                type=discord.ActivityType.watching, #activity types: playing, watching, streaming, listening, custom, competing
                name="N0Soul go insane"
            ),
            afk=True # AFK mode: ON/OFF for discord to better catch and force the notifications
        )
        print(f"{F.LIGHTMAGENTA_EX}(*){F.LIGHTWHITE_EX} rpc set to: {F.LIGHTMAGENTA_EX}Start")

        if self.debug:
            print("PRESENSE CHANGED: \nDefeault presense")

# Instantiate client object and run the bot
client = Bot(command_prefix=cfg_prefix, self_bot=True)
client.run(token)