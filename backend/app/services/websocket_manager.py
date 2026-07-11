from fastapi import WebSocket
from typing import List, Set
import json
import asyncio
import logging

logger = logging.getLogger(__name__)


class WebSocketManager:
    """
    Manages WebSocket connections for real-time dashboard updates
    Handles connection lifecycle and broadcasting to multiple clients
    """

    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        """Accept a new WebSocket connection"""
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"WebSocket connected. Active connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        """Remove a disconnected WebSocket"""
        self.active_connections.discard(websocket)
        logger.info(f"WebSocket disconnected. Active connections: {len(self.active_connections)}")

    async def broadcast(self, data: dict):
        """
        Broadcast data to all connected clients
        """
        if not self.active_connections:
            logger.debug("No active connections to broadcast to")
            return

        disconnected = []
        
        for connection in self.active_connections:
            try:
                await connection.send_json(data)
            except Exception as e:
                logger.error(f"Error broadcasting to connection: {str(e)}")
                disconnected.append(connection)

        # Clean up disconnected clients
        for connection in disconnected:
            self.disconnect(connection)

    async def send_personal(self, websocket: WebSocket, data: dict):
        """Send data to a specific client"""
        try:
            await websocket.send_json(data)
        except Exception as e:
            logger.error(f"Error sending personal message: {str(e)}")
            self.disconnect(websocket)

    async def receive_and_process(self, websocket: WebSocket, processor):
        """
        Receive messages from a client and process them
        processor: async function(message) that handles the message
        """
        try:
            while True:
                data = await websocket.receive_text()
                message = json.loads(data)
                await processor(message, websocket)
        except Exception as e:
            logger.info(f"WebSocket client disconnected: {str(e)}")
            self.disconnect(websocket)


# Global instance
manager = WebSocketManager()