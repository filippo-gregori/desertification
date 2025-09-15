# Desertification Analysis Tools

A collection of Python scripts for desertification and climate analysis using satellite and reanalysis data.

## Scripts Available

### ERA5 Temperature Downloader
Downloads daily maximum temperature data from ERA5-Land reanalysis for desertification studies.

**Features:**
- Automated download from Copernicus Climate Data Store (CDS)
- Conversion from NetCDF to daily GeoTIFF files
- Configurable geographic areas and time periods
- Resume capability for interrupted downloads
- Comprehensive logging and error handling

## Installation

### Prerequisites
1. **CDS API Account**: Register at [Copernicus Climate Data Store](https://cds.climate.copernicus.eu/api-how-to)
2. **CDS API Key**: Follow [these instructions](https://cds.climate.copernicus.eu/api-how-to) to set up your API key

### Setup
```bash
# Clone repository
git clone https://github.com/filippo-gregori/desertification.git
cd desertification

# Install dependencies
pip install -r requirements.txt

# Configure CDS API (create ~/.cdsapirc file)
echo "url: https://cds.climate.copernicus.eu/api/v2" > ~/.cdsapirc
echo "key: YOUR_CDS_API_KEY" >> ~/.cdsapirc
```

## Usage

### ERA5 Temperature Downloader

**Basic usage with configuration file:**
```bash
python scripts/era5_temperature_downloader.py --config config.yaml
```

**Download specific year/month:**
```bash
# Download entire year
python scripts/era5_temperature_downloader.py --year 2023

# Download specific month
python scripts/era5_temperature_downloader.py --year 2023 --month 6
```

**Download custom period:**
```bash
python scripts/era5_temperature_downloader.py --start-year 2020 --end-year 2023
```

### Configuration

Copy and modify the example configuration:
```bash
cp config/config_example.yaml config.yaml
# Edit config.yaml with your preferences
```

**Key configuration options:**
- `base_dir`: Directory where data will be stored
- `area`: Geographic bounding box [North, West, South, East]
- `period`: Time range to download
- `download_delay`: Delay between downloads (respect CDS limits)

### Output Structure

The script creates the following directory structure:
```
your_base_dir/
├── Daily_Tmax_TIF/          # Daily GeoTIFF files
│   ├── tmax_20230601.tif
│   ├── tmax_20230602.tif
│   └── ...
├── temp/                    # Temporary NetCDF files (auto-deleted)
└── era5_download.log        # Download log
```

## Data Description

**ERA5-Land Daily Maximum Temperature:**
- **Source**: ERA5-Land reanalysis (Copernicus/ECMWF)
- **Resolution**: ~11 km (0.1° x 0.1°)
- **Temporal Coverage**: 1979-present
- **Format**: GeoTIFF (Float32, LZW compressed)
- **Units**: Degrees Celsius
- **CRS**: WGS84 (EPSG:4326)

## Applications

This data is suitable for:
- Desertification monitoring and assessment
- Climate change impact studies
- Agricultural drought analysis
- Heat stress evaluation
- Long-term temperature trend analysis

## Example Areas

**Italy (default):**
```yaml
area: [47.0, 13.0, 39.0, 20.0]
```

**Mediterranean Basin:**
```yaml
area: [45.0, -10.0, 30.0, 40.0]
```

**Sahel Region:**
```yaml
area: [18.0, -20.0, 12.0, 22.0]
```

## Troubleshooting

**Common Issues:**

1. **CDS API errors**: Verify your API key and internet connection
2. **Disk space**: ERA5 data requires significant storage (~1GB per year for Italy)
3. **Memory errors**: Process data in smaller time chunks for large areas
4. **Network timeouts**: Script will retry automatically

**Log files**: Check `era5_download.log` for detailed error information.

## Requirements

- Python 3.8+
- cdsapi
- xarray
- rioxarray
- pyyaml
- numpy
- netcdf4
- rasterio

See `requirements.txt` for specific versions.

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## Citation

If you use this tool in your research, please cite:
```
Gregori, F. (2025). Desertification Analysis Tools. 
GitHub repository: https://github.com/filippo-gregori/desertification
```

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

## Acknowledgments

- [Copernicus Climate Data Store](https://cds.climate.copernicus.eu/) for ERA5 data
- ECMWF for ERA5-Land reanalysis
- xarray and rioxarray communities for excellent Python tools

## Contact

Filippo Gregori - [filippo.gregori3@unibo.it]

Project Link: https://github.com/filippo-gregori/desertification
