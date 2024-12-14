import os
import tarfile
import geopandas as gpd
import json

# Directory containing the downloaded .tar files
TAR_DIR = "data"
EXTRACT_DIR = "shapefiles"  # Directory to store extracted shapefiles
OUTPUT_JSON = "ice_data.json"

# Create the extraction directory if it doesn't exist
os.makedirs(EXTRACT_DIR, exist_ok=True)

def extract_tar_files(tar_dir, extract_dir):
    """Extract all .tar files in the specified directory."""
    for file in os.listdir(tar_dir):
        if file.endswith(".tar"):
            tar_path = os.path.join(tar_dir, file)
            print(f"Extracting: {tar_path}")
            with tarfile.open(tar_path, "r") as tar:
                tar.extractall(path=extract_dir)

def reproject_and_calculate_area(gdf):
    """Reproject GeoDataFrame to a projected CRS and calculate total area."""
    if gdf.crs.is_geographic:  # Check if CRS is geographic (e.g., WGS84)
        print(f"Reprojecting from geographic CRS: {gdf.crs}")
        gdf = gdf.to_crs("EPSG:3978")  # Canada Lambert Conformal Conic
    
    # Calculate total area in square meters
    total_area = gdf['geometry'].area.sum()
    return total_area

def process_shapefiles(shapefile_dir):
    """Process shapefiles to extract ice concentration data."""
    data_summary = []

    for root, dirs, files in os.walk(shapefile_dir):
        for file in files:
            if file.endswith(".shp"):
                filepath = os.path.join(root, file)
                print(f"Processing file: {filepath}")

                # Load the shapefile
                gdf = gpd.read_file(filepath)

                # Extract date from filename (assuming 'YYYYMMDD' in name)
                date = file.split("_")[2]

                # Filter for relevant columns
                if 'CT' in gdf.columns:
                    gdf['CT'] = gdf['CT'].astype(float)  # Ensure concentration is numeric

                    # Calculate average ice concentration and total area
                    avg_concentration = gdf['CT'].mean()
                    total_area = reproject_and_calculate_area(gdf)

                    # Append results to summary
                    data_summary.append({
                        "date": date,
                        "average_ice_concentration": avg_concentration,
                        "total_area": total_area
                    })
                else:
                    print(f"File {file} does not contain 'CT' attribute.")

    return data_summary

def save_to_json(data, output_path):
    """Save processed data to a JSON file."""
    with open(output_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data saved to {output_path}")

# Main processing
if __name__ == "__main__":
    print("Extracting .tar files...")
    extract_tar_files(TAR_DIR, EXTRACT_DIR)

    print("Processing shapefiles...")
    ice_data = process_shapefiles(EXTRACT_DIR)
    
    save_to_json(ice_data, OUTPUT_JSON)