import json
import logging
from typing import Dict, Any, Optional

class DataParser:
    def parse(self, raw_data: str):
        """Parse the raw sensor data into a structured format"""
        try:
            if not raw_data:
                return None
                
            parts = raw_data.split(',')
            if len(parts) < 17:  # Date + Time + 8 MT1 values + 8 MT2 values
                return None
                
            date = parts[0]
            time = parts[1]
            
            # Extract MT1 and MT2 readings (skip date and time)
            mt1_readings = [int(val.replace('MT1', '').strip()) for val in parts[2:10]]
            mt2_readings = [int(val.replace('MT2', '').strip()) for val in parts[10:18]]
            
            return {
                "timestamp": f"{date} {time}",
                "MT1": {
                    "values": mt1_readings,
                    "average": sum(mt1_readings) / len(mt1_readings)
                },
                "MT2": {
                    "values": mt2_readings,
                    "average": sum(mt2_readings) / len(mt2_readings)
                }
            }
        except Exception as e:
            return None
