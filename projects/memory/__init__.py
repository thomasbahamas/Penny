#!/usr/bin/env python3
"""
Penny Memory Integration Wrapper
Import this to automatically log all conversations
"""
import sys
sys.path.insert(0, '/root/clawd/projects/memory')

from conversation_logger import get_logger
from morning_recap import MorningRecap
from penny_memory import PennyMemory

# Export main interfaces
__all__ = ['log_conversation', 'get_memory', 'generate_recap', 'get_logger', 'MorningRecap', 'PennyMemory']

def log_conversation(user_msg: str, assistant_response: str, context: dict = None):
    """Quick function to log a conversation"""
    logger = get_logger()
    return logger.log_interaction(user_msg, assistant_response, context)

def get_memory():
    """Get PennyMemory instance"""
    return PennyMemory()

def generate_recap():
    """Generate morning recap"""
    recap = MorningRecap()
    return recap.generate_recap()

# Example usage:
# from penny_memory_integration import log_conversation, generate_recap
# log_conversation("What's the BONK price?", "BONK is at $0.000006...")
# text, file = generate_recap()
