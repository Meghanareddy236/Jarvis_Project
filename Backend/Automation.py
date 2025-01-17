from AppOpener import close,open as appopen
from webbrowser import open as webopen
from pywhatkit import search,playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os

env_vars=dotenv_values(".env")
GroqAPIKey=env_vars.get("GroqAPIKey")

classes=["zCubwf","hgKElc","LTKOO sY7ric","Z0LcW","gsrt vk_bk FzvWSb YwPhnf","pclqee","tw-Data-text tw-text-small tw-ta",
     "IZ6rdc","O5uR6d LTKOO","vlzY6d","webanswers-webanswers_table__webanswers-table","dDoNo iKb4Bb gsrt","sXLaOe",
     "LWkfKe","VQF4g","qv3Wpe","kno-rdesc","SPZz6b"    ]

user_agent="Mozilla/5.0(Windows NT 10.0; Win64 ; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/89.0.142.86 Safari/537.36"

client=Groq(api_key=GroqAPIKey)

professional_responses=[
    "Your Satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need not hesitate to ask."
]

messages=[]

SystemChatBot=[{"role":"system","content":f"Hello, Iam {os.environ['username']},You're a content writer.you have to write content like letters,codes,applications,essays,notes,songs,poems,etc."}]

def GoogleSearch(Topic):
    search(Topic)
    return True

def Content(Topic):
    def OpenNotepad(File):
        default_text_editor='notepad.exe'
        subprocess.Popen([default_text_editor,File])

    def ContentWriterAI(prompt):
        messages.append({"role":"user","content":f"{prompt}"})

        completion=client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages = SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer=""

        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer+=chunk.choices[0].delta.content
        Answer=Answer.replace("</s","")
        messages.append({"role":"assistant","content":Answer})
        return Answer
    Topic:str=Topic.replace("content","")
    ContentByAI=ContentWriterAI(Topic)

    with open(rf"Data\{Topic.lower().replace(' ','')}.txt","w",encoding="utf-8") as file:
        file.write(ContentByAI)
        file.close()
    
    OpenNotepad(rf" Data\{Topic.lower().replace(' ','')}.txt")
    return True

def YouTubeSearch(Topic):
    Url4Search=f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return True

def PlayYoutube(query):
    playonyt(query)
    return True


def OpenApp(app, sess=requests.session()):
    try:
        # Try opening the app using AppOpener
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except Exception as e:
        print(f"Error opening {app} using AppOpener: {e}")
        
        # If AppOpener fails, check for specific apps like Instagram
        if app.lower() == "instagram":
            # Open Instagram directly in the browser if it's not running
            webbrowser.open("https://www.instagram.com")
            return True
        elif app.lower() == "youtube":
            # Open YouTube directly in the browser if it's not running
            webbrowser.open("https://www.youtube.com")
            return True
        elif app.lower() == "spotify":
            # Open Spotify in the browser if it's not running
            webbrowser.open("https://www.spotify.com")
            return True
        # Add more conditions for other apps as needed
        else:
            print(f"No specific handler for {app}. Searching online...")
            # Search Google for the app or open its website
            search_url = f"https://www.google.com/search?q={app}"
            webbrowser.open(search_url)
            return True
def CloseApp(app):
    if "chrome" in app:
        pass
    else:
        try:
            close(app,match_closest=True,output=True,throw_error=True)
            return True
        except:
            return False
def System(command):
    def mute():
        keyboard.press_and_release("volume mute")
    def unmute():
        keyboard.press_and_release("volume unmute")
    def volume_up():
        keyboard.press_and_release("volume up")
    def volume_down():
        keyboard.press_and_release("volume down")

    if command=="mute":
        mute()
    elif command=="unmute":
        unmute()
    elif command=="volume up":
        volume_up()
    elif command=="volume down":
        volume_down()
    return True

async def TranslateAndExecute(commands:list[str]):
    funcs=[]
    for command in commands:
        if command.startswith("open "):
            if "open it" in command:
                pass
            if "open file" in command:
                pass
            else:
                fun=asyncio.to_thread(OpenApp,command.removeprefix("open "))
                funcs.append(fun)
        elif command.startswith("general "):
            pass
        elif command.startswith("realtime "):
            pass
        elif command.startswith("close "):
            fun=asyncio.to_thread(CloseApp,command.removeprefix("close "))
            funcs.append(fun)
        elif command.startswith("play "):
            fun=asyncio.to_thread(PlayYoutube,command.removeprefix("play "))
            funcs.append(fun)
        elif command.startswith("content "):
            fun=asyncio.to_thread(Content,command.removeprefix("content "))
            funcs.append(fun)
        elif command.startswith("google search "):
            fun=asyncio.to_thread(GoogleSearch,command.removeprefix("google search "))
            funcs.append(fun)
        elif command.startswith("youtube search "):
            fun=asyncio.to_thread(Content,command.removeprefix("content "))
            funcs.append(fun)
        elif command.startswith("system"):
            fun=asyncio.to_thread(System,command.removeprefix("system "))
            funcs.append(fun)
        else:
            print(f"No function found for {command}")
    
    results=await asyncio.gather(*funcs)
    
    for result in results:
        if isinstance(result,str):
            yield result
        else:
            yield result

async def Automation(commands:list[str]):
    async for result in TranslateAndExecute(commands):
        pass
    return True

if __name__=="__main__":
    OpenApp("Instagram")  # Will try to open the app, if not running, opens in browser
    OpenApp("YouTube")