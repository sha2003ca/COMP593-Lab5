import sys
import requests
from urllib.parse import urlencode

api_dev_key = "8fc27602ffa62fa1e34e04417b949cda"


def get_pokemon_info(pokemon_name):
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name}/'
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Getting information for {pokemon_name}...success")
        return response.json()
    else:
        print(f"Getting information for {pokemon_name}...failure")
        print(f"Response code: {response.status_code} ({response.reason})")
        return None


def create_paste(title, body, expiration, public):
    api_url = "https://pastebin.com/api/api_post.php"
    api_paste_format = "text"
    params = {
        "api_dev_key": api_dev_key,
        "api_option": "paste",
        "api_paste_name": title,
        "api_paste_code": body,
        "api_paste_format": api_paste_format,
        "api_paste_private": public,
        "api_paste_expire_date": expiration,
    }
    response = requests.post(api_url, data=params)
    if response.status_code == 200 and 'pastebin.com/' in response.text:
        print("Posting new paste to PasteBin...success")
        print(response.text)
        return
    else:
        print("Posting new paste to PasteBin...failure")
        return None


def get_pokemon_name():
    if len(sys.argv) == 2:
        return sys.argv[1]
    else:
        print("Usage: python pokemon_paste.py <pokemon_name>")
        sys.exit()


def construct_paste(pokemon_info):
    name = pokemon_info["name"].capitalize()
    abilities = "\n".join(
        [ability["ability"]["name"] for ability in pokemon_info["abilities"]])
    title = f"{name}'s Abilities"
    body = abilities
    return (title, body)


def main():
    pokemon_name = get_pokemon_name()
    pokemon_info = get_pokemon_info(pokemon_name)
    if pokemon_info is not None:
        title, body = construct_paste(pokemon_info)
        expiration = '1M'
        public = 0
        paste_url = create_paste(title, body, expiration, public)


if __name__ == "__main__":
    main()