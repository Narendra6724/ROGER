from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
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
import platform

env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")
classes = ["zCubwf", "hgKElc", " LTKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee",
           "tw-Data-text tw-text-small tw-ta",
           "IZ6rdc", "O5uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table__webanswers-table",
           "dDoNo ikb4Bd gsrt", "sXLaOe",
           "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
client = Groq(api_key=GroqAPIKey)
professional_responses = [
    "your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need not hesitate to ask.",
]
messages = []
SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ['Username']}, You're a content writer. you have to write "}]

def GoogleSearch(Topic):
    search(Topic)
    return True

def Content(Topic):
    def OpenNotepad(File):
        default_text_editor = 'notepad.exe'
        subprocess.Popen([default_text_editor, File])
    
    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"})
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )
        Answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content
        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})
        return Answer
    
    Topic: str = Topic.replace("Content ", "")
    ContentByAI = ContentWriterAI(Topic)
    with open(rf"Data\{Topic.lower().replace(' ','')}.txt", "w", encoding="utf-8") as file:
        file.write(ContentByAI)
        file.close()
    OpenNotepad(rf"Data\{Topic.lower().replace(' ','')}.txt")
    return True

def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return True

def PlayYouTube(query):
    playonyt(query)
    return True

def OpenApp(app, sess=requests.session()):
    print(f"Attempting to open app: {app}")
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        print(f"Successfully opened {app} using appopen")
        return True
    except Exception as e:
        print(f"Failed to open {app} using appopen: {e}")
        # Use Google search to find the app's official website
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser')
            # Look for links in common search result elements
            links = soup.find_all('a', href=True)
            valid_links = []
            for link in links:
                href = link.get('href')
                # Filter out Google-related links and invalid ones
                if href and "google" not in href.lower() and href.startswith("http"):
                    valid_links.append(href)
            return valid_links

        def search_google(query):
            url = f"https://www.google.com/search?q={query}+official+website"
            headers = {"User-Agent": useragent}
            try:
                print(f"Searching Google for: {url}")
                response = sess.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    print(f"Google search successful, status code: {response.status_code}")
                    return response.text
                else:
                    print(f"Failed to retrieve search results for {query}, status code: {response.status_code}")
                    return None
            except requests.exceptions.RequestException as e:
                print(f"Error during Google search for {query}: {e}")
                return None

        # Search for the app's official website
        html = search_google(app)
        if html:
            links = extract_links(html)
            if links:
                link = links[0]  # Take the first valid link
                print(f"Opening {app} via {link}")
                webopen(link)
                return True
            else:
                print(f"No valid links found for {app}, opening Google search page as fallback")
                search_url = f"https://www.google.com/search?q={app}+official+website"
                webopen(search_url)
                return False
        else:
            print(f"Failed to retrieve search results for {app}, opening Google search page as fallback")
            search_url = f"https://www.google.com/search?q={app}"
            webopen(search_url)
            return False
OpenApp("brave")
def CloseApp(app):
    if "chrome" in app:
        pass
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)
            return True
        except Exception as e:
            print(f"Error closing {app}: {e}")
            return False

def System(command):
    def mute():
        try:
            keyboard.press_and_release("volume_mute")  # Use volume_mute to toggle mute/unmute
            print("Mute command executed successfully")
        except Exception as e:
            print(f"Error executing mute command: {e}")

    def unmute():
        try:
            keyboard.press_and_release("volume_mute")  # Use volume_mute to toggle mute/unmute
            print("Unmute command executed successfully")
        except Exception as e:
            print(f"Error executing unmute command: {e}")

    def volume_up():
        try:
            keyboard.press_and_release("volume_up")
            print("Volume up command executed successfully")
        except Exception as e:
            print(f"Error executing volume up command: {e}")

    def volume_down():
        try:
            keyboard.press_and_release("volume_down")
            print("Volume down command executed successfully")
        except Exception as e:
            print(f"Error executing volume down command: {e}")

    # Platform-specific fallback (optional, for advanced handling)
    os_name = platform.system()
    print(f"Detected operating system: {os_name}")

    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()
    else:
        print(f"Unknown system command: {command}")
        return False
    return True

async def TranslateAndExecute(commands: list[str]):
    funcs = []
    for command in commands:
        if command.startswith("open "):
            if "open it" in command:
                pass
            if "open file" == command:
                pass
            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
                funcs.append(fun)
        elif command.startswith("general "):
            pass
        elif command.startswith("realtime "):
            pass
        elif command.startswith("close "):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
            funcs.append(fun)
        elif command.startswith("play "):
            fun = asyncio.to_thread(PlayYouTube, command.removeprefix("play "))
            funcs.append(fun)
        elif command.startswith("content "):
            fun = asyncio.to_thread(Content, command.removeprefix("content "))
            funcs.append(fun)
        elif command.startswith("google search "):
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))
            funcs.append(fun)
        elif command.startswith("youtube search "):
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search "))
            funcs.append(fun)
        elif command.startswith("system "):
            fun = asyncio.to_thread(System, command.removeprefix("system "))
            funcs.append(fun)
        else:
            print(f"No Function Found. For {command}")
    results = await asyncio.gather(*funcs)
    for result in results:
        if isinstance(result, str):
            yield result
        else:
            yield result

async def Automation(commands: list[str]):
    async for result in TranslateAndExecute(commands):
        pass
    return True