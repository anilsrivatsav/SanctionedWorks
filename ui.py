import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

class RailwayDashboard:
    def __init__(self, credentials_file, spreadsheet_url):
        self.credentials_file = credentials_file
        self.spreadsheet_url = spreadsheet_url
        self.client = self.authenticate_google_sheets()
        self.sheet = self.client.open_by_url(self.spreadsheet_url)

        # Expected headers for "All Sanctioned Works" table
        self.sanctioned_works_headers = [
            'SN', 'PROJECTID', 'Year of Sanction', 'Date of sanction',
            'Short Name of Work', 'Block Section Station', 'Station Code',
            'ALLOCATION', 'Current Cost', 'Expenditure up to date',
            'Financial Progress', 'ENGG. REMARKS (as on 06.08.24)',
            'IF UB?', 'PARENT WORK', 'Section',
            'Anticipated Expenditure for Revised Grant Jan 2025 - Mar2025',
            'Remarks'
        ]

        # Expected headers for "Stations" table
        self.stations_headers = [
            'Station code', 'STATION NAME', 'DIVISION', 'ZONE', 'Section',
            'CMI', 'DEN', 'Sr.DEN', 'Categorisation', 'Earnings range',
            'Passenger range', 'Passenger footfall', 'Platforms',
            'Number of Platforms', 'Platform Type', 'Parking', 'Pay-and-Use'
        ]

    def authenticate_google_sheets(self):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_file, scope)
        return gspread.authorize(creds)

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

# ------------------------- Main Streamlit App -------------------------
def display_sanctioned_works_card_view(df):
    for i in range(0, len(df), 2):  # Display two cards per row
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(df):
                row = df.iloc[i + j]
                with cols[j]:
                    st.markdown(
                        f"""
                        <div style='background-color: #fff; padding: 15px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin-bottom: 20px;'>
                            <h4 style='color: #002868;'>📄 {row.get('Short Name of Work', 'N/A')}</h4>
                            <p style='color: #333;'><strong>Year of Sanction:</strong> {row.get('Year of Sanction', 'N/A')}</p>
                            <p style='color: #333;'><strong>ALLOCATION:</strong> {row.get('ALLOCATION', 'N/A')}</p>
                            <p style='color: #333;'><strong>Current Cost:</strong> {row.get('Current Cost', 'N/A')}</p>
                            <p style='color: #333;'><strong>PARENT WORK:</strong> {row.get('PARENT WORK', 'N/A')}</p>
                            <p style='color: #333;'><strong>Remarks:</strong> {row.get('Remarks', 'N/A')}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            

def display_station_card_view(df):
    for index, row in df.iterrows():
        with st.container():
            passenger_footfall = row.get('Passenger footfall', '0')
            try:
                passenger_footfall = int(passenger_footfall) / 30
            except ValueError:
                passenger_footfall = 'N/A'
            st.markdown(
                f"""
                <div style='background-color: #f9f9f9; padding: 15px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);'>
                    <h3 style='color: #333;'>🚉 {row.get('Station code', 'N/A')} - ({row.get('STATION NAME', 'N/A')}) - {row.get('Categorisation', 'N/A')}</h3>
                    <div style='display: flex; gap: 20px;'>
                        <div style='flex: 1; background-color: #ffffff; padding: 10px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                            <h4 style='color: #002868;'>📍 Jurisdiction</h4>
                            <p style='color: #333;'><strong>Section:</strong> {row.get('Section', 'N/A')}</p>
                            <p style='color: #333;'><strong>CMI:</strong> {row.get('CMI', 'N/A')} | <strong>DEN:</strong> {row.get('DEN', 'N/A')} | <strong>Sr.DEN:</strong> {row.get('Sr.DEN', 'N/A')}</p>
                        </div>
                        <div style='flex: 1; background-color: #ffffff; padding: 10px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                            <h4 style='color: #002868;'>👥 Passenger Information</h4>
                            <p style='color: #333;'><strong>Earnings Range:</strong> {row.get('Earnings range', 'N/A')}</p>
                            <p style='color: #333;'><strong>Passenger Range:</strong> {row.get('Passenger range', 'N/A')}</p>
                            <p style='color: #333;'><strong>Passenger Footfall:</strong> {passenger_footfall}</p>
                        </div>
                    </div>
                    <div style='background-color: #f9f9f9; padding: 15px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);'>
                        <h4 style='color: #002868;'>🏗️ Infrastructure</h4>
                        <p style='color: #333;'><strong>Platforms:</strong> {row.get('Platforms', 'N/A')}</p>
                        <p style='color: #333;'><strong>Number of Platforms:</strong> {row.get('Number of Platforms', 'N/A')}</p>
                        <p style='color: #333;'><strong>Platform Type:</strong> {row.get('Platform Type', 'N/A')}</p>
                        <p style='color: #333;'><strong>Parking:</strong> {row.get('Parking', 'N/A')} | <strong>Pay-and-Use:</strong> {row.get('Pay-and-Use', 'N/A')}</p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown("---")

def main():
    st.set_page_config(page_title="Railway Sanctioned Works Dashboard", layout="wide")
    st.title("🚆 Railway Sanctioned Works Dashboard")
    st.markdown("""---""")

    # Sidebar for inputs
    st.sidebar.header("Search Filters")
    station_query = st.sidebar.text_input("🔍 Enter Station Code or Name")
    view_option = st.sidebar.radio("Select View Mode", ("Table View", "Card View"))

    # Authentication and Data Fetching
    credentials_file = 'sanctioned-works-3ec757a1aa69.json'
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1rJbfhcnEVuGMwGkT8yBObb9Bk5Hx0uU224EGxfplGRc/edit?usp=sharing"

    dashboard = RailwayDashboard(credentials_file, spreadsheet_url)

    sanctioned_works_df = dashboard.fetch_data("All Sanctioned Works", 7)
    stations_df = dashboard.fetch_data("Stations", 1)

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
                else:
                    st.warning("No related works found for the selected station.")
        else:
            st.warning("No matching stations found.")
    else:
        st.info("Enter a Station Code or Name in the sidebar to search.")

if __name__ == "__main__":
    main()
