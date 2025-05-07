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
        timeout=config["sensor"]["timeout"]
    )
    
    # Start monitoring loop
    try:
        await client.connect()
        parser = DataParser()
        
        while True:
            raw_data = await client.read_data()
            if raw_data:
                logging.debug(f"Raw data received: {raw_data}")
                parsed_data = parser.parse(raw_data)
                if parsed_data:
                    print("\nDust Sensor Reading:")
                    for key, value in parsed_data.items():
                        print(f"  - {key}: {value}")
            else:
                logging.warning("No data received from sensor")
                
            await asyncio.sleep(config["sensor"]["read_interval"])
            
    except Exception as e:
        logging.error(f"Critical error: {e}")
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
