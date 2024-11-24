from shiny import App, reactive, render, ui
import pandas as pd 

data_path = "C:/Users/15535/OneDrive/文档/GitHub/ps6/top_alerts_map/df_alert_counts.csv"
df_alert_counts = pd.read_csv(data_path)
crosswalk_data = [
    # ACCIDENT
    {"type": "ACCIDENT", "subtype": "ACCIDENT_MINOR", "updated_type": "Accident", "updated_subtype": "Minor", "updated_subsubtype": "Minor"},
    {"type": "ACCIDENT", "subtype": "ACCIDENT_MAJOR", "updated_type": "Accident", "updated_subtype": "Major", "updated_subsubtype": "Major"},
    {"type": "ACCIDENT", "subtype": "Unclassified", "updated_type": "Accident", "updated_subtype": "Unclassified", "updated_subsubtype": "Unclassified"},

    # JAM
    {"type": "JAM", "subtype": "JAM_MODERATE_TRAFFIC", "updated_type": "Jam", "updated_subtype": "Traffic", "updated_subsubtype": "Moderate"},
    {"type": "JAM", "subtype": "JAM_HEAVY_TRAFFIC", "updated_type": "Jam", "updated_subtype": "Traffic", "updated_subsubtype": "Heavy"},
    {"type": "JAM", "subtype": "JAM_STAND_STILL_TRAFFIC", "updated_type": "Jam", "updated_subtype": "Traffic", "updated_subsubtype": "Stand Still"},
    {"type": "JAM", "subtype": "JAM_LIGHT_TRAFFIC", "updated_type": "Jam", "updated_subtype": "Traffic", "updated_subsubtype": "Light"},
    {"type": "JAM", "subtype": "Unclassified", "updated_type": "Jam", "updated_subtype": "Unclassified", "updated_subsubtype": "Unclassified"},

    # WEATHERHAZARD / HAZARD
    {"type": "HAZARD", "subtype": "HAZARD_ON_ROAD", "updated_type": "Hazard", "updated_subtype": "On Road", "updated_subsubtype": "Unclassified"},
    {"type": "HAZARD", "subtype": "HAZARD_ON_SHOULDER", "updated_type": "Hazard", "updated_subtype": "On Shoulder", "updated_subsubtype": "Unclassified"},
    {"type": "HAZARD", "subtype": "HAZARD_WEATHER", "updated_type": "Hazard", "updated_subtype": "Weather", "updated_subsubtype": "Unclassified"},
    {"type": "HAZARD", "subtype": "HAZARD_ON_ROAD_OBJECT", "updated_type": "Hazard", "updated_subtype": "On Road", "updated_subsubtype": "Object"},
    {"type": "HAZARD", "subtype": "HAZARD_ON_ROAD_POT_HOLE", "updated_type": "Hazard", "updated_subtype": "On Road", "updated_subsubtype": "Pot Hole"},
    {"type": "HAZARD", "subtype": "HAZARD_ON_ROAD_ROAD_KILL", "updated_type": "Hazard", "updated_subtype": "On Road", "updated_subsubtype": "Road Kill"},
    {"type": "HAZARD", "subtype": "HAZARD_ON_SHOULDER_CAR_STOPPED", "updated_type": "Hazard", "updated_subtype": "On Shoulder", "updated_subsubtype": "Car Stopped"},
    {"type": "HAZARD", "subtype": "HAZARD_ON_SHOULDER_ANIMALS", "updated_type": "Hazard", "updated_subtype": "On Shoulder", "updated_subsubtype": "Animals"},
    {"type": "HAZARD", "subtype": "HAZARD_ON_SHOULDER_MISSING_SIGN", "updated_type": "Hazard", "updated_subtype": "On Shoulder", "updated_subsubtype": "Missing Sign"},
    {"type": "HAZARD", "subtype": "HAZARD_WEATHER_FOG", "updated_type": "Hazard", "updated_subtype": "Weather", "updated_subsubtype": "Fog"},
    {"type": "HAZARD", "subtype": "HAZARD_WEATHER_HAIL", "updated_type": "Hazard", "updated_subtype": "Weather", "updated_subsubtype": "Hail"},
    {"type": "HAZARD", "subtype": "HAZARD_WEATHER_HEAVY_SNOW", "updated_type": "Hazard", "updated_subtype": "Weather", "updated_subsubtype": "Heavy Snow"},
    {"type": "HAZARD", "subtype": "HAZARD_WEATHER_FLOOD", "updated_type": "Hazard", "updated_subtype": "Weather", "updated_subsubtype": "Flood"},
    {"type": "HAZARD", "subtype": "HAZARD_ON_ROAD_LANE_CLOSED", "updated_type": "Hazard", "updated_subtype": "On Road", "updated_subsubtype": "Lane Closed"},
    {"type": "HAZARD", "subtype": "HAZARD_ON_ROAD_ICE", "updated_type": "Hazard", "updated_subtype": "On Road", "updated_subsubtype": "Ice"},
    {"type": "HAZARD", "subtype": "HAZARD_ON_ROAD_CONSTRUCTION", "updated_type": "Hazard", "updated_subtype": "On Road", "updated_subsubtype": "Construction"},
    {"type": "HAZARD", "subtype": "HAZARD_ON_ROAD_CAR_STOPPED", "updated_type": "Hazard", "updated_subtype": "On Road", "updated_subsubtype": "Car Stopped"},
    {"type": "HAZARD", "subtype": "HAZARD_ON_ROAD_TRAFFIC_LIGHT_FAULT", "updated_type": "Hazard", "updated_subtype": "On Road", "updated_subsubtype": "Traffic Light Fault"},
    {"type": "HAZARD", "subtype": "HAZARD_ON_ROAD_EMERGENCY_VEHICLE", "updated_type": "Hazard", "updated_subtype": "On Road", "updated_subsubtype": "Emergency Vehicle"},
    {"type": "HAZARD", "subtype": "Unclassified", "updated_type": "Hazard", "updated_subtype": "Unclassified", "updated_subsubtype": "Unclassified"},

    
    # ROAD_CLOSED
    {"type": "ROAD_CLOSED", "subtype": "ROAD_CLOSED_HAZARD", "updated_type": "Road Closed", "updated_subtype": "Hazard", "updated_subsubtype": "Unclassified"},
    {"type": "ROAD_CLOSED", "subtype": "ROAD_CLOSED_CONSTRUCTION", "updated_type": "Road Closed", "updated_subtype": "Construction", "updated_subsubtype": "Unclassified"},
    {"type": "ROAD_CLOSED", "subtype": "ROAD_CLOSED_EVENT", "updated_type": "Road Closed", "updated_subtype": "Event", "updated_subsubtype": "Unclassified"},
    {"type": "ROAD_CLOSED", "subtype": "Unclassified", "updated_type": "Road Closed", "updated_subtype": "Unclassified", "updated_subsubtype": "Unclassified"},
]

