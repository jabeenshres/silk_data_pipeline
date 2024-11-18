# Silk Data Pipeline

## Overview
This project implements a data pipeline to:
- Fetch raw host data from Qualys and CrowdStrike APIs.
- Normalize the data into a unified format.
- Deduplicate records.
- Save the processed data into MongoDB.
- Generate visualizations for insights.

## Features
1. **Data Normalization**: Standardizes host data from Qualys and CrowdStrike.
2. **Data Deduplication**: Identifies and merges duplicate records.
3. **MongoDB Integration**: Stores processed data for analysis.
4. **Visualization**:
   - Distribution of hosts by OS.
   - Old vs. new hosts.
   - Distribution of open ports.

## Requirements
- Python 3.10
- MongoDB
- `python-dotenv` for managing environment variables.
- `matplotlib` for visualizations.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/silk_data_pipeline.git
   cd silk_data_pipeline