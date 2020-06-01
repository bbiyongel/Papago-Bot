# Module
import configparser
import discord # Discord.py
import requests as rq

# Config
config = configparser.RawConfigParser()
def ConfigRead(name, option):
    config.read("config.ini")
    return config[name][option]

# Value
API = ConfigRead("api", "API")
papagoimage_url = ConfigRead("url", "papagoimage_url")
langlist = ["ko", "en", "ja", "zh-CN", "zh-TW", "es", "fr", "vi", "th", "id"]
headers = {"X-Naver-Client-Id": ConfigRead("option", "id"), "X-Naver-Client-Secret": ConfigRead("option", "secret")}
translation_url = ConfigRead("url", "translation_url")
detect_url = ConfigRead("url", "detect_url")\

# Color
BLUE = '\033[34m'
YELLOW = '\033[33m'
GREEN = '\033[32m'
RED = '\033[31m'
END = '\033[0m'
BOLD = '\033[1m'

# Tool
class Tool:

    @classmethod
    def Embed(cls, ctx, title, description):
        embed=discord.Embed(title=f"「{title}」", description=description, color=0x00e00f)
        embed.set_thumbnail(url=papagoimage_url)
        embed.set_footer(text=API)
        return embed

    @classmethod
    def TXTRead(cls, name):
        with open(f"txt/{name}.txt", "r", encoding="utf8") as tf:
            text = tf.read()
            return text

    @classmethod
    def FeedBack(cls, ctx, lang1, lang2, text, result_text, type):
        if ConfigRead("option", "feedback") == "on":
            print(f"{GREEN}{BOLD}Type: {type}\n{END}")
            print(f"{ctx.author}: {text} -> {result_text} ({lang1} -> {lang2})\n")

    @classmethod
    def LangChange(cls, lang):
        if lang in langlist:
            result = lang
        elif lang == "한국어":
            result = "ko"
        elif lang == "영어":
            result = "en"
        elif lang == "일본어":
            result = "ja"
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

# Translation
class Translation:

    @classmethod
    def Translation(cls, lang1, lang2, text):
        translation_text = {"source": lang1, "target": lang2, "text": text}
        response = rq.post(translation_url, headers=headers, data=translation_text)
        result = response.json()
        result_text = result["message"]["result"]["translatedText"]
        return result_text

    @classmethod
    def Detect(cls, text):
        detect_text = {"query": text}
        detect_response = rq.post(detect_url, headers=headers, data=detect_text)
        detect_result = detect_response.json()
        result_text = detect_result["langCode"]
        return result_text

    @classmethod
    def Embed(cls, ctx, lang1, lang2, result_text):
        embed=discord.Embed(title=f"「번역 결과 {lang1} -> {lang2}」", description=f"{ctx.author.display_name}: {result_text}", color=0x00e00f)
        embed.set_thumbnail(url=papagoimage_url)
        embed.set_footer(text=API)
        return embed
