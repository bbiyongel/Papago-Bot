import configparser
import discord

config = configparser.RawConfigParser()

def ConfigRead(name, option):
    config.read("config.ini")
    OptionReadValue = config[name][option]
    return OptionReadValue

API = ConfigRead("api", "API")
papagoimage_url = ConfigRead("url", "papagoimage_url")

def Embed(ctx, title, description):
    embed=discord.Embed(title=f"「{title}」", description=description, color=0x00e00f)
    embed.set_thumbnail(url=papagoimage_url)
    embed.set_footer(text=API)
    return embed

def TXTRead(name):
    with open(f"txt/{name}.txt", "r", encoding="utf8") as tf:
        result = tf.read()
        return result