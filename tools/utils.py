from llm import get_llm



def extract_keywords(pitch: str) -> str:
    llm = get_llm()
    messages = [
        {"role": "system", "content": "Return ONLY a comma-separated list of 4-5 keywords with NO spaces within individual words. Example output: AI, B2B, customer support, automation, small business"},
        {"role": "user", "content": pitch}
    ]
    return llm.invoke(messages).content.strip()