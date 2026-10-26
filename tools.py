"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""
"""
The three FitFindr tools.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str
"""

import re

import config
from generate import generate
from utils.data_loader import load_listings


# ── Tool 1: search_listings ───────────────────────────────────────────────────

_STOPWORDS = {
    "a", "an", "and", "the", "for", "with", "under", "over", "in", "of"
}


def _keywords(text: str) -> set[str]:
    """Lowercase words worth matching on, stopwords and bare numbers removed."""
    words = re.findall(r"[a-z0-9']+", (text or "").lower())
    return {w for w in words if w not in _STOPWORDS and len(w) > 1 and not w.isdigit()}


def _size_tokens(size: str) -> set[str]:
    """Split a size like 'S/M (fits small)' into {'S', 'M'}."""
    cleaned = re.sub(r"\([^)]*\)", " ", size or "")  # drop parentheticals
    parts = [p.strip().upper() for p in cleaned.split("/")]
    return {p for p in parts if p}


def _size_matches(wanted: str | None, listing_size: str) -> bool:
    """True if no size was asked for, the listing is one size, or a token matches exactly."""
    if not wanted:
        return True
    listing_tokens = _size_tokens(listing_size)
    if any(token.startswith("ONE SIZE") for token in listing_tokens):
        return True
    return bool(_size_tokens(wanted) & listing_tokens)


def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search listings by keywords, size, and price ceiling.

    Returns a list of matching listing dicts, best match first, at most
    config.SEARCH_RESULT_LIMIT of them. Returns [] when nothing matches.
    """
    wanted = _keywords(description)
    scored = []

    for listing in load_listings():
        # 1. Filter by price and size
        if max_price is not None and listing["price"] > max_price:
            continue
        if not _size_matches(size, listing["size"]):
            continue

        # 2. Score by keyword overlap. Title and style tags count double.
        title_words = _keywords(listing["title"])
        tag_words = _keywords(" ".join(listing["style_tags"]))
        other_words = _keywords(
            " ".join([listing["description"], listing["category"], " ".join(listing["colors"])])
        )
        score = (
            2 * len(wanted & title_words)
            + 2 * len(wanted & tag_words)
            + len(wanted & other_words)
        )

        # 3. Drop anything scoring zero
        if score > 0:
            scored.append((score, listing))

    # 4. Best match first, capped at the limit
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [listing for _, listing in scored[: config.SEARCH_RESULT_LIMIT]]


# ── Shared helper ─────────────────────────────────────────────────────────────

def _describe_item(item: dict) -> str:
    """Turn a listing dict into lines for a prompt. Skips brand when it's None."""
    lines = [
        f"Title: {item['title']}",
        f"Category: {item['category']}",
        f"Colors: {', '.join(item['colors'])}",
        f"Style: {', '.join(item['style_tags'])}",
        f"Size: {item['size']}",
        f"Condition: {item['condition']}",
        f"Price: ${item['price']:.2f}",
        f"Platform: {item['platform']}",
    ]
    if item.get("brand"):
        lines.append(f"Brand: {item['brand']}")
    return "\n".join(lines)


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

_OUTFIT_SYSTEM = (
    "You are a thrift stylist. Suggest one or two complete outfits built "
    "around the item you're given. Keep it under 120 words. Plain text, "
    "no headings or bullet symbols."
)


def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Suggest one or two outfits for the item. With an empty wardrobe, returns
    general styling advice. Never returns an empty string.
    """
    items = (wardrobe or {}).get("items") or []
    item_text = _describe_item(new_item)

    if not items:
        # Empty wardrobe: general advice instead of failing
        prompt = (
            f"Someone is thinking about buying this thrifted item:\n{item_text}\n\n"
            "They haven't saved any wardrobe pieces yet. Suggest one or two "
            "general outfits built around this item, describing the kinds of "
            "pieces that would pair well with it."
        )
    else:
        wardrobe_lines = "\n".join(
            f"- {w['name']} ({w['category']}; colors: {', '.join(w['colors'])}; "
            f"style: {', '.join(w['style_tags'])})"
            for w in items
        )
        prompt = (
            f"Someone is thinking about buying this thrifted item:\n{item_text}\n\n"
            f"Here is what they already own:\n{wardrobe_lines}\n\n"
            "Suggest one or two outfits that pair the new item with pieces "
            "they already own. Name each wardrobe piece exactly as written above."
        )

    response = generate(prompt, system=_OUTFIT_SYSTEM)

    if not response or not response.strip():
        return f"Try the {new_item['title']} with simple basics in neutral colors."
    return response.strip()


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

_CARD_SYSTEM = (
    "You write captions people post about their thrift finds. Write 2 to 4 "
    "sentences that sound like a real person posting, not a product listing. "
    "Mention the item, its price, and the platform once each. Be specific "
    "about the vibe. At most 3 hashtags."
)


def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a 2-4 sentence caption for the find. If outfit is empty or
    whitespace, returns a message saying so instead of raising.
    """
    if not outfit or not outfit.strip():
        return "No outfit to caption yet. suggest_outfit needs to run first so there's something to write about."

    prompt = (
        f"The find:\n{_describe_item(new_item)}\n\n"
        f"How they're styling it:\n{outfit.strip()}\n\n"
        "Write the caption."
    )

    response = generate(prompt, system=_CARD_SYSTEM)

    if not response or not response.strip():
        return f"Just thrifted the {new_item['title']} for ${new_item['price']:.0f} on {new_item['platform']}."
    return response.strip()