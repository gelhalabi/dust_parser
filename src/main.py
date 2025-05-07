#!/usr/bin/env python3

"""
Dust Sensor Monitor
Main entry point for the dust sensor monitoring tool.
"""

import asyncio
import logging
import yaml
from sensor.client import SensorClient
from utils.data_parser import DataParser

def setup_logging(config):
    """Configure logging based on settings"""
    logging.basicConfig(
        level=getattr(logging, config["logging"]["level"]),
        format=config["logging"]["format"]
    )

async def main():
    # Load configuration
    with open("config/settings.yaml", "r") as f:
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
                data = parser.parse(raw_data)
                if data:
                    print("\n=== Dust Sensor Readings ===")
                    print(f"Time: {data['timestamp']}")
                    print("\nMT1 Values:")
                    print(f"  Average: {data['MT1']['average']:.2f}")
                    print(f"  Readings: {', '.join(map(str, data['MT1']['values']))}")
                    print("\nMT2 Values:")
                    print(f"  Average: {data['MT2']['average']:.2f}")
                    print(f"  Readings: {', '.join(map(str, data['MT2']['values']))}")
            
            await asyncio.sleep(config["sensor"]["read_interval"])
            
    except KeyboardInterrupt:
        print("\nStopping dust sensor monitoring...")
    except Exception as e:
        logging.error(f"Error: {e}")
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
