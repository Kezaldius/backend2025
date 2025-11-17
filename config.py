import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    API_TITLE = "Finance REST API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    JWT = os.environ.get("JWT")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}"
        f"@{os.environ.get('DB_HOST')}/{os.environ.get('POSTGRES_DB')}"
    )