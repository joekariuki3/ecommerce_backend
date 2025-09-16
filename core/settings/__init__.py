import os
from dotenv import load_dotenv
load_dotenv()

ENV = os.getenv("ENVIRONMENT")

if ENV == "production":
    from .production import *
elif ENV == "staging":
    from .staging import *
elif ENV == "testing":
    from .testing import *
else:
    from .development import *
