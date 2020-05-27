import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import PapagoTranslation
import PapagoTool
from gtts import gTTS
import eyed3
import os

bot = commands.Bot(command_prefix = "/")
API = PapagoTool.ConfigRead("api", "API")
Papago_translation = PapagoTool.ConfigRead("api", "Papago_translation")
Papago_detect = PapagoTool.ConfigRead("api", "Papago_detect")
bot.remove_command("help")

@bot.event
async def on_ready():
    print("봇이 준비됨!\n")
    print(f"{API}\n") 
    while True:
        game = discord.Game(API)
        await bot.change_presence(status=discord.Status.online, activity=game)
        await asyncio.sleep(5)
        game = discord.Game("/도움말 & /help")
        await bot.change_presence(status=discord.Status.online, activity=game)
        await asyncio.sleep(5)

@bot.command(pass_context=True, aliases=["help"])
async def 도움말(ctx):
    await ctx.send(embed=PapagoTool.Embed(ctx, "도움말", PapagoTool.TXTRead("helpdescription")))

@bot.command(pass_context=True)
async def 번역(ctx, lang1, lang2, *, text):
    await ctx.send(embed=PapagoTranslation.Embed(ctx, PapagoTool.LangChange(lang1), PapagoTool.LangChange(lang2), PapagoTranslation.Translation(PapagoTool.LangChange(lang1), PapagoTool.LangChange(lang2), text)))
    PapagoTool.FeedBack(ctx, PapagoTool.LangChange(lang2), PapagoTool.LangChange(lang2), text, PapagoTranslation.Translation(PapagoTool.LangChange(lang1), PapagoTool.LangChange(lang2), text), "Translation")

@bot.command(pass_context=True)
async def 자동번역(ctx, lang, *, text):
    await ctx.send(embed=PapagoTranslation.Embed(ctx, PapagoTranslation.Detect(text), PapagoTool.LangChange(lang), PapagoTranslation.Translation(PapagoTranslation.Detect(text), PapagoTool.LangChange(lang), text)))
    PapagoTool.FeedBack(ctx, PapagoTranslation.Detect(text), PapagoTool.LangChange(lang), text, PapagoTranslation.Translation(PapagoTranslation.Detect(text), PapagoTool.LangChange(lang), text), "Auto Translation")

@bot.command(pass_context=True)
async def 사운드번역(ctx, lang, *, text):
    out = gTTS(text=PapagoTranslation.Translation(PapagoTranslation.Detect(text), PapagoTool.LangChange(lang), text), lang=PapagoTool.LangChange(lang), slow=False)
    out.save(f"tts/{ctx.channel.id}.mp3")
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    voice.play(discord.FFmpegPCMAudio(f"tts/{ctx.channel.id}.mp3"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 2
    await asyncio.sleep(eyed3.load(f"tts/{ctx.channel.id}.mp3").info.time_secs)
    await voice.disconnect()
    os.remove(f"tts/{ctx.channel.id}.mp3")
    PapagoTool.FeedBack(ctx, PapagoTranslation.Detect(text), PapagoTool.LangChange(lang), text, PapagoTranslation.Translation(PapagoTranslation.Detect(text), PapagoTool.LangChange(lang), text), "Sound Translation")

@bot.command(pass_context=True)
async def 번역언어(ctx):
    await ctx.author.send(embed=PapagoTool.Embed(ctx, "번역 언어", PapagoTool.TXTRead("language")))

@bot.command(pass_context=True)
async def API목록(ctx):
    await ctx.author.send(embed=PapagoTool.Embed(ctx, "API 목록", PapagoTool.TXTRead("APIdescription")))
    
bot.run(PapagoTool.ConfigRead("option", "token"))