import streamlit as st
import pandas as pd
from festival_data import festival_planner, festival_infromation
import streamlit_cached_functions
from charts.festival_showtime_chart import FestivalShowTimeChart
from music_managers.spotify_manager import SpotifyManager


class StreamlitUI:
    def __init__(self):
        self.festival_planner_instance = None
        self.file_path = f"festival_data/edc_2023.json"
        self.spotify_user = "aerialchemist"
        self.spotify_manger = SpotifyManager(st.secrets["spotify_client_id"], st.secrets["spotify_client_secret"])

        self.fest_info = festival_infromation.FestivalInformation()
        self.fest_info.load_concert_details(self.file_path)

        st.title("Festival Planner")
        st.write("""This tool helps users search through their Spotify 
                    to find artist for festivals and help plan the shows
                     based on their preferences""")

        self.sidebar()
        self.show_festival_information()
        self.show_spotify_infromation()

    def sidebar(self):
        st.sidebar.title("Planner Settings")
        input_text = st.sidebar.text_input("Spotify Account", placeholder=self.spotify_user)
        if st.sidebar.button("Search"):
            self.spotify_manger.check_username_exists(input_text)
            self.spotify_user = input_text
        uploaded_file = st.sidebar.file_uploader("Choose a JSON file", type="json")

    def load_gantt_chart(self):
        expander = st.expander("Show Schedule")
        graphs = {}
        show_dates = self.fest_info.get_all_festival_dates()
        for date in show_dates:
            all_artist = self.fest_info.get_all_artist_for_date(date)
            self.fest_info
            shows = []
            for artist in all_artist:
                show_data = self.fest_info.get_show_data(date, artist)
                shows.append([artist,
                              show_data["start-time"],
                              show_data["end-time"],
                              show_data['stage']])
            showtime_chart = FestivalShowTimeChart(shows)
            graphs[date] = showtime_chart.fig

        selected_graph = expander.selectbox("Select Date", list(graphs.keys()))
        expander.pyplot(graphs[selected_graph])

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
        self.show_expander_to_download_festival_data()

    def show_expander_to_download_festival_data(self):
        with st.expander("Festival Data"):
            st.write("Download the festival json file below to be able to make your own example")
            with open(self.file_path, 'r') as file:
                file_content = file.read()
            file_name = f'{self.fest_info.concert_data["name"]}_{self.fest_info.concert_data["year"]}.json'
            st.download_button('Click to Download', data=file_content, file_name=file_name)

    def show_spotify_infromation(self):
        st.header("Spotify Search")
        with st.expander("Artist found in User's Playlists"):
            playlist_data = streamlit_cached_functions.get_playlist_data(self.spotify_manger,
                                                                       self.spotify_user,
                                                                       self.fest_info)
            df = self.show_spotify_playlist_data(playlist_data)
            st.table(df)
        expander = st.expander("Suggested Planner")
        expander.write(
            "These are the suggest shows to go see and the information for the shows based on your preferences")
        show_dates = self.fest_info.get_all_festival_dates()
        recommended_tables, conflict_tables = streamlit_cached_functions.generate_festival_solver_tables(
            playlist_data,
            self.fest_info,
            show_dates,
            self.festival_planner_instance)
        selected_graph = expander.selectbox("Planner Date", list(show_dates))
        expander.write(
            "Shows with no conflicts")
        expander.table(recommended_tables[selected_graph])
        expander.write(
            "Shows with conflicts")
        expander.table(conflict_tables[selected_graph])

    def show_spotify_playlist_data(self, playlist_data):
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

        df = pd.DataFrame(data)
        return df


if __name__ == "__main__":
    application = StreamlitUI()
