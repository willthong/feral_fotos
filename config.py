import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    READ_API_KEY = os.environ.get("READ_API_KEY")
    WRITE_API_KEY = os.environ.get("WRITE_API_KEY")
    APPLY_BORDER = os.environ.get("APPLY_BORDER") or True
