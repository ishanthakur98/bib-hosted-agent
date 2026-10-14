import os

HOST = os.getenv("AGENT_HOST", "127.0.0.1")
PORT = int(os.getenv("AGENT_PORT", "8088"))
REPLY_PREFIX = os.getenv("AGENT_REPLY_PREFIX", "Demo agent: ")

# DEMO-ONLY: intentional finding - fake API key, never used.
FAKE_API_KEY = "sk-demo-only-FAKE-00000000000000000000000000000000"
# DEMO-ONLY: intentional finding - fake connection string, never used.
FAKE_CONNECTION_STRING = (
    "DefaultEndpointsProtocol=https;AccountName=demoonlyfake;"
    "AccountKey=RE9OT1RVU0UtREVNTy1PTkxZLUZBS0UtS0VZ;"
    "BlobEndpoint=https://demoonlyfake.invalid/;"
)
