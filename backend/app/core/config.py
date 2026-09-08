from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Manage configurations and environment variables for the entire application.
    Uses Pydantic BaseSettings to automatically read from the .env file.
    """
    PROJECT_NAME: str = "ClinicCare Mini EMR API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API supporting a minimalist Electronic Medical Record system for clinics."

    # URL for local SQLite database connection
    DATABASE_URL: str = "sqlite:///./clinic.db"

    # JWT Settings (SECRET_KEY is mandatory from environment)
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # Shortened token lifetime (60 minutes)

    # Initial Superuser Settings (Mandatory from environment)
    FIRST_SUPERUSER_EMAIL: str
    FIRST_SUPERUSER_PASSWORD: str
    FIRST_SUPERUSER_FULL_NAME: str = "Clinic Administrator"

    # Security toggle to disable public /setup route after initial provisioning
    ALLOW_SETUP_ENDPOINT: bool = True

    model_config = {
        "env_file": ".env",
        "extra": "ignore",
    }

# Initialize a singleton instance to import in other modules
settings = Settings()
