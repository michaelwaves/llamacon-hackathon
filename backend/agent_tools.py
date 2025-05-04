import re
from typing import List, Dict, Optional
from duckduckgo_search import DDGS  # pip install duckduckgo-search

def print_banner(title: str):
    print("\n" + "=" * 40)
    print(f"{title.center(40)}")
    print("=" * 40 + "\n")

# Keyword lists
DOMESTIC_POSITIONS = [
    "Governor General", "Lieutenant Governor", "Head of Government",
    "Member of the Senate", "Member of the House of Commons", "Member of a Legislature",
    "Deputy Minister", "Ambassador", "Attaché", "Counsellor",
    "Military Officer", "General", "President of a corporation",
    "Head of a government agency", "Judge of an appellate court",
    "Leader of a political party", "Mayor", "Reeve"
]

FOREIGN_POSITIONS = [
    "Head of State", "Head of Government", "Member of the executive council",
    "Member of a legislature", "Deputy Minister", "Ambassador", "Attaché",
    "Counsellor", "Military Officer", "General",
    "President of a state-owned company", "State-owned bank",
    "Head of a government agency", "Judge of a supreme court",
    "Judge of a constitutional court", "Judge of a court of last resort",
    "Leader of a political party"
]

CUSTOM_POSITIONS = ["president", "prime minister", "councilor", "representative"]

PEP_KEYWORDS = DOMESTIC_POSITIONS + FOREIGN_POSITIONS + CUSTOM_POSITIONS

ADVERSE_MEDIA_KEYWORDS = [
    "launder", "lawsuit", "scandal", "fraud", "illegal", "criminal", "conviction",
    "guilt", "arrest", "testify", "corrupt", "accuse", "kickback", "investigate",
    "bribe", "unethical", "ponzi", "terror", "drug", "blanchiment", "poursuite",
    "scandale", "fraude", "illégal", "criminel", "condamnation", "culpabilité",
    "arrestation", "témoignage", "corrompu", "accusation", "pots-de-vin", "enquête",
    "pot-de-vin", "éthique", "ponzi", "terreur", "terroriste", "stupéfiants", "drogue"
]

# Shared helper
def _search_duckduckgo(query: str, max_results: int = 30) -> List[Dict]:
    return DDGS().text(keywords=query, max_results=max_results) or []

def _filter_results_by_keywords(results: List[Dict], keywords: List[str]) -> List[Dict]:
    filtered = []
    for result in results:
        text = f"{result.get('title', '')} {result.get('body', '')}"
        if any(re.search(keyword, text, re.IGNORECASE) for keyword in keywords):
            filtered.append(result)
    return filtered

# Main screening functions
def screen_for_pep(
    given_name: Optional[str],
    surname: Optional[str],
    occupation: Optional[str],
    max_results: int = 30
) -> List[Dict]:
    query = " ".join(filter(None, [given_name, surname, occupation]))
    results = _search_duckduckgo(query, max_results=max_results)
    return _filter_results_by_keywords(results, PEP_KEYWORDS)

def screen_for_adverse_media(
    given_name: Optional[str],
    surname: Optional[str],
    occupation: Optional[str],
    max_results: int = 5
) -> List[Dict]:
    query = " ".join(filter(None, [given_name, surname, occupation])) + " " + " ".join(ADVERSE_MEDIA_KEYWORDS)
    results = _search_duckduckgo(query, max_results=max_results)
    return _filter_results_by_keywords(results, ADVERSE_MEDIA_KEYWORDS)


if __name__  == "__main__":
    res = screen_for_adverse_media("michael",'yu','startup')
    print(res)