import streamlit as st
import pandas as pd
import os

# Load the Data
file_path = os.path.join(r"C:\Users\JOE\Pictures\Camera Roll", "combined_output.csv")
df1 = pd.read_csv(file_path)

# Clean the 'Ratings' column: Convert to numeric and handle non-numeric values
df1['Ratings'] = pd.to_numeric(df1['Ratings'], errors='coerce')

# Drop rows with NaN values in 'Ratings' column
df1 = df1.dropna(subset=['Ratings'])

# Convert Start_time and End_time to datetime format
df1['Start_time'] = pd.to_datetime(df1['Start_time'], format='%H:%M', errors='coerce').dt.time
df1['End_time'] = pd.to_datetime(df1['End_time'], format='%H:%M', errors='coerce').dt.time

# Streamlit App Title
st.title("Redbus Bus Data - Comparison and Filtering App")

# Show the entire dataframe
st.write("### Bus Routes Data")
st.dataframe(df1)

# Filtering options
st.sidebar.header("Filter Options")

# Select Route Names
routes = st.sidebar.multiselect('Select Route Name', options=df1['Route_name'].unique())

# Select Bus Types
bus_types = st.sidebar.multiselect('Select Bus Type', options=df1['Bus_type'].unique())

# Filter by Ratings (1.0 to 5.0)
rating_range = st.sidebar.slider('Select Rating Range', min_value=1.0, max_value=5.0, step=0.1, value=(1.0, 5.0))

# Filter by Start Time
start_time = st.sidebar.time_input('Select Start Time', value=None)

# Filter by End Time
end_time = st.sidebar.time_input('Select End Time', value=None)

# Filter DataFrame based on the sidebar inputs
filtered_df = df1.copy()

# Apply filters
if routes:
    filtered_df = filtered_df[filtered_df['Route_name'].isin(routes)]

if bus_types:
    filtered_df = filtered_df[filtered_df['Bus_type'].isin(bus_types)]

if start_time:
    filtered_df = filtered_df[filtered_df['Start_time'] >= start_time]

if end_time:
    filtered_df = filtered_df[filtered_df['End_time'] <= end_time]

filtered_df = filtered_df[
    (filtered_df['Ratings'] >= rating_range[0]) & (filtered_df['Ratings'] <= rating_range[1])
]

# Display filtered dataframe
st.write("### Filtered Results")
st.write(f"Showing {len(filtered_df)} results")
st.dataframe(filtered_df)

# Display specific details of a selected route
if not filtered_df.empty:
    st.write("### Detailed View of Bus Information")

    selected_route = st.selectbox('Select a Bus to View Details', options=filtered_df['Bus_name'])

    if selected_route:
        bus_details = filtered_df[filtered_df['Bus_name'] == selected_route]
        st.write(f"#### Bus Details for: {selected_route}")
        st.write(f"Bus Type: {bus_details['Bus_type'].values[0]}")
        st.write(f"Start Time: {bus_details['Start_time'].values[0]}")
        st.write(f"End Time: {bus_details['End_time'].values[0]}")
        st.write(f"Duration: {bus_details['Total_duration'].values[0]}")
        st.write(f"Price: {bus_details['Price'].values[0]}")
        st.write(f"Seats Available: {bus_details['Seats_Available'].values[0]}")
        st.write(f"Ratings: {bus_details['Ratings'].values[0]}")
