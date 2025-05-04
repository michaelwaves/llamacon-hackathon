import re
from typing import List, Dict, Optional
from duckduckgo_search import ddg  # pip install duckduckgo-search

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

def filter_results_by_keywords(results: List[Dict], keywords: List[str]) -> List[Dict]:
    filtered = []
    for result in results:
        text = f"{result.get('title', '')} {result.get('body', '')}"
        if any(re.search(keyword, text, re.IGNORECASE) for keyword in keywords):
            filtered.append(result)
    return filtered

def screen_person_for_pep_and_adverse_media(
    given_name: Optional[str], 
    surname: Optional[str], 
    occupation: Optional[str], 
    max_results: int = 30
) -> Dict[str, List[Dict]]:
    """
    Screen a person for PEP and adverse media based on their name and occupation.
    Returns a dictionary with filtered results.
    """
    query_parts = [given_name, surname, occupation]
    base_query = " ".join(filter(None, query_parts))
    full_query = base_query + " " + " ".join(ADVERSE_MEDIA_KEYWORDS)

    try:
        search_results = ddg(full_query, max_results=max_results)

        if not search_results:
            return {"pep": [], "adverseMedia": []}

        pep_results = filter_results_by_keywords(search_results, PEP_KEYWORDS)
        adverse_results = filter_results_by_keywords(search_results, ADVERSE_MEDIA_KEYWORDS)

        return {
            "pep": pep_results,
            "adverseMedia": adverse_results
        }

    except Exception as e:
        raise RuntimeError(f"Error during screening: {e}")
