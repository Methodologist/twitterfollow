import discord
from discord.ext import tasks
import tweepy

# Twitter API credentials
TWITTER_API_KEY = '...'
TWITTER_API_SECRET = '...'
TWITTER_ACCESS_TOKEN = '...'
TWITTER_ACCESS_TOKEN_SECRET = '...'

# Discord bot token
DISCORD_BOT_TOKEN = '...'

# Discord channel ID where tweets will be sent
DISCORD_CHANNEL_ID = ...

# Initialize Discord client with intents
intents = discord.Intents.default()
intents.messages = True  # Enable message intents

client = discord.Client(intents=intents)

# Authenticate to Twitter API
auth = tweepy.OAuth1UserHandler(TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Function to fetch tweets and send them to Discord
@tasks.loop(seconds=60)  # Fetch tweets every 60 seconds
async def fetch_and_send_tweets():
    user_ids = ['VVS_finance', 'CryptoKipTweets', 'realOscarRamos1']  # Add the Twitter user IDs you want to fetch tweets from
    channel = client.get_channel(DISCORD_CHANNEL_ID)
    
    for user_id in user_ids:
        tweets = api.user_timeline(id=user_id, count=5)  # Fetch the latest 5 tweets for the specified user_id
        for tweet in tweets:
            await channel.send(f'New tweet from {tweet.user.screen_name}: {tweet.text}')


# Event: Bot is ready
@client.event
async def on_ready():
    print('Bot is ready!')
    fetch_and_send_tweets.start()  # Start the task to fetch and send tweets

# Run the bot
client.run(DISCORD_BOT_TOKEN)
