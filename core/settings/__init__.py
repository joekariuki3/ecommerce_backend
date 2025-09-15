import os
from dotenv import load_dotenv
load_dotenv()

ENV = os.getenv("ENVIRONMENT")
print(f"ENVIRONMENT: {ENV}")

if ENV == "production":
    from .production import *
elif ENV == "staging":
    from .staging import *
else:
    from .development import *
