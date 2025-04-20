import os
import secrets

key = secrets.token_urlsafe(32)

print(f"Your SECRET_KEY: {key}")

with open(".env", "a") as env_file:
    env_file.write(f"SECRET_KEY={key}\n")



from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")

if SECRET_KEY is None:
    raise ValueError("SECRET_KEY not set") #
