import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import plotly.express as px
import io
import logging
from norms import station_amenities_objects
import pdfkit
#Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
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
        logger.debug(f"Fetched {len(df)} rows from {worksheet_name}")
        return df

    def filter_sanctioned_works_by_station(self, df, station_code):
        filtered_df = df[df['Station Code'].apply(
            lambda x: station_code.lower() in [code.strip().lower() for code in str(x).split(',')]
        )]
        return filtered_df
def get_station_amenities(category):
    logger.debug(f"Fetching amenities for category: {category}")
    amenities = station_amenities_objects.get(category, None)
    if amenities:
        logger.debug(f"Amenities found for {category}: {amenities.keys()}")
    else:
        logger.warning(f"No amenities found for category: {category}")
    return amenities
def display_norms_card(category):
    norms = get_station_amenities(category)
    if norms:
        st.subheader(f"📜 Norms for {category}")

        with st.container():
            col1, col2, col3 = st.columns(3)

            with col1:
              st.markdown("### ✅ Minimum Essential Amenities")
              for amenity, value in norms["Minimum Essential Amenities"].items():
                  st.markdown(f"✔️ {amenity}: {value}")
          
            with col2:
                st.markdown("### 📌 Recommended Amenities")
                for amenity, value in norms["Recommended"].items():
                    st.markdown(f"🔹 {amenity}: {value}")
            
            with col3:
                st.markdown("### 🌟 Desirable Amenities")
                for amenity, value in norms["Desirable"].items():
                     st.markdown(f"✨ {amenity}: {value}")
    else:
        st.warning("No norms data available for this category.")

def download_button(df, filename='data.csv'):
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    st.download_button(label="📥 Download CSV", data=buffer.getvalue(), file_name=filename, mime='text/csv')

def display_norms_table(category):
    norms = get_station_amenities(category)
    if norms:
        st.subheader(f"📋 Norms & Amenities for {category}")
        for section, amenities in norms.items():
            st.markdown(f"### {section}")
            df = pd.DataFrame(amenities.items(), columns=["Amenity", "Value"])
            st.dataframe(df)
    else:
        st.warning("No norms data available for this category.")
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
                            <h5 style='color: #002868; text-align: left; font-size: 16px; margin-bottom: 5px;'>📄 {row.get('Short Name of Work', 'N/A')}</h5>
                            <hr style='border: 0.5px solid skyblue; margin: 5px 0;'>
                            <p style='margin: 3px 0; font-size: 13px;'><strong>Year:</strong> {row.get('Year of Sanction', 'N/A')}</p>
                            <p style='margin: 3px 0; font-size: 13px;'><strong>Allocation:</strong> {row.get('ALLOCATION', 'N/A')}</p>
                            <p style='margin: 3px 0; font-size: 13px;'><strong>Cost:</strong> {row.get('Current Cost', 'N/A')}</p>
                            <p style='margin: 3px 0; font-size: 13px;'><strong>Parent Work:</strong> {row.get('PARENT WORK', 'N/A')}</p>
                            <p style='margin: 3px 0; font-size: 13px;'><strong>Remarks:</strong> {row.get('Remarks', 'N/A')}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
