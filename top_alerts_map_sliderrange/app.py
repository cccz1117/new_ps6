from shiny import App, reactive, render, ui
import pandas as pd 
import pandas as pd
import altair as alt 
import pandas as pd
from datetime import date
import numpy as np
from shinywidgets import render_altair, output_widget

# Print the current working directory
alt.data_transformers.disable_max_rows() 

import json

data_path = "./df_alert_hr_counts.csv"

data = pd.read_csv(data_path)
file_path = "../top_alerts_map/chicago-boundaries.geojson"
with open(file_path) as f:
    chicago_geojson = json.load(f)
geo_data = alt.Data(values=chicago_geojson["features"])

data['hour_numeric'] = data['hour'].str.split(":").str[0].astype(int)
dropdown_options = {
    f"{row['updated_type']} - {row['updated_subtype']} - {row['updated_subsubtype']}" : f"{row['updated_type']} - {row['updated_subtype']} - {row['updated_subsubtype']}"
    for _, row in data[["updated_type", "updated_subtype", "updated_subsubtype"]].drop_duplicates().iterrows()
}
app_ui = ui.page_fluid(
    ui.panel_title("Top Alerts by Hour"),
    ui.input_select(
        "alert_type",
        "Choose an alert type and subtype:",
        dropdown_options,
    ),
    ui.input_switch("range_switch", "Toggle to switch to range of hours", True),
    ui.panel_conditional(
        "!input.range_switch", 
        ui.input_slider("hour_range", "Slider", min=0, max=23, value=[10, 14]),
        output_widget("my_hist_range")
    ),
    ui.panel_conditional(
        "input.range_switch", 
        ui.input_slider("hour", "Select Hour of the Day:", min=0, max=23, value=12, step=1),
        output_widget("my_hist_single")
    )

    #output_widget("top_locations_table") 
    )
#ui.input_slider("slider", "Slider", min=0, max=100, value=[35, 65])  
def server(input, output, session):
    @render_altair
    def my_hist_single():
        selected = input.alert_type().split(" - ")
        selected_type, selected_subtype, selected_subsubtype = selected
        selected_hour = input.hour()
            # Filter the data based on the selected type and subtype
        filtered_data = data[
                (data["updated_type"] == selected_type) &
                (data["updated_subtype"] == selected_subtype)&
                (data["updated_subsubtype"] == selected_subsubtype)&
                (data['hour_numeric'] == selected_hour)
            ]
        points = alt.Chart(filtered_data.head(10)).mark_circle().encode(
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
        ).properties(title="Top 10")

        return combined_plot
    @render_altair
    def my_hist_range():
        selected = input.alert_type().split(" - ")
        selected_type, selected_subtype, selected_subsubtype = selected
        start_hour, end_hour = input.hour_range()
            # Filter the data based on the selected type and subtype
        filtered_data = data[
                (data["updated_type"] == selected_type) &
                (data["updated_subtype"] == selected_subtype)&
                (data["updated_subsubtype"] == selected_subsubtype)&
                (data['hour_numeric'] >= start_hour)&
                (data['hour_numeric'] <= end_hour)
            ]
        points = alt.Chart(filtered_data.head(10)).mark_circle().encode(
            longitude=alt.X("longitude_bin:Q"), 
            latitude=alt.Y("latitude_bin:Q"),
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
        ).properties(title="Top 10")

        return combined_plot
    @render.text
    def value():
        return f"{input.alert_type()}"
    @render.text
    def value2():
        start_hour, end_hour = input.hour_range()
        return start_hour


app = App(app_ui, server)
