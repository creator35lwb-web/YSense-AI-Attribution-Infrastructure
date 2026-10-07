"""
YSenseAI v4.5-Beta: Configuration
API keys and settings are read from environment variables (see .env.example).

Importing this module never raises. If a key is missing, the matching client
falls back to offline mode and the app still starts, so the attribution,
consent, library, and export features keep working without any AI provider.
"""

import os
import warnings
from pathlib import Path

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # python-dotenv is optional
    pass

# Alibaba Cloud Qwen (optional; used for alternative layer extraction)
QWEN_API_KEY = os.getenv("QWEN_API_KEY", "")
QWEN_MODEL = os.getenv("QWEN_MODEL", "qwen-plus")
QWEN_BASE_URL = os.getenv(
    "QWEN_BASE_URL", "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
)

# Anthropic Claude (recommended; used for layer extraction and distillation)
# claude-3-haiku-20240307 was retired on 19 April 2026. Default to the current
# small model; set ANTHROPIC_MODEL=claude-sonnet-5-5 for higher quality output.
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5")

if not ANTHROPIC_API_KEY:
    warnings.warn(
        "ANTHROPIC_API_KEY is not set. AI analysis runs in offline fallback mode. "
        "Copy .env.example to .env and add your key to enable it.",
        stacklevel=1,
    )

# Platform Configuration
PLATFORM_NAME = "YSenseAI v4.5-Beta | 慧觉™"
PLATFORM_VERSION = "4.5-beta"
DATABASE_PATH = Path(
    os.getenv("DATABASE_PATH", str(Path(__file__).parent / "database" / "ysense_v45_beta.db"))
)

# Create database directory if it doesn't exist
DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
