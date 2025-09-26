#!/bin/python3

import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

port = os.getenv("BOT_API_PORT")
if not port:
    port = 5000

url = f"http://{os.getenv('BOT_API_HOST')}:{port}"
if url == f"http://None:{port}":
    url = f"http://127.0.0.1:{port}"

def info():
    r = requests.get(f"{url}/info")
    print(f"Full bot username: {r.json()['username']}#{r.json()['discriminator']}\n"
          f"Profile picture URL: {r.json()['pfp']}")

def ping():
    r = requests.get(f"{url}/ping")
    print(r.json()["ping"])

def status():
    r = requests.get(f"{url}/status")
    
    initial_connect = datetime.fromtimestamp(r.json()["initial_connect"])
    if type(r.json()["last_disconnect"]) is not float:
        last_disconnect = None
    else:
        last_disconnect = datetime.fromtimestamp(r.json()["last_disconnect"])
    if type(r.json()["last_resume"]) is not float:
        last_resume = None
    else:
        last_resume = datetime.fromtimestamp(r.json()["last_resume"])
    
    print(f"Connected to Discord: {r.json()['connected']}\n"
          f"Ping: {r.json()['latency']}ms\n"
          f"Connected at: {initial_connect}\n"
          f"Last disconneted at: {last_disconnect}\n"
          f"Last resume: {last_resume}")

def stats(): # not to be confused with status
    r = requests.get(f"{url}/stats")
    print(f"Bot is in: {r.json()['server_count']} server(s).\n"
          f"Total member amount of the servers that the bot is in is: {r.json()['server_member_count']}.\n"
          f"Bot is installed to {r.json()['user_count']} users.")

def mutual_guilds(user_id):
    r = requests.get(f"{url}/user/{user_id}/guilds")
    print(f"Mutual server IDs that the bot has with the specified user ID: {r.text}")

def guild_info(guild_id):
    global r
    r = requests.get(f"{url}/guild/{guild_id}/{endpoint}")
    #print(r.json())

# i'm sorry
while True:
    try:
        command = input("--> ")

        if command.startswith("info"):
            info()
        elif command.startswith("ping"):
            ping()
        elif command.startswith("status"):
            status()
        elif command.startswith("stats"):
            stats()
        elif command.startswith("mutual_guilds"):
            try:
                user_id = command.split(" ")[1]
            except IndexError:
                user_id = input("User ID: ")
            mutual_guilds(user_id)
        elif command.startswith("guild_info"):
            try:
                guild_id = command.split(" ")[1]
            except IndexError:
                guild_id = input("Guild ID: ")
            endpoint = "info"
            guild_info(guild_id)
            print(r.json())
            r = None
        elif command.startswith("guild_settings"):
            try:
                guild_id = command.split(" ")[1]
            except IndexError:
                guild_id = input("Guild ID: ")
            endpoint = "settings"
            guild_info(guild_id)
            if r.status_code == 404:
                print("Error: The bot is not in the specified server.")
            elif r.status_code == 500:
                print("Error: Failed to retrieve server configuration")
            else:
                print("----- Modules -----\n"
                      f"Moderation: {r.json()['modules']['moderation']}\n"
                      f"Automod: {r.json()['modules']['automod']}\n"
                      f"Logging: {r.json()['modules']['logging']}\n"
                      f"Fireboard: {r.json()['modules']['fireboard']}")
                print("----- Settings -----\n"
                      f"Loading reaction: {r.json()['settings']['loading_reaction']}\n"
                      f"Reply ping: {r.json()['settings']['reply_ping']}")
                print("----- Prefixes -----\n",
                      json.dumps(r.json()['prefixes']))

        elif command.startswith("help"):
            print("----- Commands -----\n"
                  "'info': Shows bot account info\n"
                  "'status': Shows bot status\n"
                  "'stats': Shows bot stats\n"
                  "'mutual_guilds': Shows the bot account's mutual servers with the specified user (takes a user ID)\n"
                  "'guild_info': Shows the specified server's info (takes a server/guild ID)\n"
                  "'guild_settings': Shows Titanium's settings in the specified server (takes a server/guild ID)")
        elif command.startswith("exit"):
            exit()
        else:
            print(f"{command}: command not found")
    except EOFError:
        print("\nEOF caught, exiting...")
        break
    except KeyboardInterrupt:
        print("")
    except requests.exceptions.ConnectionError:
        print("Bot is curently offline. Make sure to start it first, or that you're on the right port.")
