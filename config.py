import os
import json

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".hrflow")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

DEFAULT_CONFIG = {
    "database": {
        "host": "localhost",
        "port": 5432,
        "name": "hrflow",
        "user": "postgres",
        "password": "postgres"
    },
    "sms_api": {
        "base_url": "https://api.onbuka.com/v3",
        "api_key": "",
        "api_pwd": "",
        "app_id": "",
        "sender_id": "HRFlow",
        "enabled": False
    },
    "kpi": {
        "weight_tasks": 40,
        "weight_attendance": 30,
        "weight_punctuality": 30,
        "prime_threshold": 70,
        "prime_percentage": 10
    },
    "company": {
        "name": "Mon Entreprise",
        "address": "",
        "phone": "",
        "logo_path": ""
    },
    "theme": "dark",
    "work_start_hour": 8,
    "work_start_minute": 0,
    "work_hours_per_day": 8,
    "onboarding_done": False
}


def ensure_config_dir():
    os.makedirs(CONFIG_DIR, exist_ok=True)


def load_config():
    ensure_config_dir()
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            saved = json.load(f)
        config = DEFAULT_CONFIG.copy()
        for key, val in saved.items():
            if isinstance(val, dict) and key in config and isinstance(config[key], dict):
                config[key].update(val)
            else:
                config[key] = val
        return config
    return DEFAULT_CONFIG.copy()


def save_config(config):
    ensure_config_dir()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def get_db_url(config=None):
    if config is None:
        config = load_config()
    db = config["database"]
    return f"postgresql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['name']}"
