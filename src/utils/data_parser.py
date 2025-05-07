import json
import logging
from typing import Dict, Any, Optional

class DataParser:
    @staticmethod
    def parse(raw_data: str) -> Optional[Dict[str, Any]]:
        """Parse raw JSON data from sensor"""
        try:
            data = json.loads(raw_data)
            logging.debug(f"Successfully parsed data: {data}")
            return data
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error during JSON parsing: {e}")
            return None
