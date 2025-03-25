import streamlit as st
import requests
import anime

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

# Initialize session state for clearing the search if not already set
if "anime_name" not in st.session_state:
    st.session_state.anime_name = ""
    st.session_state.score = None
    st.session_state.aniScore = None
    st.session_state.kitsuScore = None
    st.session_state.pic = None

st.title('Anime Score Checker')

# Take anime name as input with a unique key
anime_name = st.text_input("Enter the name of an anime:", value=st.session_state.anime_name, key="anime_name_input")

# Button to clear the current search
if st.button("Clear Search"):
    st.session_state.anime_name = ""
    st.session_state.score = None
    st.session_state.aniScore = None
    st.session_state.kitsuScore = None
    st.session_state.pic = None
    st.rerun()  # This will refresh the page

# Only show the columns after anime_name is entered
if anime_name:
    # Gathers data of the anime
    animeData = anime.get_anime_info(anime_name, headers=headers)
    title = animeData.get('title')
    score = animeData.get('score')
    pic = animeData.get('picture')
    aniScore = anime.get_anime_score_anilist(title)
    kitsuScore = anime.get_anime_score_kitsu(title)

    # Store the fetched data in session state
    st.session_state.anime_name = anime_name
    st.session_state.score = score
    st.session_state.aniScore = aniScore
    st.session_state.kitsuScore = kitsuScore
    st.session_state.pic = pic

    # Create two columns
    col1, col2 = st.columns(2)

    # Place content inside the columns
    with col1:
        st.header(title)
        st.write("Mal Score: ", st.session_state.score)
        st.write("AniList Score: ", st.session_state.aniScore)
        st.write("Kitsu Score: ", st.session_state.kitsuScore)

    with col2:
        st.image(st.session_state.pic, use_container_width=True)
