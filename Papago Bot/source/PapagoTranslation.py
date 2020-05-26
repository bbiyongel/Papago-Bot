import requests as rq
import discord
import PapagoTool

translation_url = PapagoTool.ConfigRead("url", "translation_url")
detect_url = PapagoTool.ConfigRead("url", "detect_url")
headers = {"X-Naver-Client-Id": PapagoTool.ConfigRead("option", "id"), "X-Naver-Client-Secret": PapagoTool.ConfigRead("option", "secret")}

def Translation(lang1, lang2, text):
    translation_text = {"source": lang1, "target": lang2, "text": text}
    response = rq.post(translation_url, headers=headers, data=translation_text) 
    result = response.json()
    result_text = result["message"]["result"]["translatedText"]
    return result_text

def Detect(text):
    detect_text = {"query": text}
    detect_response = rq.post(detect_url, headers=headers, data=detect_text)
    detect_result = detect_response.json()
    detect_lang = detect_result["langCode"]
    return detect_lang

API = PapagoTool.ConfigRead("api", "API")
papagoimage_url = PapagoTool.ConfigRead("url", "papagoimage_url")

def Embed(ctx, lang1, lang2, result_text):
    embed=discord.Embed(title=f"「번역 결과 {lang1} -> {lang2}」", description=f"{ctx.author.display_name}: {result_text}", color=0x00e00f)
    embed.set_thumbnail(url=papagoimage_url)
    embed.set_footer(text=API)
    return embed