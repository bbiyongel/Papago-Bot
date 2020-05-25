import discord
from discord.ext import commands
import requests as rq
import asyncio
import configparser

bot = commands.Bot(command_prefix = "/")
API = "Papago API"
url = "https://openapi.naver.com/v1/papago/n2mt"
detect_url = "https://openapi.naver.com/v1/papago/detectLangs"
language_ko = '''한국어(ko)
일본어(ja)
중국어 간체(zh-CN)
중국어 번체(zh-TW)
힌디어(hi)
영어(en)
스페인어(es)
프랑스어(fr)
독일어(de)
포르투갈어(pt)
베트남어(vi)
인도네시아어(id)
페르시아어(fa)
아랍어(ar)
미얀마어(mm)
태국어(th)
러시아어(ru)
이탈리아어(it)'''
helpdescription = '''/번역 <번역할 언어> <번역 결과 언어> <내용> - 내용을 번역합니다.

/자동번역 <번역 결과 언어> <내용> - 언어를 자동으로 감지하여 번역합니다.

/번역언어 - 번역할수 있는언어 목록을 봅니다.

/API목록 - 사용된 API 목록을 봅니다.
'''
APIdescription = '''Papago 번역
https://developers.naver.com/products/nmt
Papago 언어감지
https://developers.naver.com/products/detectLangs
'''
papagoimage = "http://post.phinf.naver.net/MjAxNjExMDlfOSAg/MDAxNDc4NjcyMzYzNTM5._nMAXYkM8-uIifnvhZQbYyMuVvGwAcPrBNwycJscULIg.Bt1tiuDSFrGnk8Il_skT5HkNjyWVwyRd0ZqLQku7yTYg.PNG/ISVgxRDaNgL3miUGjU55nGJ_cxlc.jpg"
OptionReadValue = None
config = configparser.RawConfigParser()

def OptionRead(option):
    global OptionReadValue
    config.read("config.ini")
    OptionReadValue = config["option"][option]

OptionRead("id")
id = OptionReadValue
OptionRead("secret")
secret  = OptionReadValue
headers = {"X-Naver-Client-Id": id, "X-Naver-Client-Secret": secret}

@bot.event
async def on_ready():
    print("봇이 준비됨!\n")
    print("Papgo Bot: https://discord.com/api/oauth2/authorize?client_id=714076564165492736&permissions=8&scope=bot\n") 
    while True:
        game = discord.Game(API)
        await bot.change_presence(status=discord.Status.online, activity=game)
        await asyncio.sleep(5)
        game = discord.Game("/도움말")
        await bot.change_presence(status=discord.Status.online, activity=game)
        await asyncio.sleep(5)

@bot.command(pass_context=True)
async def 도움말(ctx):
    embed=discord.Embed(title="「도움말」", description=helpdescription)
    embed.set_thumbnail(url=papagoimage)
    embed.set_footer(text=API)
    await ctx.author.send(embed=embed)

@bot.command(pass_context=True)
async def 번역(ctx, language1, language2, *, text):
    translation_text = {"source": language1, "target": language2, "text": text}
    response = rq.post(url, headers=headers, data=translation_text) 
    result = response.json()
    result_text = result["message"]["result"]["translatedText"]
    embed=discord.Embed(title=f"「번역 결과 {language1} -> {language2}」", description=f"{ctx.author.display_name }: {result_text}")
    embed.set_thumbnail(url=papagoimage)
    embed.set_footer(text=API)
    await ctx.send(embed=embed)
    print("type: translation\n")
    print(f"{ctx.author}: {text}\n")
    print(str(result) + "\n")

@bot.command(pass_context=True)
async def 자동번역(ctx, language, *, text):
    detect_text = {"query": text}
    detect_response = rq.post(detect_url, headers=headers, data=detect_text)
    detect_result = detect_response.json()
    detect_lang = detect_result["langCode"]
    translation_text = {"source": detect_lang, "target": language, "text": text}
    response = rq.post(url, headers=headers, data=translation_text) 
    result = response.json()
    result_text = result["message"]["result"]["translatedText"]
    embed=discord.Embed(title=f"「번역 결과 {detect_lang} -> {language}」", description=f"{ctx.author.display_name }: {result_text}") 
    embed.set_thumbnail(url=papagoimage)
    embed.set_footer(text=API)
    await ctx.send(embed=embed)
    print("type: autotranslation\n")
    print(f"{ctx.author}: {text}\n")
    print(str(detect_result) +"\n")
    print(str(result) + "\n")

@bot.command(pass_context=True)
async def 번역언어(ctx):
    embed=discord.Embed(title="「번역 언어」", description=language_ko)
    embed.set_thumbnail(url=papagoimage)
    embed.set_footer(text=API)
    await ctx.author.send(embed=embed)

@bot.command(pass_context=True)
async def API목록(ctx):
    embed=discord.Embed(title=f"「API」", description=APIdescription)
    embed.set_thumbnail(url=papagoimage)
    embed.set_footer(text=API)
    await ctx.author.send(embed=embed)

OptionRead("token")
bot.run(OptionReadValue)