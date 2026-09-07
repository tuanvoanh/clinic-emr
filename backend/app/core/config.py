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

    # JWT Settings
    SECRET_KEY: str = "super-secret-key-for-development" # Change in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 # 8 days

    # Initial Superuser Settings
    FIRST_SUPERUSER_EMAIL: str = "admin@clinic.com"
    FIRST_SUPERUSER_PASSWORD: str = "adminpassword"
    FIRST_SUPERUSER_FULL_NAME: str = "Admin Setup"

    model_config = {
        "env_file": ".env",
        "extra": "ignore",
    }

# Initialize a singleton instance to import in other modules
settings = Settings()
