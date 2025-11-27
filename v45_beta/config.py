"""
YSenseAI v4.5-Beta: Configuration
API keys and settings
"""

import os
from pathlib import Path

# Load from environment variables (REQUIRED)
# Copy .env.example to .env and fill in your API keys
QWEN_API_KEY = os.getenv("QWEN_API_KEY")
QWEN_MODEL = os.getenv("QWEN_MODEL", "qwen-plus")
QWEN_BASE_URL = os.getenv("QWEN_BASE_URL", "https://dashscope-intl.aliyuncs.com/compatible-mode/v1")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-haiku-20240307")

# Validate API keys
if not QWEN_API_KEY:
    raise ValueError("QWEN_API_KEY environment variable is required. Copy .env.example to .env and add your API key.")
if not ANTHROPIC_API_KEY:
    raise ValueError("ANTHROPIC_API_KEY environment variable is required. Copy .env.example to .env and add your API key.")

# Platform Configuration
PLATFORM_NAME = "YSenseAI v4.5-Beta | 慧觉™"
PLATFORM_VERSION = "4.5-beta"
DATABASE_PATH = Path(__file__).parent / "database" / "ysense_v45_beta.db"

# Create database directory if it doesn't exist
DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
