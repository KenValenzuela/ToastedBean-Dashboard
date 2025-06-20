# db/category_map.py

CATEGORY_MAP = {
    "iced coffee": "Coffee",
    "cold brew": "Coffee",
    "espresso": "Espresso",
    "espresso basics": "Espresso",
    "matcha latte": "Matcha",
    "build your own energy": "Energy",
    "crochet goods": "Merch",
    "banana puddin latte": "Specialty Espresso",
    "cinnamoney": "Specialty Espresso",
}

def standardize_category(cat: str) -> str:
    if not isinstance(cat, str):
        return "Uncategorized"
    cat_clean = cat.strip().lower()
    return CATEGORY_MAP.get(cat_clean, cat_clean.title())
