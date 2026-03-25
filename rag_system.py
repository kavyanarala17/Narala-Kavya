import requests


def clean_query(query):
    query = query.lower()

    remove_words = ["who", "what", "is", "the", "of", "?", "did"]
    words = query.split()

    cleaned = [word for word in words if word not in remove_words]

    return " ".join(cleaned)


def get_wikipedia_evidence(query):
    try:
        headers = {
            "User-Agent": "TrustGuardAI/1.0"
        }

        # ✅ Clean query
        cleaned_query = clean_query(query)

        # ✅ STEP 1: Search Wikipedia
        search_url = "https://en.wikipedia.org/w/api.php"
        search_params = {
            "action": "query",
            "list": "search",
            "srsearch": cleaned_query,
            "format": "json"
        }

        search_res = requests.get(search_url, params=search_params, headers=headers)

        if search_res.status_code != 200:
            return {
                "source": "Wikipedia",
                "evidence": "Search request failed"
            }

        search_data = search_res.json()

        if not search_data.get("query") or not search_data["query"]["search"]:
            return {
                "source": "Wikipedia",
                "evidence": "No evidence found"
            }

        # ✅ Get best matching title
        title = search_data["query"]["search"][0]["title"]

        # ✅ STEP 2: Get summary
        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
        summary_res = requests.get(summary_url, headers=headers)

        if summary_res.status_code != 200:
            return {
                "source": "Wikipedia",
                "evidence": "Summary fetch failed"
            }

        data = summary_res.json()

        return {
            "source": "Wikipedia",
            "evidence": data.get("extract", "No summary available")
        }

    except Exception as e:
        return {
            "source": "Wikipedia",
            "evidence": f"Error: {str(e)}"
        }