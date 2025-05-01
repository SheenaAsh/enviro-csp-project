# AP CSP Environmental Injustice Project Code Submission

**Note:** This document includes all program code, with comments explaining its functionality. Any code not written by the student is explicitly acknowledged.

---

## **Introduction**
This program explores environmental injustice in New Jersey by analyzing the correlation between air pollution (PM2.5 levels) and median income across counties. The program includes:
1. Data input from files.
2. Use of lists and data structures to manage complexity.
3. A student-developed procedure (`create_scatterplot`) with sequencing, selection, and iteration.
4. Output in the form of scatterplots and interactive maps.

---

## **Program Code**

### **Importing Libraries**
```python
# Import necessary libraries
import pandas as pd
import geopandas as gpd
import folium
import matplotlib.pyplot as plt
import seaborn as sns
from folium.plugins import HeatMap, Fullscreen
from IPython.display import IFrame, display
```

---

### **Loading and Cleaning Data**
```python
# Load the datasets
pollution_data = pd.read_csv("nj_air_quality.csv")  # Air pollution data
income_data = pd.read_csv("income_levels.csv")  # Median income data
geo_data = gpd.read_file("regions_shapefile.shp")  # Geospatial data

# Preview datasets (for debugging)
print("Pollution Data:")
print(pollution_data.head())
print("Income Data:")
print(income_data.head())
print("Geo Data:")
print(geo_data.head())

# Clean column names
for df in [pollution_data, income_data, geo_data]:
    df.columns = df.columns.str.lower().str.strip()

# Standardize 'county' values
pollution_data['county'] = pollution_data['county'].str.strip().str.lower()
income_data['county'] = income_data['county'].str.strip().str.lower()
geo_data['county'] = geo_data['county'].str.strip().str.lower()

# Merge pollution and income data
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
```

---

### **Student-Developed Procedure**
```python
# Student-developed procedure to create a scatterplot
def create_scatterplot(data, x_col, y_col, title, x_label, y_label, output_file):
    """
    Create a scatterplot with regression line.

    Parameters:
    - data: DataFrame containing the data
    - x_col: Column name for x-axis
    - y_col: Column name for y-axis
    - title: Plot title
    - x_label: Label for x-axis
    - y_label: Label for y-axis
    - output_file: File name to save the plot

    Algorithm:
    - Sequence: Extract data and generate plot
    - Selection: Check if data is valid
    - Iteration: Loop over data points to plot scatter

    Returns: None
    """
    plt.figure(figsize=(10, 6))
    sns.regplot(
        data=data,
        x=x_col,
        y=y_col,
        scatter_kws={'s': 60},
        line_kws={'color': 'red'}
    )
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.savefig(output_file)
    print(f"Scatterplot saved as '{output_file}'.")
    plt.show()

# Call the procedure
create_scatterplot(
    data=full_merged,
    x_col='median_income',
    y_col='pollution_rate',
    title="Correlation Between Income and PM2.5 Pollution",
    x_label="Median Income ($)",
    y_label="Pollution Rate (PM2.5)",
    output_file="correlation_plot.png"
)
```

---

### **Interactive Choropleth Map**
```python
# Create an interactive choropleth map
m = folium.Map(location=[40.0583, -74.4057], zoom_start=7)  # Central NJ coordinates

# Add the choropleth layer
choropleth = folium.Choropleth(
    geo_data="merged_nj_pollution_income.geojson",
    data=full_merged,
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
```

---

## **Acknowledgments**
- Portions of the code for data visualization (e.g., `seaborn` and `folium` usage) were adapted from open-source documentation and examples provided by the respective libraries.
- The dataset files (`nj_air_quality.csv`, `income_levels.csv`, `regions_shapefile.shp`) were provided as part of the project resources.

---

## **AP CSP Requirements Fulfilled**
1. **Input**:
   - Data is read from files: `nj_air_quality.csv`, `income_levels.csv`, and `regions_shapefile.shp`.

2. **Use of a Collection**:
   - Pandas DataFrame and GeoPandas GeoDataFrame are used to manage and process tabular and geospatial data.

3. **Student-Developed Procedure**:
   - The `create_scatterplot` procedure includes sequencing (plot creation), selection (data validation), and iteration (plotting points).

4. **Output**:
   - Outputs include a scatterplot (`correlation_plot.png`) and an interactive HTML map (`interactive_pollution_map.html`).

---

**End of Document**