import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

# Paths to the dataset and map image
path_to_Dataset = r"D:\STUDIES\DATA SCIENCE VIDEOS\PROGRAMMING FOR DATA\Assign Py\Python 2 Assignment\GrowLocations.csv"
map_image_path = r"D:\STUDIES\DATA SCIENCE VIDEOS\PROGRAMMING FOR DATA\Assign Py\Python 2 Assignment\map7.png"

# The bounding box for the map
longitude_min = -10.592
longitude_max = 1.6848
latitude_min = 50.681
latitude_max = 57.985

# This checks if the map image exists in the specified location path
if not os.path.isfile(map_image_path):
    raise FileNotFoundError(f"The map image file was not found: {map_image_path}")

# Loading the dataset into a DataFrame
df = pd.read_csv(path_to_Dataset)

# The function to clean the dataset
def clean_dataset(df):
    # Verifying column names
    expected_columns = ['Serial', 'Latitude', 'Longitude', 'Type', 'SensorType', 'Code', 'BeginTime', 'EndTime']
    if not all(col in df.columns for col in expected_columns):
        print("Warning: The dataset does not contain the expected columns.")
    
    # Swaping the Latitude and Longitude columns due to column mislabeling in the dataset
    df['Latitude'], df['Longitude'] = df['Longitude'], df['Latitude']
    
    # Ensuring that Latitude and Longitude are numeric and handle any errors
    df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
    df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')

    # Remove rows that have invalid latitude or longitude
    df_cleaned = df[
        (df['Longitude'] >= longitude_min) & (df['Longitude'] <= longitude_max) &
        (df['Latitude'] >= latitude_min) & (df['Latitude'] <= latitude_max)
    ]
    
    # Summary of the rows before and after cleaning process
    print(f"Rows before cleaning: {df.shape[0]}")
    print(f"Rows after cleaning: {df_cleaned.shape[0]}")
    print(f"Rows removed: {df.shape[0] - df_cleaned.shape[0]}")

    return df_cleaned

# Cleaning the dataset
df_cleaned = clean_dataset(df)

# Printing the first 5 rows of the cleaned data
print("\nCleaned Data (First 5 rows):")
print(df_cleaned[['Latitude', 'Longitude']].head())

# Loading the map image
img = mpimg.imread(map_image_path)

# Plotting the map and points
fig, ax = plt.subplots(figsize=(10, 10))

# Displaying the map image
ax.imshow(img, extent=[longitude_min, longitude_max, latitude_min, latitude_max])

# Ploting the cleaned points on the map
ax.scatter(df_cleaned['Longitude'], df_cleaned['Latitude'], color='red', s=30, alpha=0.5, label='Sensor Locations')

# Adding title and labels
plt.title('Ploting Sensor Locations on the UK Map')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.xlim(longitude_min, longitude_max)
plt.ylim(latitude_min, latitude_max)
plt.legend()
plt.grid(True)

# Show the plot
plt.show()

# References:
# 1.For cleaning dataset with pandas : https://www.analyticsvidhya.com/blog/2024/05/automate-data-cleaning-in-python/
# 2. For cleaning data with pandas: https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html
# 3. For plotting with matplotlib: https://matplotlib.org/stable/tutorials/introductory/pyplot.html
# 4.For ploting with matplotlib :  https://geopandas.org/en/latest/gallery/matplotlib_scalebar.html

