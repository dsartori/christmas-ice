import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from ftplib import FTP

def download_file_ftp(ftp_url, ftp_file, local_file):
    """Download a file from an FTP server."""
    print(f"Connecting to FTP: {ftp_url}")
    ftp = FTP(ftp_url)
    ftp.login()  # Anonymous login
    
    print(f"Downloading file: {ftp_file}")
    with open(local_file, 'wb') as f:
        ftp.retrbinary(f"RETR {ftp_file}", f.write)
    
    ftp.quit()
    print(f"File saved as: {local_file}")

def process_data(file_path):
    """Process the December sea ice data."""
    # Read the CSV file and skip unnecessary rows
    data = pd.read_csv(file_path, skiprows=0)  # No additional rows to skip
    
    # Debugging step to inspect raw columns and data
    print(f"Original columns: {data.columns.tolist()}")
    print(data.head())
    
    # Clean and rename columns
    data.columns = ["Year", "Month", "Data_Type", "Region", "Extent", "Area"]
    
    # Remove any non-numeric rows
    data = data[pd.to_numeric(data["Year"], errors="coerce").notna()]
    
    # Convert columns to appropriate data types
    data["Year"] = data["Year"].astype(int)
    data["Month"] = data["Month"].astype(int)
    data["Extent"] = data["Extent"].astype(float)
    
    # Filter for December only (Month = 12)
    data = data[data["Month"] == 12]
    
    # Keep only Year and Extent for further analysis
    data = data[["Year", "Extent"]]
    
    return data

def generate_projections(data, future_years=30, degree=2):
    """Generate projections for December sea ice extent."""
    years = data["Year"].values.reshape(-1, 1)
    extent = data["Extent"].values

    # Extend years into the future
    last_year = years[-1][0]
    future = np.arange(last_year + 1, last_year + future_years + 1).reshape(-1, 1)
    all_years = np.vstack((years, future))
    
    # Linear Regression
    lin_reg = LinearRegression()
    lin_reg.fit(years, extent)
    linear_projection = lin_reg.predict(all_years)
    
    # Polynomial Regression
    poly = PolynomialFeatures(degree=degree)
    years_poly = poly.fit_transform(years)
    all_years_poly = poly.fit_transform(all_years)
    poly_reg = LinearRegression()
    poly_reg.fit(years_poly, extent)
    polynomial_projection = poly_reg.predict(all_years_poly)
    
    return all_years, linear_projection, polynomial_projection

def plot_projections(data, projections, outliers, future_years):
    """Plot historical data, outliers (as indicators), and projections."""
    years = data["Year"]
    extent = data["Extent"]
    all_years, linear_proj, poly_proj = projections

    plt.figure(figsize=(12, 6))

    # Plot historical data
    plt.plot(years, extent, 'b.', label='Observed Sea Ice Extent (Million km²)')

    # Plot projections
    plt.plot(all_years, linear_proj, 'r--', label='Linear Projection')
    plt.plot(all_years, poly_proj, 'r-', label=f'Polynomial Projection (Degree 2)')

    # Adjust y-scale to ignore outliers
    ymin = data["Extent"].min() - 1  # Add padding to the lower bound
    ymax = data["Extent"].max() + 1  # Add padding to the upper bound
    plt.ylim(ymin, ymax)

    # Plot outliers as indicators at the bottom of the y-axis range
    if not outliers.empty:
        plt.scatter(outliers["Year"], [ymin] * len(outliers), color='red', marker='v', 
                    label='Outliers (Indicator)', zorder=5)

    # Customize plot
    plt.xlabel("Year")
    plt.ylabel("Sea Ice Extent (Million km²)")
    plt.title(f"December Arctic Sea Ice Extent: Historical Data and {future_years}-Year Projections")
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.savefig("december_sea_ice_projections_with_outliers.png")
    print("Projection chart saved as december_sea_ice_projections_with_outliers.png")
    plt.show()

def detect_outliers(data):
    """Detect outliers in the Extent column using IQR."""
    q1 = data["Extent"].quantile(0.25)  # 25th percentile
    q3 = data["Extent"].quantile(0.75)  # 75th percentile
    iqr = q3 - q1  # Interquartile range
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    # Identify outliers
    outliers = data[(data["Extent"] < lower_bound) | (data["Extent"] > upper_bound)]
    print(f"Outliers detected:\n{outliers}")
    return outliers, lower_bound, upper_bound

def main():
    # FTP settings
    ftp_url = "sidads.colorado.edu"
    ftp_file = "DATASETS/NOAA/G02135/north/monthly/data/N_12_extent_v3.0.csv"
    local_file = "N_12_extent_v3.0.csv"
    
    # Step 1: Download the file
    print("Downloading December sea ice data...")
    download_file_ftp(ftp_url, ftp_file, local_file)
    
    # Step 2: Process the data
    print("Processing data...")
    data = process_data(local_file)
    
    # Detect and remove outliers
    outliers, lower_bound, upper_bound = detect_outliers(data)
    data = data[(data["Extent"] >= lower_bound) & (data["Extent"] <= upper_bound)]

    # Step 3: Generate projections
    print("Generating projections...")
    future_years = 30
    projections = generate_projections(data, future_years=future_years, degree=2)
    
    # Step 4: Plot projections
    print("Plotting projections...")
    plot_projections(data, projections, outliers, future_years)

# Run the script
if __name__ == "__main__":
    main()