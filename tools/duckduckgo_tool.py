from ddgs import DDGS


def search_duckduckgo(query, max_results=10) -> list[str]:
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query):
            results.append(r)
            if len(results) >= max_results:
                break
    return results