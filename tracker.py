CATEGORY_KEYWORDS = {
    "groceries": ["walmart", "kroger", "grocery", "whole foods"],
    "dining": ["restaurant", "doordash", "ubereats", "cafe"],
    "subscription": ["netflix", "spotify", "amazon prime", "subscription"],
    # ... extend
}

def smart_categorize(description):
    desc_lower = description.lower()
    for cat, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in desc_lower for kw in keywords):
            return cat
    # Fallback: ask LLM (optional)
    return "other"