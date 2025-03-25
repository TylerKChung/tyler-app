import requests

def get_anime_info(anime_name, headers):
    """
    Fetches anime information from MyAnimeList API.
    
    Parameters:
        anime_name (str): The name of the anime to search.
        headers (dict): The request headers including authentication.
    
    Returns:
        dict: Anime title, score, and picture URL if found, otherwise None.
    """
    search_url = f'https://api.myanimelist.net/v2/anime?q={anime_name}&limit=1'
    response = requests.get(search_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None
    
    data = response.json()
    if not data.get('data'):
        print("No anime found with that name.")
        return None
    
    anime_id = data['data'][0]['node']['id']
    details_url = f'https://api.myanimelist.net/v2/anime/{anime_id}?fields=mean,main_picture,title'
    response = requests.get(details_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None
    
    anime_data = response.json()
    return {
        "title": anime_data.get("title"),
        "score": anime_data.get("mean", "No score available"),
        "picture": anime_data.get("main_picture", {}).get("large")
    }

def get_anime_score_anilist(anime_name):
    """
    Fetches anime score from AniList API and scales it down by dividing by 10.
    
    Parameters:
        anime_name (str): The name of the anime to search.
    
    Returns:
        float or str: Scaled anime score if found, otherwise None.
    """
    url = "https://graphql.anilist.co"
    query = """
    query ($search: String) {
      Media (search: $search, type: ANIME) {
        averageScore
      }
    }
    """
    variables = {"search": anime_name}
    response = requests.post(url, json={"query": query, "variables": variables})
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None
    
    data = response.json()
    anime = data.get("data", {}).get("Media")
    if not anime:
        print("No anime found with that name.")
        return None
    
    score = anime.get("averageScore")
    return round(score / 10, 1) if score is not None else "No score available"

# Example usage:
# score = get_anime_score_anilist("Naruto")
# print(score)

def get_anime_score_kitsu(anime_name):
    """
    Fetches anime score from Kitsu API.
    
    Parameters:
        anime_name (str): The name of the anime to search.
    
    Returns:
        float or str: Scaled anime score if found, otherwise a message.
    """
    search_url = f"https://kitsu.io/api/edge/anime?filter[text]={anime_name}"
    response = requests.get(search_url)
    
    if response.status_code != 200:
        return f"Error: {response.status_code}"
    
    data = response.json()
    if not data.get("data"):
        return "No anime found with that name."
    
    anime_info = data["data"][0]["attributes"]
    score = anime_info.get("averageRating")
    
    return round(float(score) / 10, 1) if score else "No score available"

# Example usage:
# score = get_anime_score_kitsu("Attack on Titan")
# print(score)