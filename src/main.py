#!/usr/bin/env python3

"""
Dust Sensor Monitor
Main entry point for the dust sensor monitoring tool.
"""

import asyncio
import logging
import yaml
import os
from sensor.client import SensorClient
from utils.data_parser import DataParser

def setup_logging(config):
    """Configure logging based on settings"""
    logging.basicConfig(
        level=getattr(logging, config["logging"]["level"]),
        format=config["logging"]["format"]
    )

async def main():
    # Get the absolute path to the config file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    config_path = os.path.join(project_root, "config", "settings.yaml")

    # Load configuration
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    
    # Setup logging
    setup_logging(config)
    
    # Initialize sensor client
    client = SensorClient(
        host=config["sensor"]["host"],
        port=config["sensor"]["port"],
        sensor_config=config["sensor"]["sensors"],
        timeout=config["sensor"]["timeout"]
    )
    
    # Start monitoring loop
    try:
        await client.connect()
        parser = DataParser()
        
        while True:
            raw_data = await client.read_data()
            if raw_data:
                print("\n=== Raw Sensor Data ===")
                print(f"Raw: {raw_data}")
                print("\n=== Parsed Data ===")
                
                data = parser.parse(raw_data)
                if data:
                    print(f"Time: {data['timestamp']}")
                    
                    print("\nMT1 Values:")
                    print("  Readings:")
                    for reading in data['MT1']['readings']:
                        print(f"    {reading['size']}: {reading['count']}")
                    
                    print("\nMT2 Values:")
                    print("  Readings:")
                    for reading in data['MT2']['readings']:
                        print(f"    {reading['size']}: {reading['count']}")
            
            await asyncio.sleep(config["sensor"]["read_interval"])
            
    except KeyboardInterrupt:
        print("\nStopping dust sensor monitoring...")
    except Exception as e:
        logging.error(f"Error: {e}")
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
