class StationAmenities:
    def __init__(self, category, amenities):
        self.category = category
        self.amenities = amenities

    def __repr__(self):
        return f"StationAmenities(category={self.category}, amenities={self.amenities})"

station_amenities_objects = {
    "NSG1": {
        "Minimum Essential Amenities": {
            "Drinking water": "20 taps/PF",
            "Waiting hall": "250 sqm",
            "Platform shelter": "500 sqm",
            "Urinals": "12",
            "Lighting": "As per norms",
            "Dustbins": "Yes",
            "Clock": "To be decided by zonal railways",
            "Time Table Display": "As per instructions",
            "Public Address System": "Yes",
            "Parking-circulatory area with lights": "As per instructions",
            "Electronic Train indicator board": "As per instructions",
            "Signage": "Yes",
            "Seating arrangement": "150 seats/PF",
            "Latrines": "12",
            "Foot over bridge": "1 with cover",
            "Water cooler": "2 on each PF"
        },
        "Recommended": {
            "Wi-Fi": "Yes",
            "CCTV Surveillance": "Yes",
            "Parking area with lights": "Yes",
            "Solar Power": "As per feasibility",
            "Escalators": "Yes",
            "Coach Guidance System": "Yes",
            "Travellator": "Yes",
            "Integrated Mobile Charging Stations": "Yes",
            "High mast lighting": "Yes"
        },
        "Desirable": {
            "Food Courts": "Yes",
            "Prepaid Taxi Service": "Yes",
            "Wheelchair Accessibility": "Yes",
            "Retiring Room": "Yes",
            "Waiting room with bathing facilities": "Yes",
            "Separate waiting for ladies": "Yes",
            "Enquiry System": "Yes",
            "Food Plaza": "Yes",
            "Automatic Vending Machines": "Yes",
            "Coin-operated Ticket Vending Machines": "Yes",
            "Second entry with booking office": "Yes",
            "Washable apron with direct watering facilities": "Yes",
            "Access control": "Yes"
        }
    },
    "NSG2": {
        "Minimum Essential Amenities": {
            "Drinking water": "20 taps/PF",
            "Waiting hall": "250 sqm",
            "Platform shelter": "500 sqm",
            "Urinals": "12",
            "Lighting": "As per norms",
            "Dustbins": "Yes",
            "Clock": "To be decided by zonal railways",
            "Time Table Display": "As per instructions",
            "Public Address System": "Yes",
            "Parking-circulatory area with lights": "As per instructions",
            "Electronic Train indicator board": "As per instructions",
            "Signage": "Yes",
            "Seating arrangement": "150 seats/PF",
            "Latrines": "12",
            "Foot over bridge": "1 with cover",
            "Water cooler": "2 on each PF"
        },
        "Recommended": {
            "Wi-Fi": "Yes",
            "CCTV Surveillance": "Yes",
            "Parking area with lights": "Yes",
            "Solar Power": "As per feasibility",
            "Escalators": "Yes",
            "Coach Guidance System": "Yes",
            "Travellator": "Yes",
            "Integrated Mobile Charging Stations": "Yes",
            "High mast lighting": "Yes"
        },
        "Desirable": {
            "Food Courts": "Yes",
            "Prepaid Taxi Service": "Yes",
            "Wheelchair Accessibility": "Yes",
            "Retiring Room": "Yes",
            "Waiting room with bathing facilities": "Yes",
            "Separate waiting for ladies": "Yes",
            "Enquiry System": "Yes",
            "Food Plaza": "Yes",
            "Automatic Vending Machines": "Yes",
            "Coin-operated Ticket Vending Machines": "Yes",
            "Second entry with booking office": "Yes",
            "Washable apron with direct watering facilities": "Yes"
        }
    },
    "NSG3": {
        "Minimum Essential Amenities": {
            "Drinking water": "20 taps/PF",
            "Waiting hall": "125 sqm",
            "Platform shelter": "400 sqm",
            "Urinals": "10",
            "Lighting": "As per norms",
            "Dustbins": "Yes",
            "Clock": "To be decided by zonal railways",
            "Time Table Display": "As per instructions",
            "Public Address System": "Yes",
            "Parking-circulatory area with lights": "As per instructions",
            "Electronic Train indicator board": "As per instructions",
            "Signage": "Yes",
            "Seating arrangement": "125 seats/PF",
            "Latrines": "10",
            "Foot over bridge": "1 with cover",
            "Water cooler": "2 on each PF"
        },
        "Recommended": {
            "Wi-Fi": "Yes",
            "CCTV Surveillance": "Yes",
            "Parking area with lights": "Yes",
            "Solar Power": "As per feasibility",
            "Escalators": "Yes",
            "Coach Guidance System": "Yes",
            "Travellator": "Yes",
            "Integrated Mobile Charging Stations": "Yes",
            "High mast lighting": "Yes"
        },
        "Desirable": {
            "Food Courts": "Yes",
            "Prepaid Taxi Service": "Yes",
            "Wheelchair Accessibility": "Yes",
            "Retiring Room": "Yes",
            "Waiting room with bathing facilities": "Yes",
            "Separate waiting for ladies": "Yes",
            "Enquiry System": "Yes",
            "Food Plaza": "Yes",
            "Automatic Vending Machines": "Yes",
            "Coin-operated Ticket Vending Machines": "Yes",
            "Modular Catering Stalls": "Yes"
        }
    },
    "NSG4": {
        "Minimum Essential Amenities": {
            "Drinking water": "20 taps/PF",
            "Waiting hall": "75 sqm",
            "Platform shelter": "200 sqm",
            "Urinals": "6",
            "Lighting": "As per norms",
            "Dustbins": "Yes",
            "Clock": "To be decided by zonal railways",
            "Time Table Display": "As per instructions",
            "Public Address System": "Yes",
            "Parking-circulatory area with lights": "As per instructions",
            "Electronic Train indicator board": "As per instructions",
            "Signage": "Yes",
            "Seating arrangement": "100 seats/PF",
            "Latrines": "6",
            "Foot over bridge": "1",
            "Water cooler": "2 on each main PF"
        },
        "Recommended": {
            "Wi-Fi": "Yes",
            "CCTV Surveillance": "Yes",
            "Parking area with lights": "Yes",
            "Solar Power": "As per feasibility",
            "Escalators": "Yes",
            "Coach Guidance System": "Yes",
            "Travellator": "Yes",
            "Integrated Mobile Charging Stations": "Yes",
            "High mast lighting": "Yes"
        },
        "Desirable": {
            "Food Courts": "Yes",
            "Prepaid Taxi Service": "Yes",
            "Wheelchair Accessibility": "Yes",
            "Retiring Room": "Yes",
            "Waiting room with bathing facilities": "Yes",
            "Separate waiting for ladies": "Yes",
            "Enquiry System": "Yes",
            "Food Plaza": "Yes",
            "Automatic Vending Machines": "Yes",
            "Coin-operated Ticket Vending Machines": "Yes"
        }
    },
    "NSG5": {
        "Minimum Essential Amenities": {
            "Drinking water": "8 taps/PF",
            "Waiting hall": "30 sqm",
            "Platform shelter": "50 sqm",
            "Urinals": "4",
            "Lighting": "As per norms",
            "Dustbins": "Yes",
            "Clock": "To be decided by zonal railways",
            "Time Table Display": "As per instructions",
            "Public Address System": "Yes",
            "Parking-circulatory area with lights": "As per instructions",
            "Electronic Train indicator board": "As per instructions",
            "Signage": "Yes",
            "Seating arrangement": "50 seats/PF",
            "Latrines": "4",
            "Foot over bridge": "As per norms"
        },
        "Recommended": {
            "Wi-Fi": "Yes",
            "CCTV Surveillance": "Yes",
            "Parking area with lights": "Yes",
            "Solar Power": "As per feasibility",
            "Escalators": "Yes",
            "Coach Guidance System": "Yes",
            "Travellator": "Yes",
            "Integrated Mobile Charging Stations": "Yes",
            "High mast lighting": "Yes"
        },
        "Desirable": {
            "Food Courts": "Yes",
            "Prepaid Taxi Service": "Yes",
            "Wheelchair Accessibility": "Yes",
            "Retiring Room": "Yes",
            "Waiting room with bathing facilities": "Yes",
            "Separate waiting for ladies": "Yes",
            "Enquiry System": "Yes",
            "Food Plaza": "Yes",
            "Automatic Vending Machines": "Yes",
            "Coin-operated Ticket Vending Machines": "Yes",
            "Cyber Caf\u00e9": "Yes",
            "Pay & Use Toilets": "Yes",
            "Access Control": "Yes"
        }
    },
    "NSG6": {
        "Minimum Essential Amenities": {
            "Drinking water": "2 taps/PF",
            "Waiting hall": "15 sqm",
            "Platform shelter": "50 sqm",
            "Urinals": "1",
            "Lighting": "As per norms",
            "Dustbins": "Yes",
            "Clock": "To be decided by zonal railways",
            "Time Table Display": "As per instructions",
            "Public Address System": "Yes",
            "Parking-circulatory area with lights": "As per instructions",
            "Electronic Train indicator board": "As per instructions",
            "Signage": "Yes",
            "Seating arrangement": "50 seats/PF",
            "Latrines": "1",
            "Foot over bridge": "1"
        },
        "Recommended": {
            "Wi-Fi": "Yes",
            "CCTV Surveillance": "Yes",
            "Parking area with lights": "Yes",
            "Solar Power": "As per feasibility",
            "Escalators": "Yes",
            "Coach Guidance System": "Yes",
            "Travellator": "Yes",
            "Integrated Mobile Charging Stations": "Yes",
            "High mast lighting": "Yes"
        },
        "Desirable": {
            "Food Courts": "Yes",
            "Prepaid Taxi Service": "Yes",
            "Wheelchair Accessibility": "Yes",
            "Retiring Room": "Yes",
            "Waiting room with bathing facilities": "Yes",
            "Separate waiting for ladies": "Yes",
            "Enquiry System": "Yes",
            "Food Plaza": "Yes",
            "Automatic Vending Machines": "Yes",
            "Coin-operated Ticket Vending Machines": "Yes",
            "Signage": "Yes",
            "Bottle crushers, vending machines": "Yes"
        }
    }
}

