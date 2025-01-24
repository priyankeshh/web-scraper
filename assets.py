from typing import Dict, List
from dataclasses import dataclass

@dataclass
class ModelConfig:
    input_price: float
    output_price: float
    batch_support: bool = False

USER_AGENTS  = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.265 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.265 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.265 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6777.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
]

PRICING: Dict[str, ModelConfig] = {
    "gpt-4o-mini": ModelConfig(
        input_price=0.150 / 1_000_000,
        output_price=0.600 / 1_000_000
    ),
    "gpt-4o-2024-08-06": ModelConfig(
        input_price=2.5 / 1_000_000,    # $2.5 per 1M input tokens
        output_price=10.0 / 1_000_000   # $10 per 1M output tokens
    ),
    "gemini-1.5-flash": ModelConfig(
        input_price=0.075 / 1_000_000,  # $0.075 per 1M input tokens
        output_price=0.30 / 1_000_000   # $0.30 per 1M output tokens
    ),
    "Llama3.1 8B": ModelConfig(
        input_price=0,                  # Free
        output_price=0                  # Free
    ),
    "Groq Llama3.1 70b": ModelConfig(
        input_price=0,                  # Free
        output_price=0                  # Free
    )
}

MODEL_NAMES = {
    "GPT4_MINI": "gpt-4o-mini",
    "GPT4_2024": "gpt-4o-2024-08-06",
    "GEMINI_15": "gemini-1.5-flash",
    "LLAMA_8B": "Llama3.1 8B",
    "GROQ_LLAMA": "Groq Llama3.1 70b"    
}

class Config:
    SELENIUM_TIMEOUT = 30
    MAX_RETRIES = 3
    CACHE_TTL = 3600
    MAX_WORKERS = 3
    MODEL_CONFIGS = {
        "gemini-2.0-flash-exp": {
            "temperature": 0.7,
            "max_tokens": 1000
        }
    }

TIMEOUT_SETTINGS = {
    "page_load": 30,
    "script": 10
}

REQUEST_SETTINGS = {
    "max_retries": 3,
    "backoff_factor": 0.3,
    "status_forcelist": [500, 502, 503, 504],
    "timeout": 30,
    "verify": True,
    "headers": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
}

RETRY_SETTINGS = {
    "max_retries": 3,
    "base_delay": 1,
    "exponential_base": 2,
    "max_delay": 60
}

RATE_LIMIT = {
    "requests_per_second": 2,
    "burst_limit": 5
}

MAX_WORKERS = 3

HEADLESS_OPTIONS = [ "--headless=new","--disable-gpu", "--disable-dev-shm-usage","--window-size=1920,1080","--disable-search-engine-choice-screen"]

PROGRESS_LOG_FILE = "scraping_progress.log"

LLAMA_MODEL_FULLNAME="lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF"
GROQ_LLAMA_MODEL_FULLNAME="llama-3.1-70b-versatile"

SYSTEM_MESSAGE = """You are an intelligent text extraction and conversion assistant. Your task is to extract structured information 
                        from the given text and convert it into a pure JSON format. The JSON should contain only the structured data extracted from the text, 
                        with no additional commentary, explanations, or extraneous information. 
                        You could encounter cases where you can't find the data of the fields you have to extract or the data will be in a foreign language.
                        Please process the following text and provide the output in pure JSON format with no words before or after the JSON:"""

USER_MESSAGE = f"Extract the following information from the provided text:\nPage content:\n\n"