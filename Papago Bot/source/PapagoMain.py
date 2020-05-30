import discord
from discord.ext import commands
from discord.utils import get
import asyncio
import PapagoSub
from gtts import gTTS
import eyed3
import os

bot = commands.Bot(command_prefix="/")
bot.remove_command("help")

@bot.event
async def on_ready():
    print("봇이 준비됨!\n")
    print(f"{PapagoSub.API}\n") 
    while True:
        game = discord.Game(PapagoSub.API)
        await bot.change_presence(status=discord.Status.online, activity=game)
        await asyncio.sleep(5)
        game = discord.Game("/도움말 & /help")
        await bot.change_presence(status=discord.Status.online, activity=game)
        await asyncio.sleep(5)
    
@bot.command(pass_context=True, aliases=["help"])
async def 도움말(ctx):
    await ctx.author.send(embed=PapagoSub.Tool.Embed(ctx, "도움말", PapagoSub.Tool.TXTRead("helpdescription")))

@bot.command(pass_context=True)
async def 번역(ctx, lang1, lang2, *, text):
    await ctx.send(embed=PapagoSub.Translation.Embed(ctx, PapagoSub.Tool.LangChange(lang1), PapagoSub.Tool.LangChange(lang2), PapagoSub.Translation.Translation(PapagoSub.Tool.LangChange(lang1), PapagoSub.Tool.LangChange(lang2), text)))
    PapagoSub.Tool.FeedBack(ctx, PapagoSub.Tool.LangChange(lang2), PapagoSub.Tool.LangChange(lang2), text, PapagoSub.Translation.Translation(PapagoSub.Tool.LangChange(lang1), PapagoSub.Tool.LangChange(lang2), text), "Translation")

@bot.command(pass_context=True)
async def 자동번역(ctx, lang, *, text):
    await ctx.send(embed=PapagoSub.Translation.Embed(ctx, PapagoSub.Translation.Detect(text), PapagoSub.Tool.LangChange(lang), PapagoSub.Translation.Translation(PapagoSub.Translation.Detect(text), PapagoSub.Tool.LangChange(lang), text)))
    PapagoSub.Tool.FeedBack(ctx, PapagoSub.Tool.LangChange(PapagoSub.Translation.Detect(text)), PapagoSub.Tool.LangChange(lang), text, PapagoSub.Translation.Translation(PapagoSub.Translation.Detect(text), PapagoSub.Tool.LangChange(lang), text), "Auto Translation")

@bot.command(pass_context=True)
async def 음성번역(ctx, lang, *, text):
    out = gTTS(text=PapagoSub.Translation.Translation(PapagoSub.Translation.Detect(text), PapagoSub.Tool.LangChange(lang), text), lang=PapagoSub.Tool.LangChange(lang), slow=False)
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
    PapagoSub.Tool.FeedBack(ctx, PapagoSub.Tool.LangChange(PapagoSub.Translation.Detect(text)), PapagoSub.Tool.LangChange(lang), text, PapagoSub.Translation.Translation(PapagoSub.Translation.Detect(text), PapagoSub.Tool.LangChange(lang), text), "Auto Translation")

@bot.command(pass_context=True)
async def 번역언어(ctx):
    await ctx.author.send(embed=PapagoSub.Tool.Embed(ctx, "번역 언어", PapagoSub.Tool.TXTRead("language")))

@bot.command(pass_context=True)
async def API목록(ctx):
    await ctx.author.send(embed=PapagoSub.Tool.Embed(ctx, "API 목록", PapagoSub.Tool.TXTRead("APIdescription")))
    
bot.run(PapagoSub.ConfigRead("option", "token"))