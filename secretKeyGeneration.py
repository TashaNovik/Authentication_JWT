import secrets

key = secrets.token_urlsafe(32)

with open("my_jwt_secret.key", "a") as env_file:
    env_file.write(f"{key}\n")