crosswalk_df = pd.DataFrame(crosswalk_data)

# Define the Shiny app UI
dropdown_options = {}
for _, row in crosswalk_df.iterrows():
    if row["updated_type"] not in dropdown_options:
        dropdown_options[row["updated_type"]] = {}
    dropdown_options[row["updated_type"]][
        f"{row['updated_type']} - {row['updated_subtype']} - {row['updated_subsubtype']}"
    ] = f"{row['updated_subtype']} - {row['updated_subsubtype']}"

app_ui = ui.page_fluid(
    ui.input_select(
        "alert_type",
        "Choose an alert type:",
        dropdown_options,
    ),
    ui.output_text("selected_alert"),
)
app_ui = ui.page_fluid(
    ui.input_select(
        "state",
        "Choose a state:",
        {
            "East Coast": {"NY": "New York", "NJ": "New Jersey", "CT": "Connecticut"},
            "West Coast": {"WA": "Washington", "OR": "Oregon", "CA": "California"},
            "Midwest": {"MN": "Minnesota", "WI": "Wisconsin", "IA": "Iowa"},
        },
    ),
    ui.output_text("value"),
)


def server(input, output, session):
    @render.text
    def value():
        return "You choose: " + str(input.input_select())


# Create the Shiny app
app = App(app_ui, server)
