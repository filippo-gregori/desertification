# ERA5 Climate Data Downloader

A Python script to download and convert ERA5 climate data from Copernicus Climate Data Store (CDS) to daily GeoTIFF files. Perfect for climate analysis, environmental research, and machine learning applications.

## Features

- **Multiple Climate Variables**: Temperature (min/max/mean), precipitation, and evapotranspiration
- **Daily GeoTIFF Output**: Ready-to-use raster files for GIS and analysis
- **Flexible Geographic Areas**: Configurable bounding boxes for any region
- **Automatic Restart**: Resumes downloads from where it left off
- **Unit Conversion**: Automatic conversion to standard units (°C, mm/day)
- **Robust Error Handling**: Continues processing even if individual downloads fail

## Requirements

### Software Dependencies
```bash
pip install -r requirements.txt
```

### CDS API Setup
1. Create a free account at [Copernicus CDS](https://cds.climate.copernicus.eu)
2. Install your API key following [these instructions](https://cds.climate.copernicus.eu/api-how-to)
3. Accept the ERA5 license terms in your CDS account

## Quick Start

1. **Clone this repository**
   ```bash
   git clone https://github.com/yourusername/ERA5-Climate-Downloader.git
   cd ERA5-Climate-Downloader
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the script**
   Edit the configuration section in `era5_climate_downloader.py`:
   ```python
   BASE_PATH = r'C:\your\data\directory'
   DATA_TYPE = 'tmax'  # Choose: 'tmax', 'tmin', 'tmean', 'precipitation', 'evapotranspiration'
   AREA_NAME = 'Italy'
   GEOGRAPHIC_AREA = [47.0, 13.0, 39.0, 20.0]  # [North, West, South, East]
   START_YEAR = 1979
   END_YEAR = 2024
   ```

4. **Run the script**
   ```bash
   python era5_climate_downloader.py
   ```

## Data Types

| Variable | Description | Units | Source Dataset |
|----------|-------------|-------|----------------|
| **tmax** | Daily maximum temperature | °C | ERA5-Land daily statistics |
| **tmin** | Daily minimum temperature | °C | ERA5-Land daily statistics |
| **tmean** | Daily mean temperature | °C | ERA5-Land daily statistics |
| **precipitation** | Daily precipitation totals | mm/day | ERA5-Land (hourly aggregated) |
| **evapotranspiration** | Daily potential evapotranspiration | mm/day | ERA5-Land (hourly aggregated) |

## Output Structure

```
ERA5_[DATATYPE]_[AREA]/
├── Daily_[Datatype]_TIF/
│   ├── tmax_19790101.tif
│   ├── tmax_19790102.tif
│   └── ...
└── temp/
    └── (temporary download files)
```

## 🗺Geographic Areas

### Predefined Areas
- **Italy**: `[47.0, 13.0, 39.0, 20.0]`
- **Europe**: `[71.0, -25.0, 34.0, 45.0]`
- **Mediterranean**: `[46.0, -6.0, 30.0, 37.0]`

### Custom Areas
Define your own bounding box as `[North, West, South, East]` in decimal degrees.

## Configuration Options

### Time Range
```python
START_YEAR = 1979    # ERA5 data available from 1979
START_MONTH = 1      # Resume from specific month
END_YEAR = 2024      # Up to present (~2-month delay)
```

### Data Processing
- **Temperature data**: Pre-computed daily statistics from Copernicus
- **Precipitation/ET**: Hourly data automatically aggregated to daily totals
- **Automatic unit conversion**: Kelvin→°C, meters→millimeters

## Performance Notes

- **Download Speed**: Temperature data is faster (pre-aggregated), precipitation/ET slower (hourly data)
- **Storage Requirements**: ~16,000 files per variable for full time series (1979-2024)
- **File Size**: ~2-10 MB per daily GeoTIFF (depends on geographic area)
- **Restart Capability**: Script automatically skips completed months

## Troubleshooting

### Common Issues
1. **CDS API Key**: Make sure your `.cdsapirc` file is properly configured
2. **Disk Space**: Ensure sufficient storage for the time series you're downloading
3. **Network**: Large downloads may be interrupted; the script will resume automatically
4. **Coordinates**: Use decimal degrees in the format `[North, West, South, East]`

### Error Messages
- **Download errors**: Usually temporary network issues, script will retry
- **Conversion errors**: Check available disk space and file permissions

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## Citation

If you use this tool in your research, please cite:
```
Gregori, F. (2024). Desertification Analysis with Remote Sensing Analysis. 
GitHub repository: https://github.com/filippo-gregori/desertification
```

## Acknowledgments

- **Copernicus Climate Change Service (C3S)** for providing ERA5 data
- **European Centre for Medium-Range Weather Forecasts (ECMWF)** for ERA5 reanalysis
- Data source: Hersbach, H., Bell, B., Berrisford, P., et al. (2020). The ERA5 global reanalysis. Q J R Meteorol Soc, 146: 1999-2049.

---

**Need help?** Open an issue or check the [CDS documentation](https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-land).
