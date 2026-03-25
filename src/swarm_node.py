import hashlib
from typing import List, Dict, Any
from dataclasses import dataclass
from time import time
import asyncio

@dataclass
class Message:
    sender_id: str
    payload: Any
    timestamp: float
    signature: str

class SwarmNode:
    def __init__(self, node_id: str, private_key: str):
        self.node_id = node_id
        self.private_key = private_key
        self.peers: List[str] = []
        self.message_pool: Dict[str, Message] = {}
        self.consensus_threshold = 0.67  # 2/3 majority for Byzantine fault tolerance
        
    def sign_message(self, payload: Any) -> Message:
        timestamp = time()
        message_data = f"{self.node_id}{payload}{timestamp}"
        signature = hashlib.sha256(
            f"{message_data}{self.private_key}".encode()
        ).hexdigest()
        return Message(
            sender_id=self.node_id,
            payload=payload,
            timestamp=timestamp,
            signature=signature
        )
    
    async def broadcast_message(self, message: Message) -> None:
        self.message_pool[message.signature] = message
        # Simulate network broadcast to peers
        for peer_id in self.peers:
            await self.send_to_peer(peer_id, message)
    
    async def send_to_peer(self, peer_id: str, message: Message) -> None:
        # Implement actual peer communication logic here
        pass
    
    def verify_message(self, message: Message) -> bool:
        message_data = f"{message.sender_id}{message.payload}{message.timestamp}"
        # In practice, would verify using sender's public key
        return len(message.signature) == 64  # Simple check for demo
    
    async def process_message(self, message: Message) -> None:
        if not self.verify_message(message):
            return
            
        self.message_pool[message.signature] = message
        
        # Check for consensus
        consensus = await self.check_consensus(message)
        if consensus:
            await self.execute_consensus_action(message.payload)
    
    async def check_consensus(self, message: Message) -> bool:
        matching_messages = [
            msg for msg in self.message_pool.values()
            if msg.payload == message.payload
        ]
        return len(matching_messages) >= len(self.peers) * self.consensus_threshold
    
    async def execute_consensus_action(self, payload: Any) -> None:
        # Implement consensus-reached actions here
        print(f"Consensus reached for payload: {payload}")
    
    async def run(self):
        while True:
            # Main node operation loop
            await asyncio.sleep(1)

    def add_peer(self, peer_id: str) -> None:
        if peer_id not in self.peers:
            self.peers.append(peer_id)

    def remove_peer(self, peer_id: str) -> None:
        if peer_id in self.peers:
            self.peers.remove(peer_id)