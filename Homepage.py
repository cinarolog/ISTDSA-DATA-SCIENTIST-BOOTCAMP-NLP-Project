import streamlit as st
import pandas as pd
import numpy as np
import math 

# Sayfa Ayarları
st.set_page_config(
    page_title="Spotify Recommendation Systems",
    page_icon="https://miro.medium.com/v2/resize:fit:2400/1*rGi8_JUoGX0L3W6nivmIAg@2x.png",
    menu_items={
        "Get help": "mailto:mhmmtcnr81@gmail.com",
        "About": "For More Information\n" + "https://github.com/cinarolog"
    }
)

st.info("Firsly enter the song name likeDream ship	DJ RYOW	,7 Things - Single Version	,Movement	Lylos	, after click submit")

new_df = pd.read_csv("data/last.csv")


def recommendations(data, track_name, song_count):

    """
    This function calculates the euclidian distance between
    points which are in the same cluster.
    """

    i = data[data['track_name'] == track_name].index[0]
    cluster = data['KMeans'][i]

    df = data[data['KMeans'] == cluster]
    df.reset_index(drop = True, inplace = True)
    ind = df[df['track_name'] == track_name].index[0]
    PCA = data[['PCA1','PCA2']].to_numpy()

    similarity = []
    for j in range(len(df)):
        distance = math.dist(PCA[ind], PCA[j])
        similarity.append(distance)

    df['similarity'] = similarity
    df.sort_values('similarity', inplace = True)
    df['track_id'] = df['track_id'].apply(lambda x: 'https://open.spotify.com/track/' + x)

    x = pd.DataFrame(df.iloc[1:song_count + 1, [1,2,0]].values, columns = ['Track', 'Artist', 'spotify_link'])
    # First value is the songs itself. So we skip it by starting the index 1.

    return x



number_of_songs= st.sidebar.number_input("Number of Songs", min_value=1, format="%d")

choose_song_with_num= st.sidebar.number_input("Choose Song", min_value=1, format="%d")
song_name= st.sidebar.text_input("Song Name", help="Please capitalize the first letter of your name!")

df_songs=recommendations(new_df,song_name, number_of_songs)

if st.sidebar.button("Submit"):

    # Info mesajı oluşturma
    st.info("You can find the result below.")

   
    st.table(recommendations(new_df,song_name, number_of_songs))

else:
    st.markdown("Please click the *Submit Button*!")


st.table(df_songs.spotify_link[:10])


if st.button("Find Music"):

    # Info mesajı oluşturma
    st.info("You can find the songs link below.")

   
    st.markdown(df_songs.spotify_link[choose_song_with_num])

else:
    st.markdown("Please click the *Submit Button*!")
