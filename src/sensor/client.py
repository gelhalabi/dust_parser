import asyncio
import logging
from typing import Optional, Tuple

class SensorClient:
    def __init__(self, host: str, port: int, timeout: int = 10):
        self.host = host
        self.port = port
        self.timeout = timeout
        self._connection: Optional[Tuple[asyncio.StreamReader, asyncio.StreamWriter]] = None

    async def connect(self):
        """Establish connection to sensor"""
        try:
            self._connection = await asyncio.wait_for(
                asyncio.open_connection(self.host, self.port),
                timeout=self.timeout
            )
            logging.info(f"Connected to dust sensor at {self.host}:{self.port}")
        except Exception as e:
            logging.error(f"Failed to connect to dust sensor: {e}")
            self._connection = None
            raise

    async def read_data(self) -> Optional[str]:
        """Read raw data from sensor"""
        if not self._connection:
            logging.error("No active connection")
            return None
        
        try:
            reader, _ = self._connection
            data = await asyncio.wait_for(reader.readline(), timeout=5)
            return data.decode().strip()
        except Exception as e:
            logging.error(f"Error reading data: {e}")
            return None

    async def close(self):
        """Close the connection"""
        if self._connection:
            _, writer = self._connection
            writer.close()
            await writer.wait_closed()
            logging.info("Connection closed")
