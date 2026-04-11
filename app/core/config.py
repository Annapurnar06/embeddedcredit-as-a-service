from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = ""
    redis_url: str = "redis://localhost:6379/0"
    secret_key: str = ""
    environment: str = "development"
    log_level: str = "INFO"
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Authority boundaries (hard-coded limits)
    bureau_pull_max_per_aadhaar_48h: int = 2
    disbursement_max_amount: int = 500_000
    fee_waiver_max: int = 500
    moratorium_max_months: int = 3
    can_auto_approve: bool = False
    can_disburse_without_human: bool = False

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
