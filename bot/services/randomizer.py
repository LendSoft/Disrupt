import random
from dataclasses import dataclass

from bot.audit import AUDIENCES
from bot.product import PRODUCTS
from bot.activity import ACTIVITIES
from bot.ogran import OGRANS

@dataclass(frozen=True)
class RoundPack:
    audit: str
    product: str
    activity: str
    ogran: str

def pick_base() -> RoundPack:
    return RoundPack(
        audit=random.choice(AUDIENCES),
        product=random.choice(PRODUCTS),
        activity=random.choice(ACTIVITIES),
        ogran="—",
    )

def pick_ogran() -> str:
    return random.choice(OGRANS)
