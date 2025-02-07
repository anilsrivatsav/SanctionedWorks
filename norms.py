class StationAmenities:
    def __init__(self, category, amenities):
        self.category = category
        self.amenities = amenities

    def __repr__(self):
        return f"StationAmenities(category={self.category}, amenities={self.amenities})"

station_amenities_objects = {
    "NSG 1": StationAmenities("NSG 1", {
        "Drinking water (Piped/Hand Pump)": "Yes",
        "Waiting hall": "Yes",
        "Seating arrangement": "Yes",
        "Platform shelter": "NSG1-NSG3: 1.4 to 5.0 sqm per passenger",
        "Urinals": "12",
        "Latrines": "12",
        "Platforms - High level": "Yes",
        "Lighting": "As per Board’s letter No. 2004/Elec(G)/138/5 dated 18.05.2007",
        "Fans": "As given below",
        "Foot over bridge": "1 with cover",
        "Time Table Display": "Yes",
        "Clock": "To be decided by zonal railways",
        "Water cooler": "2 on each PF",
        "Public Address system/Computer-based announcement": "As per extant instructions",
        "Parking-cum-circulatory area, with lights": "To be decided by the Zonal Railways",
        "Electronic Train indicator board": "To be decided by the Zonal Railways",
        "Signage (standardised)": "Yes",
        "Dustbins": "Yes",
        "Retiring room": "Yes",
        "Waiting room (Upper Class)": "Yes",
        "Waiting room (2nd class)": "Yes",
        "Separate for ladies (Upper & 2nd Class)": "Yes",
        "Clock room": "Yes",
        "Enquiry Counter": "Yes",
        "NTES": "Yes",
        "IVRS": "Yes",
        "Public Address system (With Speakers)": "Yes",
        "Refrigerated room": "Yes",
        "Tourist information counter": "Yes",
        "Washable apron with boundary wall": "Yes",
        "Enquiry system": "Yes",
        "Water vending machines": "Yes",
        "Escalators": "Yes",
        "Travellator": "Yes",
        "Modular Catering Stalls": "Yes",
        "Automatic Vending Machines": "Yes",
        "Pay & Use Toilets": "Yes",
        "Provision of cyber cafes": "Yes",
        "Provision of ATMs": "Yes",
        "Provision of at least one VIP Lounge": "Yes",
        "Food Plaza": "Yes",
        "Train coach indication system": "Yes",
        "CCTV for security purpose": "Yes",
        "Coin operated Ticket Vending Machines": "Yes",
        "Pre-paid Taxi service": "Yes",
        "Access Control": "Yes",
        "Separate Waiting Hall for senior citizens & Divyangjan": "Yes",
        "Wheelchair lifting devices / ramps": "Yes",
        "Water Fountain": "Yes"
    }),
}

for i in range(2, 7):
    station_amenities_objects[f"NSG {i}"] = StationAmenities(
        f"NSG {i}", station_amenities_objects["NSG 1"].amenities.copy()
    )

halt_amenities_data = {
    "Waiting room (Upper Class)": ["-", "-", "-"],
    "Waiting room (2nd Class)": ["Yes¹", "Yes¹", "-"],
    "Separate for ladies (Upper & 2nd Class)": ["-", "-", "-"],
    "Public Address system / Computer-based announcement": ["Yes", "-", "-"],
    "Book stalls / other stalls of essential goods": ["Yes²", "-", "-"],
    "Refreshment room": ["Yes", "-", "-"],
    "Parking / circulatory area with lights": ["Yes", "Yes", "-"],
    "Electronic Train indicator board": ["Yes", "Yes", "-"],
    "Touch Screen Enquiry system": ["Yes", "-", "-"],
    "Water vending machines": ["Yes*", "-", "-"],
    "Signage (standardized)": ["Yes", "Yes", "-"],
    "Modular Catering Stalls": ["Yes", "Yes", "-"],
    "Automatic Vending Machines": ["Yes", "-", "-"],
    "Pay & Use Toilets on end platforms & circulating area": ["Yes", "Yes", "Yes"],
    "Provision of ATMs (preferably with ticketing facility)": ["Yes", "-", "-"],
    "CCTV for announcement & security purpose": ["Yes", "-", "-"],
    "Coin operated Ticket Vending Machines": ["Yes", "-", "-"],
    "Bus type shelter": ["Yes", "-", "-"],
}

for i in range(1, 4):
    station_amenities_objects[f"HG {i}"] = StationAmenities(
        f"HG {i}", {amenity: values[i - 1] for amenity, values in halt_amenities_data.items()}
    )

print(station_amenities_objects)
