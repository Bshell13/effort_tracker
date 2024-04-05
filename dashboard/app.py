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

ui.page_opts(title="PLC+ Math Group 2: Effort Tracker", fillable=True)

# -------------------------------
# Sidebar
# Heading
# Intputs
# "Block"
# "Teacher Name"
# "Week Number"
# "Minute Number"
# Links
# Data
# -------------------------------



# -------------------------------
# Gathering Data
# First use the random data
# Either use a google form or just manually enter data
# Needs to be in CSV
# Fetch data and input as a DataFrame (pandas)
# -------------------------------

@reactive.calc
def get_data():
    file = Path(__file__).parent / "effort_tracker.csv"
    return pd.read_csv(file)

with ui.navset_card_underline():

    with ui.nav_panel("Data frame"):
        @render.data_frame
        def frame():
            # Give dat() to render.DataGrid to customize the grid
            return get_data()

    with ui.nav_panel("Table"):
        @render.table
        def table():
            return get_data()


# -------------------------------
# Outputs
# Valuebox
# Average Percent on-task
# Card
# Data Table
# Plot: Percent off task vs min
# Plot: Percent off task vs week
# Plot: Percent off task vs block
# -------------------------------



with ui.navset_pill(id="tab"):
    with ui.nav_panel("Block"):
        with ui.sidebar(open="open"):
            ui.input_checkbox_group("block", "Block",
                {
                    "b1": "Blue 1",
                    "b2": "Blue 2",
                    "b3": "Blue 3",
                    "b5": "Blue 5",
                    "w1": "White 1",
                    "w2": "White 2",
                    "w3": "White 3",
                    "w5": "White 5",
                },
            )

    with ui.nav_panel("Week"):
        with ui.sidebar(open="open"):
            ui.input_checkbox_group("week", "Week Number",
                {
                    "1": "Week 1",
                    "2": "Week 2",
                    "3": "Week 3",
                    "4": "Week 4",
                    "5": "Week 5",
                }
            )


    with ui.nav_panel("task"):
        with ui.sidebar(open="open"):
            ui.input_checkbox_group("task", "Type of Task",
                {
                    "solving_equations": "Solving Equations",
                    "four_fours": "Four Four's",
                    "open_middle": "Open Middle Math",
                    "rebus_puzzles": "Rebus Puzzles",
                    "logic_puzzles": "Logic Puzzles",
                }
            )
