import json
import matplotlib.pyplot as plt
from datetime import datetime

# Input JSON data
INPUT_FILE = "ice_data.json"
OUTPUT_FILE = "ice_chart.png"

def process_data(input_file):
    """Load and process JSON data."""
    with open(input_file, 'r') as file:
        data = json.load(file)
    
    # Convert to time series
    processed_data = []
    for entry in data:
        date = entry['date'][:8]  # Extract YYYYMMDD
        date_obj = datetime.strptime(date, "%Y%m%d")
        processed_data.append({
            "date": date_obj,
            "average_ice_concentration": entry["average_ice_concentration"],
            "total_area": entry["total_area"] / 1e12  # Convert to trillions of square meters for readability
        })
    
    # Sort by date
    processed_data.sort(key=lambda x: x["date"])
    return processed_data

def generate_chart(data, output_file):
    """Generate a time series chart for ice concentration and area."""
    # Extract data
    dates = [entry["date"] for entry in data]
    concentrations = [entry["average_ice_concentration"] for entry in data]
    total_areas = [entry["total_area"] for entry in data]
    
    # Calculate dynamic y-axis limits for concentration
    min_concentration = min(concentrations)
    max_concentration = max(concentrations)
    concentration_padding = (max_concentration - min_concentration) * 0.05  # 5% padding
    
    # Calculate dynamic y-axis limits for total area
    min_area = min(total_areas)
    max_area = max(total_areas)
    area_padding = (max_area - min_area) * 0.25  # % padding
    
    # Create figure and axes
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # Plot average ice concentration (left y-axis)
    ax1.plot(dates, concentrations, 'b-', label='Average Ice Concentration (%)')
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Average Ice Concentration (%)", color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    ax1.set_ylim(min_concentration - concentration_padding, max_concentration + concentration_padding)
    
    # Plot total area (right y-axis)
    ax2 = ax1.twinx()
    ax2.plot(dates, total_areas, 'r-', label='Total Ice Area (Trillion m²)')
    ax2.set_ylabel("Total Ice Area (Trillion m²)", color='r')
    ax2.tick_params(axis='y', labelcolor='r')
    ax2.set_ylim(min_area - area_padding, max_area + area_padding)
    
    # Add title and grid
    plt.title("Arctic Ice: Average Concentration and Total Area Over Time", fontsize=14)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    
    # Save the chart
    fig.tight_layout()
    plt.savefig(output_file)
    print(f"Chart saved as {output_file}")
    plt.show()

# Main script
if __name__ == "__main__":
    # Process data and generate chart
    ice_data = process_data(INPUT_FILE)
    generate_chart(ice_data, OUTPUT_FILE)