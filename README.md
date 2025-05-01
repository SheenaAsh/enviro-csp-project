# Environmental Injustice Analysis in New Jersey

This project investigates the relationship between air pollution and median income across counties in New Jersey. The analysis utilizes data on PM2.5 levels, median income, and geospatial information for visualization and statistical modeling.

## Data Sources
1. **Air Pollution Data**: PM2.5 levels per region (e.g., `nj_air_quality.csv`).
2. **Income Data**: Median income per region (e.g., `income_levels.csv`).
3. **Geospatial Data**: Shapefiles for mapping regions (e.g., `regions_shapefile.shp`).

## Project Goals
- Analyze whether there is a correlation between air pollution (PM2.5 levels) and income levels in New Jersey counties.
- Visualize the data using scatterplots and choropleth maps.

## Results
1. **Scatterplot Analysis**:
   - A scatterplot was created to investigate the relationship between median income and PM2.5 levels across counties.
   - The Pearson correlation coefficient analysis returned a **p-value of 0.8**, making the results statistically insignificant.
   - This means we cannot conclude that poorer counties in New Jersey experience significantly higher PM2.5 pollution levels.

2. **Future Work**:
   - Exploring other pollutants such as ozone levels might reveal statistically significant relationships.

## Choropleth Map
The project includes a choropleth map to visualize pollution levels across New Jersey counties.

### Map Features
- The map displays PM2.5 pollution levels by county.
- Includes tooltips showing county name and pollution intensity.
- Can be viewed interactively in the browser or within a Jupyter Notebook.

---

## Running the Analysis
To replicate the analysis and visualizations, follow these steps:

1. **Install Required Libraries**:
   ```bash
   pip install pandas geopandas matplotlib seaborn folium
   ```

2. **Run the Script**:
   Execute the Python script (`ap_csp_environmental_injustice_project.py`) in your environment to generate:
   - Scatterplots
   - Choropleth maps
   - Merged GeoJSON files for visualization

3. **Generated Outputs**:
   - `merged_nj_pollution_income.geojson`: Merged dataset with geospatial data.
   - `correlation_plot.png`: Scatterplot of median income vs. PM2.5 levels.
   - `interactive_pollution_map.html`: Interactive map of pollution levels.

---

## Future Directions
- Test other pollutants (e.g., ozone levels) to investigate potential correlations with income levels.
- Expand the dataset to include more socioeconomic factors (e.g., population density, healthcare access).
- Apply machine learning models to predict pollution levels based on demographic data.

---

### Author
- **Sheena Ash**  
- For questions or contributions, please feel free to open an issue or pull request.