# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 11:57:25 2022

@author: ASUS
"""

import streamlit as st
st.set_page_config(page_title="Relaxation Songs Recommendation", layout="wide")

import pandas as pd
from sklearn.neighbors import NearestNeighbors
import streamlit.components.v1 as components

@st.cache(allow_output_mutation=True)
def load_data():
    df = pd.read_csv("track_df.csv")
    return df
audio_feats = ["acousticness", "danceability", "energy", "instrumentalness", "valence", "tempo"]
df = load_data()

def n_neighbors_uri_audio(start_year, end_year, test_feat):
    t_data = df[(df["release_year"]>=start_year) & (df["release_year"]<=end_year)]
    t_data = t_data.sort_values(by='track_popularity', ascending=False)[:500]
    neigh = NearestNeighbors()
    neigh.fit(t_data[audio_feats].to_numpy())
    n_neighbors = neigh.kneighbors([test_feat],       n_neighbors=len(t_data), return_distance=False)[0]
    uris = t_data.iloc[n_neighbors]["uri"].tolist()
    audios = t_data.iloc[n_neighbors][audio_feats].to_numpy()
    return uris, audios

title = "Song Recommendation Engine for Relaxation/Meditation"
st.title(title)
st.write("First of all, welcome! This is the place where you can customize what you want to listen to based on several key audio features. Try playing around with different settings and listen to the Relaxation/Meditation songs recommended by our system!")
st.markdown("##")
with st.container():
    col1, col2,col3 = st.columns((2,0.5,0.5))
    
    with col1:
        st.markdown("***Choose features to customize:***")
        start_year, end_year = st.slider(
            'Select the year range',
            1990, 2019, (2015, 2019)
        )
        acousticness = st.slider(
            'Acousticness',
            0.6, 1.0, 0.6)
        danceability = st.slider(
            'Danceability',
            0.0, 0.4, 0.0)
        energy = st.slider(
            'Energy',
            0.0, 0.4, 0.0)
        instrumentalness = st.slider(
            'Instrumentalness',
            0.0, 0.5, 0.0)
        valence = st.slider(
            'Valence',
            0.5, 1.0, 0.5)
        tempo = st.slider(
            'Tempo',
            0.0, 125.0, 62.0)


tracks_per_page = 6
test_feat = [acousticness, danceability, energy, instrumentalness, valence, tempo]
uris, audios = n_neighbors_uri_audio(start_year, end_year, test_feat)

tracks = []
for uri in uris:
    track = """<iframe src="https://open.spotify.com/embed/track/{}" width="260" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>""".format(uri)
    tracks.append(track)
    
if 'previous_inputs' not in st.session_state:
    st.session_state['previous_inputs'] = [start_year, end_year] + test_feat
    

    

if 'start_track_i' not in st.session_state:
    st.session_state['start_track_i'] = 0

with st.container():
    col1, col2, col3 = st.columns([2,1,2])
    if st.button("Recommend More Songs"):
        if st.session_state['start_track_i'] < len(tracks):
            st.session_state['start_track_i'] += tracks_per_page

    current_tracks = tracks[st.session_state['start_track_i']: st.session_state['start_track_i'] + tracks_per_page]
    current_audios = audios[st.session_state['start_track_i']: st.session_state['start_track_i'] + tracks_per_page]
    if st.session_state['start_track_i'] < len(tracks):
        for i, (track, audio) in enumerate(zip(current_tracks, current_audios)):
            if i%2==0:
                with col1:
                    components.html(
                        track,
                        height=400,
                    )
                    
                        
            else:
                with col3:
                    components.html(
                    track,
                    height=400,
                )
               

    else:
        st.write("No songs left to recommend")
