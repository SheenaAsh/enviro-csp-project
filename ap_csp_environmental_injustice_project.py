# -*- coding: utf-8 -*-
"""
AP CSP Environmental Injustice Project

Analyze the correlation between air pollution (PM2.5) and median income across counties.
"""

# Import necessary libraries
import pandas as pd
import geopandas as gpd
import folium
import matplotlib.pyplot as plt
import seaborn as sns
from folium.plugins import HeatMap, Fullscreen
from IPython.display import IFrame, display

# Load the datasets
pollution_data = pd.read_csv("nj_air_quality.csv")  # Must include: Region, PM2.5, Latitude, Longitude
income_data = pd.read_csv("income_levels.csv")  # Must include: Region, Median_Income
geo_data = gpd.read_file("regions_shapefile.shp")  # Must include: Region and geometry

# Preview datasets
print("Pollution Data:")
print(pollution_data.head())
print("Income Data:")
print(income_data.head())
print("Geo Data:")
print(geo_data.head())

# Clean column names
for df in [pollution_data, income_data, geo_data]:
    df.columns = df.columns.str.lower().str.strip()

# Clean and standardize 'county' values
pollution_data['county'] = pollution_data['county'].str.strip().str.lower()
income_data['county'] = income_data['county'].str.strip().str.lower()
geo_data['county'] = geo_data['county'].str.strip().str.lower()

# Merge pollution and income data on 'county'
pollution_income = pd.merge(pollution_data, income_data, on='county', how='inner')

# Merge with GeoDataFrame (adds geometry)
full_merged = geo_data.merge(pollution_income, on='county', how='inner')

# Rename columns for clarity
full_merged.rename(columns={"micrograms per cubic meter (pm2.5)(1)": "pollution_rate"}, inplace=True)

# Remove commas and convert 'median_income' to numeric
full_merged['median_income'] = full_merged['median_income'].str.replace(',', '').astype(float)

# Save merged data as GeoJSON for the interactive map
full_merged.to_file("merged_nj_pollution_income.geojson", driver="GeoJSON")
print("Merged data saved as GeoJSON.")

# Group data by county
county_grouped = full_merged.groupby('county').agg({
    'pollution_rate': 'mean',  # Average PM2.5 pollution levels
    'median_income': 'mean'   # Average median income per county
}).reset_index()

# Rename columns for clarity
county_grouped.rename(columns={'median_income': 'average_income'}, inplace=True)

# Debug: Check grouped data
print("County Grouped Data:")
print(county_grouped.head())

# Create scatterplot showing correlation between income and pollution presence
plt.figure(figsize=(10, 6))
sns.regplot(
    data=county_grouped,
    x='average_income',
    y='pollution_rate',
    scatter_kws={'s': 60},
    line_kws={'color': 'red'}
)
plt.title("Correlation Between County Income and Pollution Presence")
plt.xlabel("Average Median Income by County ($)")
plt.ylabel("Proportion of Sites with Pollution (PM2.5)")
plt.savefig("correlation_plot.png")
print("Correlation plot saved as 'correlation_plot.png'.")
plt.show()

# Interactive Choropleth Map
m = folium.Map(location=[40.0583, -74.4057], zoom_start=7)  # Central NJ coordinates

# Add the choropleth layer
choropleth = folium.Choropleth(
    geo_data="merged_nj_pollution_income.geojson",
    data=county_grouped,
    columns=["county", "pollution_rate"],  # Columns for county and pollution rate
    key_on="feature.properties.county",  # Match GeoJSON data
    fill_color="YlOrRd",  # Color scheme
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="PM2.5 Pollution Levels"
).add_to(m)

# Add tooltips
tooltip = folium.GeoJsonTooltip(
    fields=["county", "pollution_rate"],
    aliases=["County:", "PM2.5 Intensity:"],
    localize=True
)
choropleth.geojson.add_child(tooltip)

# Add fullscreen button
Fullscreen().add_to(m)

# Save and display the map
m.save("interactive_pollution_map.html")
print("Interactive map saved as 'interactive_pollution_map.html'.")
display(IFrame("interactive_pollution_map.html", width=700, height=500))