import streamlit as st
import requests

st.set_page_config(

    page_title='Hello world',
    layout='centered',
    initial_sidebar_state='auto',
    menu_items={
        'Get Help': 'https://streamlit.io/',
        'Report a bug': 'https://github.com',
        'About': 'About your application: **Hello world**'
        }
)

st.title('Anime Score Checker')
anime_name = st.text_input("Enter the name of an anime:")

# Replace with your own MyAnimeList API Key
api_key = "144d45cc1080fcd2dd9768ff99323ab1"

# Set up the headers for authentication
headers = {
    'X-MAL-CLIENT-ID': api_key
}

# API URL to search for anime by name
search_url = f'https://api.myanimelist.net/v2/anime?q={anime_name}&limit=1'  # Searching for the first result
    
# Send GET request to the API
response = requests.get(search_url, headers=headers)
    
if response.status_code == 200:
    data = response.json()
        
    if data.get('data'):
        # Extract the anime's ID from the search result
        anime_id = data['data'][0]['node']['id']

        url = f'https://api.myanimelist.net/v2/anime/{anime_id}?fields=mean'
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            title = data.get('title', None)
            score = data.get('mean', None)
            pic = data.get('main_picture', None)
            pic = pic.get('large', None)

        
        else:
            print(f"Error: {response.status_code}")
            
        if score is None:
            print(f"Anime: {title}, Score: No score available")
    else:
        print("No anime found with that name.")
else:
    print(f"Error: {response.status_code}")


# Create two columns
col1, col2 = st.columns(2)

# Place content inside the columns
with col1:
    st.header(title)
    st.write("Mal Score: ", score)

with col2:
    st.image(pic, use_container_width=True)