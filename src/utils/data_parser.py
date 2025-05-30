import json
import logging
from typing import Dict, Any, Optional

class DataParser:
    # Particle size ranges in micrometers
    PARTICLE_SIZES = [
        "≥ 0.3 µm",
        "≥ 0.5 µm",
        "≥ 0.7 µm",
        "≥ 1.0 µm",
        "≥ 2.0 µm",
        "≥ 3.0 µm",
        "≥ 5.0 µm",
        "≥ 10.0 µm"
    ]

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
            
            # Create readings with size context
            mt1_with_size = [{"size": size, "count": count} 
                           for size, count in zip(self.PARTICLE_SIZES, mt1_readings)]
            mt2_with_size = [{"size": size, "count": count} 
                           for size, count in zip(self.PARTICLE_SIZES, mt2_readings)]
            
            return {
                "timestamp": f"{date} {time}",
                "MT1": {"readings": mt1_with_size},
                "MT2": {"readings": mt2_with_size}
            }
        except Exception as e:
            return None
