from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(dotenv_path=find_dotenv())


class Settings:
    TITLE = "Kolesa parser application"
    DESCRIPTION = """
    ## Parser for kolesa.kz created in FASTAPI
    Sending xlsx file to email with information of adds
    """
    CONTACT = {
        "name": "Baigonus Dinmukhamed",
        "email": "d.baigonus@gmail.com"
    }
    TAGS = [
        {
            "name": "Adds",
            "description": "Finding adds API"
        },
        {
            "name": "Sending email",
            "description": "Sending ready xlsx to email"
        },
        {
            "name": "Parse kolesa.kz's adds",
            "description": "Parsing adds and sending email"
        }
    ]

    # POSTGRES_USER = os.getenv("POSTGRES_USER")
    # POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    # POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")
    # POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    # POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")
    # DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
    # SECRET_KEY : str = os.getenv("SECRET_KEY")
    # ALGORITHM : str = os.getenv("ALGORITHM")
    # TEST_USER : str = os.getenv("TEST_USER")
    # TEST_PASSWORD : str = os.getenv("TEST_PASSWORD")
settings = Settings()