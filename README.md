# Christmas Ice Project

## Overview
For a Mean, Median and Moose podcast segment, this project analyzes sea ice extent in the Eastern Arctic during December. This analysis provides estimates of future Arctic ice loss based on historical data using regression models but does not account for physical climate processes like ocean currents, feedback loops, or emissions scenarios, which are included in more sophisticated climate models.

## Data Source
Data is sourced from the National Snow and Ice Data Center
- [NSIDC Sea Ice Data](https://nsidc.org/data/g02171/versions/1)
- Canadian Ice Service sea ice charts in SIGRID-3 format (https://noaadata.apps.nsidc.org/NOAA/G02171/Eastern_Arctic/) 

## Objectives
- Analyze historical sea ice extent data
- Visualize trends and patterns
- Provide insights into changes in sea ice extent

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/christmas-ice.git
    cd christmas-ice
    ```

2. Build the Docker container:
    ```sh
    docker build -t christmas-ice .
    ```

3. Run the Docker container:
    ```sh
    docker run -it --rm christmas-ice
    ```

## Usage

Steps to run the analysis and visualize the results.

1. Run `get_data.py` to download the necessary sea ice data.
2. Execute `process_data.py` to clean and preprocess the downloaded data.
3. Use `plot_data.py` to generate visualizations of the processed data.
4. Finally, run `project_sea_ice.py` to project future sea ice extent based on the analysis.


