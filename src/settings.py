import os

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")
PROMPTS_DEBUG_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts_debug")

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "test_key")