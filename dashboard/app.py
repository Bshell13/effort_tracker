# Shiny imports
from shiny.express import input, ui
from shiny import reactive, render
from shinyswatch import theme
from shinywidgets import render_plotly

# Python imports
import pandas as pd
import random
import plotly.express as px
from scipy import stats
from pathlib import Path
import statistics as stat

from faicons import icon_svg


ui.page_opts(title="PLC+ Math Group 2: Effort Tracker", fillable=True)

with ui.sidebar():
    ui.input_checkbox_group(
        "teacher",
        "Teacher",
        {
            "shellenberger": "Shellenberger",
            "beckley": "Beckley",
            "kear": "Kear",
            "bergmann": "Bergmann",
            "shephard": "Shephard",
            "mcnaney": "McNaney",
            "kueser": "Kueser",
        },
        selected=[
            "shellenberger",
        ]
    )


# Fetching data

file = Path(__file__).parent / "effort_tracker.csv"
df = pd.read_csv(file)

# Adding a column for average of each record
df["avg_on_task"] = (1 - (
        df[["min_1", "min_2", "min_3", "min_4", "min_5"]].mean(axis=1)
        / df["total_students"])) * 100

# Box to show averages
with ui.value_box(
    showcase=icon_svg("sun"),
    theme="bg-gradient-blue-purple",
):

    "Averages"
    
    @render.text
    def display_stats():
        return f"{round(df['avg_on_task'].mean(),2)}"

    "Names"

    @render.text
    def names():
        return f"{input.teacher()}"

with ui.layout_columns():
    with ui.card():
        ui.card_header("Block")

        @render_plotly
        def block_plotly():
            plotly_block = px.bar(
                df,
                x=sorted(df["block"].unique()),
                y=df.groupby(["block"])["avg_on_task"].mean(),
            )
            plotly_block.update_layout(
                xaxis_title="Block", yaxis_title="Average Students on Task (%)"
            )
            return plotly_block

    with ui.card():
        ui.card_header("Task")

        @render_plotly
        def week_plotly():
            plotly_task = px.bar(
                df,
                x=sorted(df["task"].unique()),
                y=df.groupby(["task"])["avg_on_task"].mean(),
                color=filtered_data(),
            )
            plotly_task.update_layout(
                xaxis_title="Task", yaxis_title="Average Students on Task (%)"
            )
            return plotly_task

@reactive.calc
def filtered_data():
    return df[df["teacher"].isin(input.teacher())]
