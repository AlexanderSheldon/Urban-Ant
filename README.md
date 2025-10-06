# Urban-Ant
Welcome to the home of Urban Ant's Operations
---
**Urban Ant** helps city planners identify where public transit is needed most. By combining open data from the U.S. Census Bureau and TransitLand, Urban Ant maps areas of high demand and unmet accessibility, providing a foundation for smarter, data-driven decisions in urban development.

## Group Links
Github only allows files to be 100 MB, which the Transitland datasets exceed. For now I've created a google drive https://drive.google.com/drive/folders/1gFQ6tWOg2vqyWpBK5Pg3H5ERe7P4y1qf?usp=drive_link. In the future, I'd like to incorporate live transitland data, using their API.

## Overview
Urban Ant is an early-stage prototype focused on modeling public transit need across U.S. urban areas. It uses demographic and commuting data from the **American Community Survey (ACS)** alongside real-time **TransitLand GTFS feeds** to visualize gaps in transit coverage.  
The goal is to make it easier for planners, researchers, and city stakeholders to understand where investment in transit would have the greatest impact for the fewest dollars.

## Data Sources
- **American Community Survey (ACS):** population density, commuting modes, income, and vehicle access by census tract  
- **TransitLand:** generalized GTFS (a standardized transit data format) feed aggregations for existing transit routes and stops across U.S. metro regions

## Repository Contents
- `src/` — Python scripts for data ingestion, cleaning, and spatial joins  
- `data/` — Raw and processed CSV / GeoJSON files  
- `gis_layers/` — ArcGIS Pro project files and spatial outputs  
- `docs/` — Internal documentation and notes  


## Tech Stack
- **Python** (GeoPandas, Pandas, Requests, etc.)  
- **ArcGIS Pro** for spatial visualization and map composition  


## Current Stage
Urban Ant is an internal prototype in active development. Current efforts focus on refining data pipelines, and creating early visualization layers. Future work will expand toward deploying interactive dashboards.

