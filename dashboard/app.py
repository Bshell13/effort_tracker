# Shiny imports
from shiny.express import input, ui
from shiny import reactive, render
from shinyswatch import theme
from shinywidgets import render_plotly

# Python imports
import pandas as pd
import plotly.express as px
from pathlib import Path

from faicons import icon_svg

ui.page_opts(title="PLC+ Math Group 2: Effort Tracker", fillable=True)

with ui.sidebar(open='closed'):
    ui.input_checkbox_group(
        "teacher",
        "Teacher",
        {
            "beckley": "Beckley",
            "bergmann": "Bergmann",
            "kear": "Kear",
            "kueser": "Kueser",
            "mcnaney": "McNaney",
            "shellenberger": "Shellenberger",
            "shephard": "Shephard",
        },
        selected=[
            "beckley",
            "bergmann",
            'kear',
            'kueser',
            'mcnaney',
            'shellenberger',
            'shephard',
        ]
    )


# Fetching data

file = Path(__file__).parent / "effort_tracker.csv"
df = pd.read_csv(file)

# Adding a column for average of each record
df["avg_on_task"] = (1 - (
        df[["min_1", "min_2", "min_3", "min_4", "min_5"]].mean(axis=1)
        / df["total_students"])) * 100



with ui.layout_columns():
    with ui.value_box(
        showcase=icon_svg("school"),
        theme="bg-blue",
    ):
    
        "Average Percent of Students On-Task"
        # Average Number of Students recoreded On-Task.
        @render.text
        def display_stats():
            data_teacher = filtered_data_teacher()
            return f"{round(data_teacher['avg_on_task'].mean(),2)} %"
    
        "Average Total Number of Students Per Class"
        # Average Number of Students recoreded during implementation.
        @render.text
        def names():
            data_teacher = filtered_data_teacher()
            return f"{round(data_teacher['total_students'].mean(), 0)}"

    with ui.card():
        ui.card_header("Week")

        # Render bar plot of percent on task students per week
        @render_plotly
        def week_plotly():
            filtered = filtered_data_teacher()
            plotly_week = px.line(
                filtered,
                x=sorted(df["week_num"].unique()),
                y=filtered.groupby(["week_num"])['avg_on_task'].mean()
            )
            plotly_week.update_layout(
                xaxis_title="Week",
                yaxis_title="Average Students on Task (%)"
            )
            plotly_week.update_traces(
                marker_color='dodgerblue'
            )
            return plotly_week

with ui.layout_columns():
    with ui.navset_card_tab():
        with ui.nav_panel("Block"):
            # Render bar plot of percent on task students per block
            @render_plotly
            def block_plotly():
                filtered = filtered_data_teacher()
                plotly_block = px.bar(
                    filtered,
                    x=sorted(filtered["block"].unique()),
                    y=filtered.groupby(["block"])["avg_on_task"].mean(),
                )
                plotly_block.update_layout(
                    xaxis_title="Block",
                    yaxis_title="Average Students on Task (%)"
                )
                plotly_block.update_traces(
                    marker_color='dodgerblue'
                )
                return plotly_block

        with ui.nav_panel("Course"):
            # Render bar plot of percent on task students per block
            @render_plotly
            def course_plotly():
                filtered = filtered_data_teacher()
                plotly_course = px.bar(
                    filtered,
                    x=sorted(filtered["name_of_class"].unique()),
                    y=filtered.groupby(["name_of_class"])["avg_on_task"].mean(),
                )
                plotly_course.update_layout(
                    xaxis_title="Course",
                    yaxis_title="Average Students on Task (%)"
                )
                plotly_course.update_traces(
                    marker_color='dodgerblue'
                )
                return plotly_course

    with ui.card():
        ui.card_header("Task")

        # Render bar plot of percent on task students per task
        @render_plotly
        def task_plotly():
            filtered = filtered_data_teacher()
            plotly_task = px.bar(
                filtered,
                x=sorted(df["task"].unique()),
                y=filtered.groupby(["task"])["avg_on_task"].mean(),
            )
            plotly_task.update_layout(
                xaxis_title="Task",
                yaxis_title="Average Students on Task (%)"
            )
            plotly_task.update_traces(
                marker_color='dodgerblue'
            )
            return plotly_task



@reactive.calc
def filtered_data_teacher():
    return df[df["teacher"].isin(input.teacher())]
