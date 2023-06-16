import streamlit as st
import main
import festival_infromation
import pandas as pd
from charts.festival_show_time_chart import FestivalShowTimeChart


class StreamlitUI:
    def __init__(self):
        st.title("Concert Planner")
        st.write("""This tool helps users search through their Spotify 
                    to find artist for festivals and help plan the shows
                     based on their preferences""")
        self.sidebar()
        file_path = f"festival_data/festival_info.json"
        self.fest_info = festival_infromation.FestivalInfromation()
        self.fest_info.load_concert_details(file_path)

        st.image(self.fest_info.concert_data["image_url"], caption=self.fest_info.concert_data["name"], use_column_width=True)
        st.header(self.fest_info.concert_data["name"])
        st.write(self.fest_info.concert_data["year"])
        st.write(self.fest_info.concert_data["description"])

        with st.expander("Festival Map"):
            if self.fest_info.concert_data["map_image_url"] != "":
                st.image(self.fest_info.concert_data["map_image_url"], caption=self.fest_info.concert_data["name"], use_column_width=True)

        self.festival_planner_instance = main.FestivalPlanner(file_path)
        self.load_gantt_chart()

        st.header("Spotify Search")
        with st.expander("Artist found in User's Playlists"):
            data = {
                'Artist': ['John', 'Jane', 'Alice', 'Bob'],
                '# Songs': [25, 30, 28, 35],
                'Playlist': ['New York', 'London', 'Paris', 'Tokyo']
            }

            # Create a DataFrame from the data
            df = pd.DataFrame(data)

            # Display the table
            st.table(df)

        with st.expander("Suggested Planner"):
            st.write("These are the suggest shows to go see and the information for the shows based on your preferences")

    def sidebar(self):
        st.sidebar.title("Planner Settings")

        input_text = st.sidebar.text_input("Spotify Account")
        if st.sidebar.button("Search"):
            st.write("You entered:", input_text)

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


if __name__ == "__main__":
    application = StreamlitUI()
