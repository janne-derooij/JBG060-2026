import pandas as pd
import netCDF4 as nc
import xarray as xr
import io
import numpy as np
from pathlib import Path
import json
import rasterio 
from rasterio.windows import from_bounds
from affine import Affine


#### NOTE: FIRST DOWNLOAD THE RAW DATA FROM SURFDRIVE

def load_worldpop_coordinate(longitude : float, latitude : float) -> dict[int, pd.DataFrame]:
    """
    Constrained estimates of the total number of people per grid square at a resolution of 3 arc (approximately 100m at the equator) R2025A version v1.  
    Unit: number of people per pixel. 
    
    This function extracts the population count at the given coordinate, at each year between 2015-2025.

    Notice that due to the small spatial grid size of this data, lots of grid locations will not have people.
    
    """
    years = np.arange(2015, 2026)
    data_dir = './raw_data/worldpop'

    pop_data = {}
    for year in years:
        fname = data_dir + f"/ssd_pop_{year}_CN_100m_R2025A_v1.tif"

        with rasterio.open(fname) as src:
            bounds = src.bounds  
            ## Check if the provided coordinates are within South Sudan       
            if not (bounds.left <= longitude <= bounds.right and
                    bounds.bottom <= latitude <= bounds.top):
                print(f"  WARNING: ({longitude}, {latitude}) is outside raster bounds {bounds}")
                return np.nan

            # Convert lon/lat to (row, col) using the inverse affine transform
            row, col = src.index(longitude, latitude)   # src.index takes (x, y) = (lon, lat)
            value = src.read(1)[row, col]

            if src.nodata is not None and value == src.nodata:
                pop_year = np.nan
            else:
                pop_year = value

        pop_data[year] = pop_year

    return pop_data

            
    
def load_worldpop_area(bbox : dict) -> dict[int, pd.DataFrame]:
    """
    Constrained estimates of the total number of people per grid square at a resolution of 3 arc (approximately 100m at the equator) R2025A version v1.  
    Unit: number of people per pixel. 
    
    This function extracts the total population count in the provided bounding box, at each year between 2015-2025.    
    """
    years = np.arange(2015, 2026)
    data_dir = './raw_data/worldpop'

    pop_total = {}
    for year in years:
        fname = data_dir + f"/ssd_pop_{year}_CN_100m_R2025A_v1.tif"
        with rasterio.open(fname) as src:
            ## Extract the correct pixels in the .tif file using the rasterio function
            window = from_bounds(
                bbox['lon_min'], bbox['lat_min'],
                bbox['lon_max'], bbox['lat_max'],
                src.transform
            )
            
            ## Load the data in this window
            arr = src.read(1, window=window).astype(np.float32)

            # Mask nodata
            if src.nodata is not None:
                arr[arr == src.nodata] = np.nan

            total = float(np.nansum(arr))
            pop_total[year] = total


    return pop_total


def main():
    """Example usage"""

    ## Loading population data at a single location:

    ## location at which there are people
    pop_loc = load_worldpop_coordinate(31.046249993815, 9.473750002105)
    print(f"Location with population : lon = 31.046249993815, lat = 9.473750002105" )
    for year, count in pop_loc.items():
        print(f"Year {year} has total population count of {count}")
    print("")

    ## location without people
    pop_loc = load_worldpop_coordinate(31, 9)
    print("pop_loc : ", pop_loc)
    print(f"Location with population : lon = 31, lat = 9" )
    for year, count in pop_loc.items():
        print(f"Year {year} has total population count of {count}")
    print("")
    

    bbox_ex = {}
    bbox_ex['lon_min'] = 29.5
    bbox_ex['lat_min'] = 8.5
    bbox_ex['lon_max'] = 32.5
    bbox_ex['lat_max'] = 10

    pop_area = load_worldpop_area(bbox_ex)
    print("Area : ", bbox_ex)
    for year, count in pop_area.items():
        print(f"Year {year} has total population count of {count}")

if __name__ == "__main__":
    main()


