import streamlit as st
import festival_planner
import festival_infromation
import pandas as pd
from charts.festival_show_time_chart import FestivalShowTimeChart
from music_managers.spotify_manager import SpotifyManager


class StreamlitUI:
    def __init__(self):
        self.festival_planner_instance = None
        self.file_path = f"festival_data/festival_info.json"
        self.spotify_user = "aerialchemist"

        st.title("Festival Planner")
        st.write("""This tool helps users search through their Spotify 
                    to find artist for festivals and help plan the shows
                     based on their preferences""")
        self.sidebar()

        self.fest_info = festival_infromation.FestivalInfromation()
        self.fest_info.load_concert_details(self.file_path)
        self.show_festival_information()

        self.spotify_manger = SpotifyManager(st.secrets["spotify_client_id"], st.secrets["spotify_client_secret"])
        self.show_spotify_infromation()

    def sidebar(self):
        st.sidebar.title("Planner Settings")

        input_text = st.sidebar.text_input("Spotify Account", placeholder=self.spotify_user)
        if st.sidebar.button("Search"):
            self.spotify_manger.check_username_exists(input_text)
            self.spotify_user = input_text

        uploaded_file = st.sidebar.file_uploader("Choose a JSON file", type="json")

    def load_gantt_chart(self):
        all_artist = self.fest_info.get_all_artist()
        shows = []
        for artist in all_artist:
            shows.append([artist,
                          self.fest_info.concert_data["shows"][artist]["start-time"],
                          self.fest_info.concert_data["shows"][artist]["end-time"],
                          self.fest_info.concert_data["shows"][artist]['stage']])

        showtime_chart = FestivalShowTimeChart(shows)
        with st.expander("Show Schedule"):
            st.pyplot(showtime_chart.fig)

    def show_festival_information(self):
        st.image(self.fest_info.concert_data["image_url"], caption=self.fest_info.concert_data["name"],
                 use_column_width=True)
        st.header(self.fest_info.concert_data["name"])
        st.write(self.fest_info.concert_data["year"])
        st.write(self.fest_info.concert_data["description"])

        with st.expander("Festival Map"):
            if self.fest_info.concert_data["map_image_url"] != "":
                st.image(self.fest_info.concert_data["map_image_url"], caption=self.fest_info.concert_data["name"],
                         use_column_width=True)

        self.festival_planner_instance = festival_planner.FestivalPlanner()
        self.load_gantt_chart()

        with st.expander("Festival Data"):
            st.write("Download the festival json file below to be able to make your own example")
            with open(self.file_path, 'r') as file:
                file_content = file.read()

            # Specify the file name
            file_name = f'{self.fest_info.concert_data["name"]}_{self.fest_info.concert_data["year"]}.json'

            # Download the JSON file
            st.download_button('Click to Download', data=file_content, file_name=file_name)


    def show_spotify_infromation(self):
        st.header("Spotify Search")
        playlist_data = self.spotify_manger.search_spotify_playlists(self.spotify_user, self.fest_info.get_all_artist())
        with st.expander("Artist found in User's Playlists"):
            data = {
                'Artist': [],
                '# Songs': [],
                'Playlist': []
            }
            for artist in playlist_data:
                if playlist_data[artist] > 0:
                    data["Artist"].append(artist)
                    data["# Songs"].append(playlist_data[artist])
                    data["Playlist"].append("")

            # Create a DataFrame from the data
            df = pd.DataFrame(data)

            # Display the table
            st.table(df)

        with st.expander("Suggested Planner"):
            st.write(
                "These are the suggest shows to go see and the information for the shows based on your preferences")


if __name__ == "__main__":
    application = StreamlitUI()