def display_station_card_view(df):
    #for index, row in df.iterrows():
    for i in range(0, len(df), 2):  # Show 2 cards per row for better compactness
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(df):
                row = df.iloc[i + j]
                with cols[j]:
                 with st.container():
                    passenger_footfall = row.get('Passenger footfall', '0')
                    try:
                        passenger_footfall = int(passenger_footfall) / 30
                    except ValueError:
                        passenger_footfall = 'N/A'
                    st.markdown(
                        f"""
                        <style>
                            .responsive-grid {{
                                display: grid;
                                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                                gap: 10px;
                            }}
                        </style>
                        """,
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f"""
                        <div  style='background-color: #fff; padding: 10px; border-radius: 8px; 
                                            box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 10px;'>
                            <h3 style='color: #333;'>🚉 {row.get('Station code', 'N/A')} - ({row.get('STATION NAME', 'N/A')}) - {row.get('Categorisation', 'N/A')}</h3>
                            <div style=' gap: 10px;'>
                                <div style=' background-color: #ffffff; padding: 15px; border-radius: 8px; margin-bottom: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                                    <h4 style='color: #002868;'>📍 Jurisdiction</h4>
                                    <hr style='border: 0.5px solid skyblue;'>
                                    <div>
                                        <p><strong>📍Section:</strong> {row.get('Section', 'N/A')}</p>
                                        <p><strong>👤 Commercial Inspector:</strong> {row.get('CMI', 'N/A')} </p>
                                        <p> <strong>📌 DEN-Section:</strong> {row.get('DEN', 'N/A')} </p>
                                        <p> <strong>📌 Sr.DEN:</strong> {row.get('Sr.DEN', 'N/A')}</p>
                                    </div>
                                </div>
                                <div style=' background-color: #ffffff; padding: 15px; border-radius: 8px; margin-bottom: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                                    <h4 style='color: #002868;'>👥 Passenger Information</h4>
                                    <hr style='border: 0.5px solid skyblue;'>
                                    <div >
                                        <p><strong>💰 Earnings Range:</strong> {row.get('Earnings range', 'N/A')}</p>
                                        <p><strong>🚶 Passenger Range:</strong> {row.get('Passenger range', 'N/A')}</p>
                                        <p><strong>👣 Passenger Footfall:</strong> {passenger_footfall}</p>
                                    </div>
                                </div>
                            </div>
                            <div style='background-color: #f9f9f9; padding: 15px; border-radius: 10px;margin-bottom: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);'>
                                <h4 style='color: #002868;'>🏗️ Infrastructure</h4>
                                <hr style='border: px solid skyblue;'>
                                <div>
                                    <p><strong>🅿️ Platforms:</strong> {row.get('Platforms', 'N/A')}</p>
                                    <p><strong>🔢 Number of Platforms:</strong> {row.get('Number of Platforms', 'N/A')}</p>
                                    <p><strong>🛗 Platform Type:</strong> {row.get('Platform Type', 'N/A')}</p>
                                    <p><strong>🅿️ Parking:</strong> {row.get('Parking', 'N/A')}</p>
                                    <p><strong>🚻 Pay-and-Use:</strong> {row.get('Pay-and-Use', 'N/A')}</p>
                                </div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.markdown("---")

def convert_df_to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Report')
    return output.getvalue()

def convert_df_to_pdf(df):
    # Convert DataFrame to HTML and then to PDF using pdfkit
    html = df.to_html(index=False)
    pdf = pdfkit.from_string(html, False)
    return pdf
def display_station_categorisation_report(df):
    st.markdown("## Station Categorisation Report")
    # Group the stations DataFrame by "Categorisation"
    grouped = df.groupby("Categorisation")
    for category, group in grouped:
        # For the header, use the first row's Earnings and Passenger ranges
        earnings_range = group['Earnings range'].iloc[0]
        passenger_range = group['Passenger range'].iloc[0]
        st.markdown(f"### {category} | Earnings Range: {earnings_range} | Passenger Range: {passenger_range}")
        
        # Build a DataFrame with only Station Code and computed Avg Daily Footfall
        rows = []
        for _, row in group.iterrows():
            station_code = row['Station code']
            try:
                footfall = int(row['Passenger footfall']) / 30
                footfall = f"{footfall:.2f}"
            except Exception:
                footfall = 'N/A'
            rows.append({"Station Code": station_code, "Avg Daily Footfall": footfall})
        
        report_df = pd.DataFrame(rows)
        st.table(report_df)
        
        # Add download buttons for Excel and PDF
        excel_data = convert_df_to_excel(report_df)
        st.download_button(
            label="Download Excel",
            data=excel_data,
            file_name=f"{category}_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        try:
            pdf_data = convert_df_to_pdf(report_df)
            st.download_button(
                label="Download PDF",
                data=pdf_data,
                file_name=f"{category}_report.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error("PDF generation is not configured. Please install pdfkit and wkhtmltopdf.")
        
def main():
    # Compact Header Row with Title, Search, and View Mode
    col1, col2, col3 = st.columns([3, 2, 2])
    with col1:
        st.markdown("<h1 style='text-align: left; font-size: 26px; margin-bottom: 0;'>🚆 PH-53 Dashboard</h1>", unsafe_allow_html=True)
    with col2:
        station_query = st.text_input("🔍 Search", max_chars=5, key="search", help="Enter Station Code or Name").strip()
    with col3:
        # Updated view mode options to include Categorisation Report
        view_option = st.radio("View Mode", ["📊 Table", "📌 Card", "📋 Categorisation Report"], horizontal=True)
    
    st.markdown("---")
    
    credentials_file = st.secrets["credentials"]
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1rJbfhcnEVuGMwGkT8yBObb9Bk5Hx0uU224EGxfplGRc/edit?usp=sharing"
    dashboard = RailwayDashboard(credentials_file, spreadsheet_url)

    with st.spinner("Fetching Data..."):
        sanctioned_works_df = dashboard.fetch_data("All Sanctioned Works", 7)
        stations_df = dashboard.fetch_data("Stations", 1)

    # If Categorisation Report view is selected, show the full report
    if view_option == "📋 Categorisation Report":
        display_station_categorisation_report(stations_df)
    elif station_query:
        logger.debug(f"User searched for station: {station_query}")
        matching_stations = stations_df[stations_df.apply(
            lambda row: station_query.lower() in str(row['Station code']).lower() or station_query.lower() in str(row['STATION NAME']).lower(), axis=1
        )]

        if not matching_stations.empty:
            selected_station = matching_stations['Station code'].values[0]
            selected_station_info = matching_stations[matching_stations['Station code'] == selected_station]
            selected_station_name = selected_station_info['STATION NAME'].values[0]
            selected_categorization = selected_station_info['Categorisation'].values[0]
            logger.debug(f"Selected station category: {selected_categorization}")

            if view_option == "📊 Table":
                st.dataframe(selected_station_info)
                display_norms_table(selected_categorization)
            else:
                display_station_card_view(selected_station_info)
                display_norms_card(selected_categorization)

            matching_works = dashboard.filter_sanctioned_works_by_station(sanctioned_works_df, selected_station)
            if not matching_works.empty:
                st.subheader(f"📋 Sanctioned Works for {selected_station_name} ({selected_station})")
                if view_option == "📊 Table":
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