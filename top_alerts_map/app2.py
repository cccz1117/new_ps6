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

data_path = "C:/Users/15535/OneDrive/文档/GitHub/ps6/top_alerts_map/df_alert_counts.csv"
df_alert_counts = pd.read_csv(data_path)
file_path = "C:/Users/15535/OneDrive/文档/GitHub/ps6/top_alerts_map/chicago-boundaries.geojson"
#----
with open(file_path) as f:
    chicago_geojson = json.load(f)
geo_data = alt.Data(values=chicago_geojson["features"])


# Define the Shiny app UI
dropdown_options = {
    f"{row['updated_type']} - {row['updated_subtype']} - {row['updated_subsubtype']}" : f"{row['updated_type']} - {row['updated_subtype']} - {row['updated_subsubtype']}"
    for _, row in df_alert_counts[["updated_type", "updated_subtype", "updated_subsubtype"]].drop_duplicates().iterrows()
}

# Define the Shiny app UI
app_ui = ui.page_fluid(
    ui.input_select(
        "alert_type",
        "Choose an alert type and subtype:",
        dropdown_options,
    ),
    ui.output_text("selected_alert"),
    ui.output_table("top_locations"),    
    output_widget("my_hist") 

)


def server(input, output, session):
    @reactive.calc
    @render.text
    def selected_alert():
        return f"You chose: {input.alert_type()}"

    @render.table
    def top_locations():
        # Parse the selected type and subtype
        selected = input.alert_type().split(" - ")
        if len(selected) == 3:
            selected_type, selected_subtype, selected_subsubtype = selected
            # Filter the data based on the selected type and subtype
            filtered_data = df_alert_counts[
                (df_alert_counts["updated_type"] == selected_type) &
                (df_alert_counts["updated_subtype"] == selected_subtype)&
                (df_alert_counts["updated_subsubtype"] == selected_subsubtype)
            ]
            # Get the top 10 locations by count
            top_locations = (
            filtered_data
            .sort_values(by="alert_count", ascending=False)
            .head(10)
)
            return top_locations
        return pd.DataFrame({"Message": ["No data for the selected alert type and subtype"]})

    @render_altair
    def my_hist():
        selected = input.alert_type().split(" - ")
        if len(selected) == 3:
            selected_type, selected_subtype, selected_subsubtype = selected
            # Filter the data based on the selected type and subtype
            filtered_data = df_alert_counts[
                (df_alert_counts["updated_type"] == selected_type) &
                (df_alert_counts["updated_subtype"] == selected_subtype)&
                (df_alert_counts["updated_subsubtype"] == selected_subsubtype)
            ]
            # Get the top 10 locations by count
            top_locations = (
                filtered_data
                .sort_values(by="alert_count", ascending=False)
                .head(10)
                )
            scatter_plot = (
                alt.Chart(top_locations)
                .mark_circle()
                .encode(
                x=alt.X("longitude_bin:Q", title="Longitude", scale=alt.Scale(domain=[-87.61, -87.80])),
                y=alt.Y("latitude_bin:Q", title="Latitude", scale=alt.Scale(domain=[41.86, 41.99])),
                color=alt.Color("alert_count:Q", title="Number of Alerts"),
                tooltip=["latitude_bin", "longitude_bin", "alert_count"],
                )
                .properties(
                title="Top 10 Latitude-Longitude Bins with Highest 'Jam - Heavy Traffic' Alerts",
                width=200,
                height=200,)) 
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
            ).properties(title=f"Top 10 locations with the highest counts of {input.alert_type()}")

            return combined_plot

        return pd.DataFrame({"Message": ["No data for the selected alert type and subtype"]})

    output.selected_alert = selected_alert
    output.top_locations = top_locations


app = App(app_ui, server)