for i in range(2, 7):
    station_amenities_objects[f"NSG {i}"] = StationAmenities(
        f"NSG {i}", station_amenities_objects["NSG 1"].amenities.copy()
    )

halt_amenities_data = {
   
    "HG1": {
        "Minimum Essential Amenities": {
            "Drinking water": "Appropriate drinking water facility",
            "Waiting hall": "10 sqm booking office cum waiting hall",
            "Platform shelter": "Bus type modular shelter",
            "Urinals": "Yes",
            "Lighting": "As per norms",
            "Dustbins": "As per instructions",
            "Clock": "1",
            "Time Table Display": "As per instructions",
            "Public Address System": "Yes",
            "Parking-circulatory area with lights": "As per instructions",
            "Electronic Train indicator board": "As per instructions",
            "Signage": "Yes",
            "Platforms": "High Level",
            "FOB": "1"
        },
        "Recommended": {
            "Wi-Fi": "Yes",
            "CCTV Surveillance": "Yes",
            "Parking area with lights": "Yes",
            "Solar Power": "As per feasibility",
            "Escalators": "Yes",
            "Coach Guidance System": "Yes",
            "Travellator": "Yes",
            "Integrated Mobile Charging Stations": "Yes",
            "High mast lighting": "Yes",
            "Modular Catering Stalls": "Yes"
        },
        "Desirable": {
            "Food Courts": "Yes",
            "Prepaid Taxi Service": "Yes",
            "Wheelchair Accessibility": "Yes",
            "Retiring Room": "Yes",
            "Waiting room with bathing facilities": "Yes",
            "Separate waiting for ladies": "Yes",
            "Enquiry System": "Yes",
            "Food Plaza": "Yes",
            "Automatic Vending Machines": "Yes",
            "Coin-operated Ticket Vending Machines": "Yes",
            "Book Stalls": "Yes",
            "Water Vending Machines": "Yes",
            "ATMs": "Yes",
            "Pay & Use Toilets": "Yes",
            "Bus type shelter": "Yes"
        }
    },
    "HG2": {
        "Minimum Essential Amenities": {
            "Drinking water": "Appropriate drinking water facility",
            "Waiting hall": "10 sqm booking office cum waiting hall",
            "Platform shelter": "Shady trees",
            "Urinals": "Yes",
            "Lighting": "As per norms",
            "Dustbins": "As per instructions",
            "Clock": "-",
            "Time Table Display": "As per instructions",
            "Public Address System": "Yes",
            "Parking-circulatory area with lights": "As per instructions",
            "Electronic Train indicator board": "As per instructions",
            "Signage": "Yes",
            "Platforms": "High Level",
            "FOB": "1"
        },
        "Recommended": {
            "Wi-Fi": "Yes",
            "CCTV Surveillance": "Yes",
            "Parking area with lights": "Yes",
            "Solar Power": "As per feasibility",
            "Escalators": "Yes",
            "Coach Guidance System": "Yes",
            "Travellator": "Yes",
            "Integrated Mobile Charging Stations": "Yes",
            "High mast lighting": "Yes"
        },
        "Desirable": {
            "Food Courts": "Yes",
            "Prepaid Taxi Service": "Yes",
            "Wheelchair Accessibility": "Yes",
            "Retiring Room": "Yes",
            "Waiting room with bathing facilities": "Yes",
            "Separate waiting for ladies": "Yes",
            "Enquiry System": "Yes",
            "Food Plaza": "Yes",
            "Automatic Vending Machines": "Yes",
            "Coin-operated Ticket Vending Machines": "Yes"
        }
    },
    "HG3": {
        "Minimum Essential Amenities": {
            "Drinking water": "Yes",
            "Waiting hall": "-",
            "Platform shelter": "Shady trees",
            "Urinals": "Yes",
            "Lighting": "As per norms",
            "Dustbins": "As per instructions",
            "Clock": "-",
            "Time Table Display": "As per instructions",
            "Public Address System": "Yes",
            "Parking-circulatory area with lights": "As per instructions",
            "Electronic Train indicator board": "As per instructions",
            "Signage": "Yes",
            "Platforms": "High Level",
            "FOB": "1"
        },
        "Recommended": {
            "Wi-Fi": "Yes",
            "CCTV Surveillance": "Yes",
            "Parking area with lights": "Yes",
            "Solar Power": "As per feasibility",
            "Escalators": "Yes",
            "Coach Guidance System": "Yes",
            "Travellator": "Yes",
            "Integrated Mobile Charging Stations": "Yes",
            "High mast lighting": "Yes"
        },
        "Desirable": {
            "Food Courts": "Yes",
            "Prepaid Taxi Service": "Yes",
            "Wheelchair Accessibility": "Yes",
            "Retiring Room": "Yes",
            "Waiting room with bathing facilities": "Yes",
            "Separate waiting for ladies": "Yes",
            "Enquiry System": "Yes",
            "Food Plaza": "Yes",
            "Automatic Vending Machines": "Yes",
            "Coin-operated Ticket Vending Machines": "Yes",
            "Bus Shelter": "Yes"
        }
    }
}

for i in range(1, 4):
    station_amenities_objects[f"HG {i}"] = StationAmenities(
        f"HG {i}", {amenity: values[i - 1] for amenity, values in halt_amenities_data.items()}
    )

print(station_amenities_objects)
