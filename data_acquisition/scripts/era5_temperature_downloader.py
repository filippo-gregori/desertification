
#!/usr/bin/env python3
"""
ERA5 Daily Maximum Temperature Downloader

This script downloads ERA5 Land daily maximum temperature data from 
Copernicus Climate Data Store (CDS) and converts it to daily GeoTIFF files.
Designed for desertification analysis and climate studies.

Author: Filippo Gregori
Date: 2025
License: GPL v3

Copyright (C) 2025 Filippo Gregori

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

Requirements:
- CDS API account and key configured
- Python packages: cdsapi, xarray, rioxarray

Usage:
    python era5_temperature_downloader.py --config config.yaml
    python era5_temperature_downloader.py --year 2023 --month 6
"""

import cdsapi
import os
import xarray as xr
import rioxarray
import time
import argparse
import yaml
import logging
from datetime import datetime
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('era5_download.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ERA5TemperatureDownloader:
    """Download and process ERA5 daily maximum temperature data"""
    
    def __init__(self, config):
        """Initialize downloader with configuration"""
        self.config = config
        self.base_dir = Path(config['paths']['base_dir'])
        self.daily_dir = self.base_dir / 'Daily_Tmax_TIF'
        self.temp_dir = self.base_dir / 'temp'
        
        # Create directories
        self.daily_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize CDS client
        try:
            self.client = cdsapi.Client()
            logger.info("CDS client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize CDS client: {e}")
            raise
    
    def has_month_data(self, year, month):
        """Check if month data is already complete"""
        prefix = f"tmax_{year}{month:02d}"
        existing_files = list(self.daily_dir.glob(f"{prefix}*.tif"))
        min_expected_days = 25  # Account for months with different lengths
        
        has_data = len(existing_files) >= min_expected_days
        if has_data:
            logger.info(f"Month {year}-{month:02d} already complete ({len(existing_files)} files)")
        
        return has_data
    
    def download_month_data(self, year, month):
        """Download and process data for a specific month"""
        if self.has_month_data(year, month):
            return True
        
        temp_file = self.temp_dir / f"temp_{year}_{month:02d}.nc"
        
        logger.info(f"Starting download for {year}-{month:02d}")
        
        try:
            # Prepare request parameters
            request_params = {
                "variable": ["2m_temperature"],
                "year": str(year),
                "month": f"{month:02d}",
                "day": [f"{d:02d}" for d in range(1, 32)],
                "daily_statistic": "daily_maximum",
                "time_zone": "utc+00:00",
                "area": self.config['area'],  # [North, West, South, East]
                "format": "netcdf"
            }
            
            # Download data
            self.client.retrieve(
                "derived-era5-land-daily-statistics", 
                request_params, 
                str(temp_file)
            )
            
            logger.info(f"Download completed for {year}-{month:02d}")
            
            # Process and convert to GeoTIFF
            success = self._convert_to_geotiff(temp_file, year, month)
            
            # Cleanup
            if temp_file.exists():
                temp_file.unlink()
                
            return success
            
        except Exception as e:
            logger.error(f"Download failed for {year}-{month:02d}: {e}")
            if temp_file.exists():
                temp_file.unlink()
            return False
    
    def _convert_to_geotiff(self, nc_file, year, month):
        """Convert NetCDF to daily GeoTIFF files"""
        try:
            logger.info(f"Converting {year}-{month:02d} to GeoTIFF")
            
            # Open dataset
            with xr.open_dataset(nc_file) as ds:
                # Set CRS
                ds.t2m.rio.write_crs("EPSG:4326", inplace=True)
                
                processed_days = 0
                for i, time_val in enumerate(ds.valid_time.values):
                    # Extract date
                    date_str = str(time_val)[:10].replace('-', '')
                    tif_file = self.daily_dir / f'tmax_{date_str}.tif'
                    
                    if not tif_file.exists():
                        # Convert from Kelvin to Celsius
                        daily_data = ds.t2m.isel(valid_time=i) - 273.15
                        
                        # Save as GeoTIFF
                        daily_data.rio.to_raster(
                            str(tif_file), 
                            dtype='float32',
                            compress='lzw'
                        )
                        processed_days += 1
                
                logger.info(f"Converted {processed_days} days for {year}-{month:02d}")
                return True
                
        except Exception as e:
            logger.error(f"Conversion failed for {year}-{month:02d}: {e}")
            return False
    
    def download_period(self, start_year, start_month, end_year, end_month=12):
        """Download data for a specified period"""
        logger.info(f"Starting download from {start_year}/{start_month:02d} to {end_year}/{end_month:02d}")
        
        total_months = 0
        successful_months = 0
        
        for year in range(start_year, end_year + 1):
            month_start = start_month if year == start_year else 1
            month_end = end_month if year == end_year else 12
            
            for month in range(month_start, month_end + 1):
                total_months += 1
                
                if self.download_month_data(year, month):
                    successful_months += 1
                
                # Small delay to be respectful to the service
                time.sleep(self.config.get('download_delay', 2))
        
        logger.info(f"Download completed: {successful_months}/{total_months} months successful")
        return successful_months == total_months

def load_config(config_file):
    """Load configuration from YAML file"""
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        logger.error(f"Failed to load config file {config_file}: {e}")
        raise

def create_default_config():
    """Create default configuration"""
    return {
        'paths': {
            'base_dir': 'C:/Desertification/Dataset/CNN_Training/ERA5_Tmax'
        },
        'area': [47.0, 13.0, 39.0, 20.0],  # Italy [North, West, South, East]
        'download_delay': 2,  # seconds between downloads
        'period': {
            'start_year': 1979,
            'start_month': 1,
            'end_year': 2024,
            'end_month': 12
        }
    }

def main():
    parser = argparse.ArgumentParser(description='Download ERA5 daily maximum temperature data')
    parser.add_argument('--config', type=str, help='Configuration file path')
    parser.add_argument('--year', type=int, help='Specific year to download')
    parser.add_argument('--month', type=int, help='Specific month to download (requires --year)')
    parser.add_argument('--start-year', type=int, help='Start year for range download')
    parser.add_argument('--start-month', type=int, default=1, help='Start month')
    parser.add_argument('--end-year', type=int, help='End year for range download')
    parser.add_argument('--end-month', type=int, default=12, help='End month')
    
    args = parser.parse_args()
    
    # Load configuration
    if args.config:
        config = load_config(args.config)
    else:
        logger.warning("No config file provided, using default configuration")
        config = create_default_config()
    
    # Initialize downloader
    downloader = ERA5TemperatureDownloader(config)
    
    # Determine what to download
    if args.year:
        if args.month:
            # Download specific month
            success = downloader.download_month_data(args.year, args.month)
            logger.info(f"Download {'successful' if success else 'failed'}")
        else:
            # Download entire year
            success = downloader.download_period(args.year, 1, args.year, 12)
    elif args.start_year:
        # Download range
        end_year = args.end_year or args.start_year
        success = downloader.download_period(
            args.start_year, args.start_month, 
            end_year, args.end_month
        )
    else:
        # Use config period
        period = config['period']
        success = downloader.download_period(
            period['start_year'], period['start_month'],
            period['end_year'], period.get('end_month', 12)
        )
    
    logger.info("Process completed")

if __name__ == "__main__":
    main()
