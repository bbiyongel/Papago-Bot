import configparser
import discord

config = configparser.RawConfigParser()

def ConfigRead(name, option):
    config.read("config.ini")
    ConfigReadValue = config[name][option]
    return ConfigReadValue

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

def FeedBack(ctx, lang1, lang2, text, result_text, type):
    if ConfigRead("option", "feedback") == "on":
        print(f"Type: {type}\n")
        print(f"{ctx.author}: {text} -> {result_text} ({lang1} -> {lang2})\n")

langlist = ["ko", "en", "zh-CN", "zh-TW", "es", "fr", "vi", "th", "id"]

def LangChange(lang):
    if lang in langlist:
        result = lang
    elif lang == "한국어":
        result = "ko"
    elif lang == "영어":
        result = "en"
    elif lang == "중국어(간체)":
        result = "zh-CN"
    elif lang == "중국어(번체)":
        result = "zh-TW"
    elif lang == "스페인어":
        result = "es"
    elif lang == "프랑스어":
        result = "fr"
    elif lang == "베트남어":
        result = "vi"
    elif lang == "태국어":
        result = "th"
    elif lang == "인도네시아어":
        result = "id"
    else:
        result = None
    return result