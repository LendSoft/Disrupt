import json
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


def _get_bool(name: str, default: bool = False) -> bool:
    v = os.getenv(name)
    if v is None:
        return default
    return v.strip().lower() in ("1", "true", "yes", "y", "on")


def _get_json(name: str, default):
    v = os.getenv(name)
    if not v:
        return default
    return json.loads(v)


@dataclass(frozen=True)
class Settings:
    bot_token: str

    admins: set[int]

    gigachat_credentials: str
    gigachat_scope: str
    gigachat_verify_ssl: bool

    db_users_path: str
    db_teams_path: str
    db_rounds_path: str
    db_solutions_path: str
    db_moderators_path: str


def load_settings() -> Settings:
    bot_token = os.environ["BOT_TOKEN"]

    admins_raw = _get_json("ADMINS", [])
    admins = set(int(x) for x in admins_raw)

    return Settings(
        bot_token=bot_token,
        admins=admins,
        gigachat_credentials=os.environ.get("GIGACHAT_CREDENTIALS", ""),
        gigachat_scope=os.environ.get("GIGACHAT_SCOPE", "GIGACHAT_API_PERS"),
        gigachat_verify_ssl=_get_bool("GIGACHAT_VERIFY_SSL", False),
        db_users_path=os.environ.get("DB_USERS_PATH", "bot/data/users.json"),
        db_teams_path=os.environ.get("DB_TEAMS_PATH", "bot/data/teams.json"),
        db_rounds_path=os.environ.get("DB_ROUNDS_PATH", "bot/data/rounds.json"),
        db_solutions_path=os.environ.get("DB_SOLUTIONS_PATH", "bot/data/solutions.json"),
        db_moderators_path=os.environ.get("DB_MODERATORS_PATH", "bot/data/moderators.json"),
    )
