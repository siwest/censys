import os
import re

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def run():

    target_directory = "event_analytics/data-dump"
    spacer = f"\n{'#'*79}\n"

    events_df = load_events(target_directory)
    clean_events_df = clean_data(events_df)

    frequency_events_emitted_by_device_df = (
        calculate_frequency_events_emitted_by_device(clean_events_df)
    )
    print_stats_to_console(frequency_events_emitted_by_device_df, spacer)

    frequency_device_events_by_event_type_df = (
        calculate_frequency_device_events_by_event_type(clean_events_df)
    )
    print_stats_to_console(frequency_device_events_by_event_type_df, spacer)

    summary_df = describe_by_event_type(frequency_events_emitted_by_device_df)
    print_stats_to_console(summary_df, spacer)
    write_data_to_file(summary_df, target_directory, "metadata")
    render_histogram_overall_event_types(frequency_events_emitted_by_device_df)
    render_histogram_of_squirrel_event_types(frequency_events_emitted_by_device_df)


def load_events(target_directory="data-dump"):
    """Load events from a target directory"""

    file_list = os.listdir(target_directory)

    files = [
        os.path.join(target_directory, file)
        for file in file_list
        if file.startswith("ev_dump_") and file.endswith(".csv")
    ]
    df_list = [pd.read_csv(file) for file in files]

    df = pd.concat(df_list)

    return df


def clean_data(df):
    """Clean pandas dataframe"""

    # Lowercase device_id and event_type
    # Assumption: use casefold to handle non-ascii characters
    df["event_type"] = df["event_type"].str.casefold()
    df["device_id"] = df["device_id"].str.casefold()

    # Coerce timestamp to datetime format, or null (NaT)
    df["time"] = pd.to_datetime(df["timestamp"], unit="s", errors="coerce")
    df["date"] = df["time"].dt.date

    # Remove rows with malformed `time` field
    df = df.loc[~df.time.isnull()]

    # Remove rows with malformed `event_type` field
    df = df[df["event_type"].str.match("^[a-z]*$")]

    # Remove rows with malformed `device_id` field
    df = df[df["device_id"].str.match("^[0-9a-fA-F]{8}$")]

    # Remove any other rows with NULL values
    df.dropna(inplace=True)

    df["event_type"] = df["event_type"].astype("category")
    df["device_id"] = df["device_id"].astype("category")

    return df


def calculate_frequency_events_emitted_by_device(df):
    count_events_df = df.copy(deep=True)

    count_events_df["count_event_payloads"] = count_events_df.groupby(
        ["device_id", "event_type"], sort=True
    )["event_type"].transform("count")

    count_events_df = (
        count_events_df[["device_id", "event_type", "count_event_payloads"]]
        .drop_duplicates(keep="first")
        .reset_index(drop=True)
        .sort_values("count_event_payloads", ascending=False)
    )

    return count_events_df


def calculate_frequency_device_events_by_event_type(df):
    count_devices_df = df.copy(deep=True)

    count_devices_df["count_payloads_sent_by_devices"] = count_devices_df.groupby(
        ["event_type"], sort=True
    )["device_id"].transform("count")
    count_devices_df[
        "count_distinct_devices_sending_event_type"
    ] = count_devices_df.groupby(["event_type"], sort=True)["device_id"].transform(
        "nunique"
    )

    count_devices_df = (
        count_devices_df[
            [
                "event_type",
                "count_payloads_sent_by_devices",
                "count_distinct_devices_sending_event_type",
            ]
        ]
        .drop_duplicates(keep="first")
        .reset_index(drop=True)
        .sort_values("count_payloads_sent_by_devices", ascending=False)
    )
    return count_devices_df


def describe_by_event_type(df):
    """Calculate summary statistics"""
    describe_events_df = (
        df.set_index("event_type")
        .select_dtypes(np.number)
        .stack()
        .groupby("event_type")
        .agg(["min", "max", "mean"])
    ).sort_index()

    return describe_events_df


def print_stats_to_console(df, spacer):
    """Print out human-readable stats to the console"""

    print(spacer)
    print(df.to_string())


def write_data_to_file(df, target_directory, filename):
    """Write pandas dataframe to file"""
    target_metadata_path = os.path.join(target_directory, filename)
    df.to_csv(target_metadata_path)


def render_histogram_overall_event_types(df):
    df.hist(by="event_type", figsize=(20, 8), xrot=30, alpha=0.5, bins=10)
    plt.show()


def render_histogram_of_squirrel_event_types(df):
    squirrel_count_events_df = df[df["event_type"] == "squirrel"]

    squirrel_count_events_df.hist(figsize=(20, 8), xrot=30, alpha=0.5, bins=10)
    plt.title("Histogram of Squirrel Events")
    plt.xlabel("Event Frequency")
    plt.ylabel("Number of Devices")
    plt.show()


run()
