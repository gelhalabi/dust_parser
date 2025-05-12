# Dust Sensor Monitor

Tool for verifying dust sensor data output over network connection.

## Directory Structure
```
dust_sensor/
├── src/                # Source code
│   ├── sensor/        # Sensor communication modules
│   └── utils/         # Utility functions
├── tests/             # Test files
├── config/            # Configuration files
└── README.md         # Project documentation
```

## Setup
1. Ensure Python 3.12 or later is installed
2. Install required packages:
   ```
   pip install pyyaml
   ```
3. Clone or download this repository
4. Verify your sensor configuration in `config/settings.yaml`:
   - Default host: 10.40.200.32
   - Default port: 50003
   - Sensor heights: 2m and 24m

## Usage
1. Navigate to the project directory:
   ```
   cd path/to/dust_sensor
   ```

2. Run the monitoring script:
   ```
   python3 src/main.py
   ```

The program will:
- Connect to the dust sensors
- Display both raw and parsed data
- Show particle counts for 8 size ranges (0.3µm to 10.0µm)
- Update readings every second

To stop the program, press Ctrl+C.

### Data Format
Each reading shows:
- Raw sensor data
- Timestamp
- MT1 readings (2m height)
- MT2 readings (24m height)

Each sensor reports particle counts in these size ranges:
- P1: ≥ 0.3 µm
- P2: ≥ 0.5 µm
- P3: ≥ 0.7 µm
- P4: ≥ 1.0 µm
- P5: ≥ 2.0 µm
- P6: ≥ 3.0 µm
- P7: ≥ 5.0 µm
- P8: ≥ 10.0 µm
