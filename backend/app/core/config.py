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

    class Config:
        env_file = ".env"

# Initialize a singleton instance to import in other modules
settings = Settings()
