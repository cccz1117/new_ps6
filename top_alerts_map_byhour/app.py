from shiny import App, reactive, render, ui
import pandas as pd 
import pandas as pd
import altair as alt 
import pandas as pd
from datetime import date
import numpy as np
from shinywidgets import render_altair, output_widget

alt.data_transformers.disable_max_rows() 

import json

data_path = "C:/Users/15535/OneDrive/文档/GitHub/ps6/top_alerts_map_byhour/top_alerts_map_byhour.csv"
data = pd.read_csv(data_path)
file_path = "C:/Users/15535/OneDrive/文档/GitHub/ps6/top_alerts_map/chicago-boundaries.geojson"

with open(file_path) as f:
    chicago_geojson = json.load(f)
geo_data = alt.Data(values=chicago_geojson["features"])

data['hour_numeric'] = data['hour'].str.split(":").str[0].astype(int)
dropdown_options = {
    f"{row['updated_type']} - {row['updated_subtype']} - {row['updated_subsubtype']}" : f"{row['updated_type']} - {row['updated_subtype']} - {row['updated_subsubtype']}"
    for _, row in data[["updated_type", "updated_subtype", "updated_subsubtype"]].drop_duplicates().iterrows()
}
# Define the Shiny app UI
app_ui = ui.page_fluid(
    ui.panel_title("Top Alerts by Hour"),
    ui.input_select(
        "alert_type",
        "Choose an alert type and subtype:",
        dropdown_options,
    ),
    ui.input_slider("hour", "Select Hour of the Day:", min=0, max=23, value=12, step=1),
    output_widget("top_locations_table") )

def server(input, output, session):
    @reactive.calc
    @render_altair
    def top_locations_table():
         #Filter data based on the selected hour
        selected_hour = input.hour()
        selected = input.alert_type().split(" - ")
        selected_type, selected_subtype, selected_subsubtype = selected
        filtered_data = data[
                (data["updated_type"] == selected_type) &
                (data["updated_subtype"] == selected_subtype)&
                (data["updated_subsubtype"] == selected_subsubtype)&
                (data['hour_numeric'] == selected_hour)
            ]
        top_locations = (
            filtered_data
            .sort_values(by="alert_count", ascending=False)
            .head(10))
        points = alt.Chart(top_locations).mark_circle().encode(
            longitude=alt.X("longitude_bin:Q"), 
            latitude=alt.Y("latitude_bin:Q"),
            color=alt.Color("alert_count:Q", title="Number of Alerts").scale(scheme="darkred"),
            size=alt.value(70),
            tooltip=["latitude_bin", "longitude_bin", "alert_count"],
        )
        map_layer = (
            alt.Chart(geo_data).mark_geoshape(fill="lightgray", stroke="black")
            .properties(
                width=400,
                height=400
            )
            .project("identity", reflectY=True)  # Ensure correct alignment with coordinates
        )
        combined_plot = (
            map_layer + points
        ).properties(title=f"Top 10 locations with the highest counts when it is {input.hour()}:00")
        return combined_plot

    return pd.DataFrame({"Message": ["No data for the selected alert type and subtype"]})

        
    @render.table
    def my_hist():
        selected = input.hour()
        hr_alert_counts_by_selection = data[data['hour_numeric'] == selected]
        return hr_alert_counts_by_selection


# Create the Shiny app
app = App(app_ui, server)
