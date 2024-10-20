import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import unquote

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def colored_text(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

def find_mp3_url(page_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Referer': page_url,
        'Origin': 'https://instromusic.com',
    }
    response = requests.get(page_url, headers=headers)
    
    if response.status_code != 200:
        print(colored_text(f"failed to load page.. code: {response.status_code}", '38;5;214'))
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    audio_div = soup.find('div', class_='compact_audio_player_wrapper')

    if not audio_div:
        print(colored_text("audio player element not found on page, is the link valid?", '38;5;214'))
        return None

    play_button = audio_div.find('input', {'onclick': True})

    if not play_button:
        print(colored_text("play button element not found on page, is the link valid?", '38;5;214'))
        return None

    onclick_content = play_button['onclick']
    start_index = onclick_content.find("https://instromusic.net/mp3/")
    end_index = onclick_content.find("'", start_index)

    if start_index == -1 or end_index == -1:
        print(colored_text("mp3 url not found in play button html, try again..", '38;5;214'))
        return None

    mp3_url = onclick_content[start_index:end_index]
    return mp3_url

def download_mp3(mp3_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://instromusic.com/',
        'Connection': 'keep-alive',
        'Origin': 'https://instromusic.com',
    }
    response = requests.get(mp3_url, headers=headers)

    if response.status_code == 200:
        filename = mp3_url.split("/")[-1]
        decoded_filename = unquote(filename)
        with open(decoded_filename, 'wb') as f:
            f.write(response.content)
        print(colored_text(f"file downloaded successfully as {decoded_filename}.", '38;5;214'))
    else:
        print(colored_text(f"download failed.. code: {response.status_code}", '38;5;214'))

def main():
    clear_terminal()
    print(colored_text(r"""                 
             _/_          /                //           /      
 o ____  _   /  __  __ __/ __ , , , ____  // __ __.  __/ _  __ 
<_/ / <_/_)_<__/ (_(_)(_/_(_)(_(_/_/ / <_</_(_)(_/|_(_/_</_/ (_
    """, '38;5;214'))
    
    page_url = input(colored_text("instromusic url: ", '38;5;214'))
    mp3_url = find_mp3_url(page_url)

    if mp3_url:
        print(colored_text(f"file url found!!: {mp3_url}", '38;5;214'))
        download_mp3(mp3_url)
    else:
        print(colored_text("could not find the url of the file..", '38;5;214'))

if __name__ == "__main__":
    main()