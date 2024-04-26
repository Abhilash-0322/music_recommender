import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import webbrowser

CLIENT_ID = '445f4d10566043b897cafc061a2609a6'
CLIENT_SECRET = '54e1eba9297a45d59a04f01108b589e1'

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results['tracks']['items']:
        track = results['tracks']['items'][0]
        album_cover_url = track['album']['images'][0]['url']
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"  # Placeholder image

def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    for i in distances[1:6]:
        artist = music.iloc[i[0]].artist
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)

    return recommended_music_names, recommended_music_posters

def play_song_on_spotify(song_uri):
  """
  This function constructs a custom Spotify web player URL and opens it in a new browser tab/window.
  """
  spotify_web_player_url = f"https://open.spotify.com/track/{song_uri.split(':')[-1]}"
  webbrowser.open(spotify_web_player_url, new=2)

def play_song(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results['tracks']['items']:
        song_uri = results['tracks']['items'][0]['uri']
        play_song_on_spotify(song_uri)  # Use this function to play on Spotify
    else:
        st.error(f"Song '{song_name}' by '{artist_name}' not found on Spotify.")

st.header('Music Recommender System')
similarity = pickle.load(open('pkls/similarity.pkl', 'rb'))
music = pickle.load(open('pkls/df.pkl', 'rb'))

music_list = music['song'].values
selected_music = st.selectbox(
    "Type or select a song from the dropdown",
    music_list
)

if st.button('Show Recommendation'):
    recommended_music_names, recommended_music_posters = recommend(selected_music)
    col1, col2, col3, col4, col5 = st.columns(5)

    # Define song names and artist names outside the loop for clarity
    song_names = recommended_music_names
    artist_names = [music.loc[music['song'] == name, 'artist'].values[0] for name in song_names]

    with col1:
        st.text(recommended_music_names[0])
        st.image(recommended_music_posters[0])
        if st.button(f"Play {recommended_music_names[0]}", key=recommended_music_names[0]):
            play_song(song_names[0], artist_names[0])  # Use pre-defined names

    with col2:
        st.text(recommended_music_names[1])
        st.image(recommended_music_posters[1])
        if st.button(f"Play {recommended_music_names[1]}", key=recommended_music_names[1]):
            play_song(song_names[1], artist_names[1])
    with col3:
        st.text(recommended_music_names[2])
        st.image(recommended_music_posters[2])
        if st.button(f"Play {recommended_music_names[2]}", key=recommended_music_names[2]):
            play_song(song_names[2], artist_names[2])
    with col4:
        st.text(recommended_music_names[3])
        st.image(recommended_music_posters[3])
        if st.button(f"Play {recommended_music_names[3]}", key=recommended_music_names[3]):
            play_song(song_names[3], artist_names[3])
    with col5:
        st.text(recommended_music_names[4])
        st.image(recommended_music_posters[4])
        if st.button(f"Play {recommended_music_names[4]}", key=recommended_music_names[4]):
            play_song(song_names[4], artist_names[4])