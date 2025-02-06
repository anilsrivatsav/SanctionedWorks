import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import plotly.express as px
import io

class RailwayDashboard:
    def __init__(self, credentials_file, spreadsheet_url):
        self.credentials_file = credentials_file
        self.spreadsheet_url = spreadsheet_url
        self.client = self.authenticate_google_sheets()
        self.sheet = self.client.open_by_url(self.spreadsheet_url)

        self.sanctioned_works_headers = [
            'SN', 'PROJECTID', 'Year of Sanction', 'Date of sanction',
            'Short Name of Work', 'Block Section Station', 'Station Code',
            'ALLOCATION', 'Current Cost', 'Expenditure up to date',
            'Financial Progress', 'ENGG. REMARKS (as on 06.08.24)',
            'IF UB?', 'PARENT WORK', 'Section',
            'Anticipated Expenditure for Revised Grant Jan 2025 - Mar2025',
            'Remarks'
        ]

        self.stations_headers = [
            'Station code', 'STATION NAME', 'DIVISION', 'ZONE', 'Section',
            'CMI', 'DEN', 'Sr.DEN', 'Categorisation', 'Earnings range',
            'Passenger range', 'Passenger footfall', 'Platforms',
            'Number of Platforms', 'Platform Type', 'Parking', 'Pay-and-Use'
        ]

    def authenticate_google_sheets(self):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = st.secrets["credentials"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
        return gspread.authorize(creds)

    @st.cache_data(ttl=600)
    def fetch_data(self, worksheet_name, start_row):
        worksheet = self.sheet.worksheet(worksheet_name)
        data = worksheet.get_all_values()
        df = pd.DataFrame(data[start_row:], columns=data[start_row - 1])
        return df

    def filter_sanctioned_works_by_station(self, df, station_code):
        filtered_df = df[df['Station Code'].apply(
            lambda x: station_code.lower() in [code.strip().lower() for code in str(x).split(',')]
        )]
        return filtered_df

def download_button(df, filename='data.csv'):
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    st.download_button(label="📥 Download CSV", data=buffer.getvalue(), file_name=filename, mime='text/csv')

def display_charts(df):
    if 'Current Cost' in df.columns and 'Station Code' in df.columns:
        fig = px.bar(df, x='Station Code', y='Current Cost', color='ALLOCATION')
        st.plotly_chart(fig)

def sidebar_filters():
    station_query = st.sidebar.text_input("🔍 Enter Station Code, Name, or Any Field")
    view_option = st.sidebar.radio("Select View Mode", ("Table View", "Card View"))
    return station_query, view_option

def display_sanctioned_works_card_view(df):
    for i in range(0, len(df), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(df):
                row = df.iloc[i + j]
                with cols[j]:
                    with st.expander(f"📄 {row.get('Short Name of Work', 'N/A')}"):
                        st.write(f"Year of Sanction: {row.get('Year of Sanction', 'N/A')}")
                        st.write(f"ALLOCATION: {row.get('ALLOCATION', 'N/A')}")
                        st.write(f"Current Cost: {row.get('Current Cost', 'N/A')}")
                        st.write(f"PARENT WORK: {row.get('PARENT WORK', 'N/A')}")
                        st.write(f"Remarks: {row.get('Remarks', 'N/A')}")

def display_station_card_view(df):
    for index, row in df.iterrows():
        with st.expander(f"🚉 {row.get('Station code', 'N/A')} - {row.get('STATION NAME', 'N/A')}"):
            passenger_footfall = row.get('Passenger footfall', '0')
            try:
                passenger_footfall = int(passenger_footfall) / 30
            except ValueError:
                passenger_footfall = 'N/A'

            st.write(f"**Categorisation:** {row.get('Categorisation', 'N/A')}")
            st.write(f"**Passenger Footfall:** {passenger_footfall}")
            st.write(f"**Platforms:** {row.get('Platforms', 'N/A')}, **Parking:** {row.get('Parking', 'N/A')}")

def main():
    st.set_page_config(page_title="PH-53 Dashboard", layout="wide")
    st.title("🚆 PH-53 Dashboard")
    st.markdown("""---""")

    credentials_file = st.secrets["credentials"]
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1rJbfhcnEVuGMwGkT8yBObb9Bk5Hx0uU224EGxfplGRc/edit?usp=sharing"

    dashboard = RailwayDashboard(credentials_file, spreadsheet_url)

    with st.spinner("Fetching Data..."):
        sanctioned_works_df = dashboard.fetch_data("All Sanctioned Works", 7)
        stations_df = dashboard.fetch_data("Stations", 1)

    station_query, view_option = sidebar_filters()

    if station_query:
        matching_stations = stations_df[stations_df.apply(
            lambda row: station_query.lower() in str(row['Station code']).lower() or station_query.lower() in str(row['STATION NAME']).lower(), axis=1
        )]

        if not matching_stations.empty:
            selected_station = st.sidebar.selectbox("Select a Station", matching_stations['Station code'].unique())

            if selected_station:
                selected_station_info = matching_stations[matching_stations['Station code'] == selected_station]
                selected_station_name = selected_station_info['STATION NAME'].values[0]

                st.subheader(f"📊 Station Details for {selected_station_name} ({selected_station})")
                if view_option == "Table View":
                    st.dataframe(selected_station_info)
                else:
                    display_station_card_view(selected_station_info)

                matching_works = dashboard.filter_sanctioned_works_by_station(sanctioned_works_df, selected_station)
                matching_works['Station Name'] = selected_station_name

                st.subheader(f"📋 Sanctioned Works for {selected_station_name} ({selected_station})")
                if not matching_works.empty:
                    if view_option == "Table View":
                        st.dataframe(matching_works)
                    else:
                        display_sanctioned_works_card_view(matching_works)

                    display_charts(matching_works)
                    download_button(matching_works, f"{selected_station}_works.csv")
                else:
                    st.warning("No related works found for the selected station.")
        else:
            st.warning("No matching stations found.")
    else:
        st.info("Enter a Station Code or Name in the sidebar to search.")

if __name__ == "__main__":
    main()
