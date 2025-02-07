import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import plotly.express as px
import io
from norms import station_amenities_objects
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
    def fetch_data(_self, worksheet_name, start_row):
        worksheet = _self.sheet.worksheet(worksheet_name)
        data = worksheet.get_all_values()
    
        # Use the predefined column headers
        if worksheet_name == "All Sanctioned Works":
            required_columns = _self.sanctioned_works_headers
        elif worksheet_name == "Stations":
            required_columns = _self.stations_headers
        else:
            return pd.DataFrame()  # Return empty DataFrame if an unknown sheet is requested
    
        # Convert data to DataFrame
        df = pd.DataFrame(data[start_row:], columns=data[start_row - 1])
    
        # Keep only the required columns
        df = df[[col for col in required_columns if col in df.columns]]
    
        # Convert all values to string to prevent type errors
        df = df.astype(str)
    
        return df

    def filter_sanctioned_works_by_station(self, df, station_code):
        filtered_df = df[df['Station Code'].apply(
            lambda x: station_code.lower() in [code.strip().lower() for code in str(x).split(',')]
        )]
        return filtered_df
def get_station_amenities(category):
    """Fetch the amenities for the given station category."""
    return station_amenities_objects.get(category, None)
def display_norms_card(category):
    norms = get_station_amenities(category)
    if norms:
        st.subheader("📜 Norms & Amenities")

        with st.container():
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("### ✅ Minimum Essential Amenities")
                for amenity, value in norms.amenities.items():
                    if value == "Yes":
                        st.markdown(f"✔️ {amenity}")

            with col2:
                st.markdown("### 📌 Recommended Amenities")
                for amenity, value in norms.amenities.items():
                    if value in ["Yes¹", "Yes²"]:
                        st.markdown(f"🔹 {amenity}")

            with col3:
                st.markdown("### 🌟 Desirable Amenities")
                for amenity, value in norms.amenities.items():
                    if value not in ["Yes", "Yes¹", "Yes²", "-"]:
                        st.markdown(f"✨ {amenity}")
    else:
        st.warning("No norms data available for this category.")

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
    for i in range(0, len(df), 2):  # Show 2 cards per row for better compactness
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(df):
                row = df.iloc[i + j]
                with cols[j]:
                    st.markdown(
                        f"""
                        <div style='background-color: #fff; padding: 10px; border-radius: 8px; 
                                    box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 10px;'>
                            <h5 style='color: #002868; text-align: center; font-size: 14px; margin-bottom: 5px;'>📄 {row.get('Short Name of Work', 'N/A')}</h5>
                            <hr style='border: 0.5px solid skyblue; margin: 5px 0;'>
                            <p style='margin: 3px 0; font-size: 12px;'><strong>Year:</strong> {row.get('Year of Sanction', 'N/A')}</p>
                            <p style='margin: 3px 0; font-size: 12px;'><strong>Allocation:</strong> {row.get('ALLOCATION', 'N/A')}</p>
                            <p style='margin: 3px 0; font-size: 12px;'><strong>Cost:</strong> {row.get('Current Cost', 'N/A')}</p>
                            <p style='margin: 3px 0; font-size: 12px;'><strong>Parent Work:</strong> {row.get('PARENT WORK', 'N/A')}</p>
                            <p style='margin: 3px 0; font-size: 12px;'><strong>Remarks:</strong> {row.get('Remarks', 'N/A')}</p>
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
                <div style='background: #ffffff; padding: 10px; border-radius: 8px; 
                        box-shadow: 0 1px 3px rgba(0,0,0,0.15); margin-bottom: 10px;'>
                    <h4 style='color: #002868; margin-bottom: 5px;'>🚉 {row.get('Station code', 'N/A')} - {row.get('STATION NAME', 'N/A')} ({row.get('Categorisation', 'N/A')})</h4>
                
                    <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 14px;'>
                        <div style='flex: 1; background-color: #ffffff; padding: 10px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                            <h4 style='color: #002868;'>📍 Jurisdiction</h4>
                            <hr style='border: 0.5px solid skyblue;'>
                            <div style='display: flex; flex-wrap: wrap; gap: 10px;'>
                                <p style='flex: 1 50%;'><strong>Section:</strong> {row.get('Section', 'N/A')}</p>
                                <p style='flex: 1 50%;'><strong>CMI:</strong> {row.get('CMI', 'N/A')} </p>
                                <p style='flex: 1 50%;'> <strong>DEN:</strong> {row.get('DEN', 'N/A')} </p>
                                <p style='flex: 1 50%;'> <strong>Sr.DEN:</strong> {row.get('Sr.DEN', 'N/A')}</p>
                            </div>
                        </div>
                        <div style='flex: 1; background-color: #ffffff; padding: 10px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                            <h4 style='color: #002868;'>👥 Passenger Information</h4>
                            <hr style='border: 0.5px solid skyblue;'>
                            <div style='display: flex; flex-wrap: wrap; gap: 10px;'>
                                <p style='flex: 1 50%;'><strong>Earnings Range:</strong> {row.get('Earnings range', 'N/A')}</p>
                                <p style='flex: 1 50%;'><strong>Passenger Range:</strong> {row.get('Passenger range', 'N/A')}</p>
                                <p style='flex: 1 50%;'><strong>Passenger Footfall:</strong> {passenger_footfall}</p>
                            </div>
                        </div>
                    </div>
                    <div style='background-color: #f9f9f9; padding: 15px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);'>
                        <h4 style='color: #002868;'>🏗️ Infrastructure</h4>
                        <hr style='border: 0.5px solid skyblue;'>
                        <div style='display: flex; flex-wrap: wrap; gap: 10px;'>
                                <p style='flex: 1 50%;'><strong>Platforms:</strong> {row.get('Platforms', 'N/A')}</p>
                                <p style='flex: 1 50%;'><strong>Number of Platforms:</strong> {row.get('Number of Platforms', 'N/A')}</p>
                                <p style='flex: 1 50%;'><strong>Platform Type:</strong> {row.get('Platform Type', 'N/A')}</p>
                                <p style='flex: 1 50%;'><strong>Parking:</strong> {row.get('Parking', 'N/A')} </p>
                                <p style='flex: 1 50%;'><strong>Pay-and-Use:</strong> {row.get('Pay-and-Use', 'N/A')}</p>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown("---")


def main():
    st.set_page_config(page_title="PH-53 Dashboard", layout="wide")

    # Centered Title
    st.markdown("<h1 style='text-align: center; font-size: 30px;'>🚆 PH-53 Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("""---""")  # Separator


    # Small, Center-Aligned Input Box (Max 10 Characters)
    col1, col2, col3, col4 = st.columns([1, 2, 3, 1])  # Adjust column widths for alignment
    with col2:
        st.markdown("<h4 style='text-align: right; margin-top: 7px;'>🔍 Search</h4>", unsafe_allow_html=True)
    with col3:
         station_query = st.text_input("Enter Station Code or Name", max_chars=5, key="search", help="Enter a 5-character Station Code").strip()

    # View Mode Chips (Instead of Dropdown)
    col4, col5, col6 = st.columns([1, 3, 1])  # Center alignment
    with col5:
        view_option = st.radio("View Mode", ["📊 Table View", "📌 Card View"], horizontal=True)

    st.markdown("""---""")  # Separator below the search card

    credentials_file = st.secrets["credentials"]
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1rJbfhcnEVuGMwGkT8yBObb9Bk5Hx0uU224EGxfplGRc/edit?usp=sharing"

    dashboard = RailwayDashboard(credentials_file, spreadsheet_url)

    with st.spinner("Fetching Data..."):
        sanctioned_works_df = dashboard.fetch_data("All Sanctioned Works", 7)
        stations_df = dashboard.fetch_data("Stations", 1)

    if station_query:
        matching_stations = stations_df[stations_df.apply(
            lambda row: station_query.lower() in str(row['Station code']).lower() or station_query.lower() in str(row['STATION NAME']).lower(), axis=1
        )]

        if not matching_stations.empty:
            selected_station = matching_stations['Station code'].values[0]
            selected_station_info = matching_stations[matching_stations['Station code'] == selected_station]
            selected_station_name = selected_station_info['STATION NAME'].values[0]
            selected_categorization = selected_station_info['Categorisation'].values[0]


            st.subheader(f"📊 Station Details for {selected_station_name} ({selected_station})")
            if "Table View" in view_option:
                st.dataframe(selected_station_info)
            else:
                display_station_card_view(selected_station_info)

            # Display Norms Card
            display_norms_card(selected_categorization)

            matching_works = dashboard.filter_sanctioned_works_by_station(sanctioned_works_df, selected_station)

            if not matching_works.empty:
                st.subheader(f"📋 Sanctioned Works for {selected_station_name} ({selected_station})")

                if "Table View" in view_option:
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
        st.info("Enter a Station Code or Name in the search box to search.")

if __name__ == "__main__":
    main()
