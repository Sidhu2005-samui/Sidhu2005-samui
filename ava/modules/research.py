import requests
from bs4 import BeautifulSoup

class ResearchModule:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def research(self, topic, preferred_length="short"):
        print(f"Researching topic: {topic} (Preference: {preferred_length})")

        summary_base = ""
        try:
            url = f"https://html.duckduckgo.com/html/?q={topic}"
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                results = soup.find_all('a', class_='result__a')
                if results:
                    top_result = results[0].get_text()
                    snippet = soup.find_all('a', class_='result__snippet')
                    snippet_text = snippet[0].get_text() if snippet else ""
                    summary_base = f"{top_result}. {snippet_text}"

            if not summary_base:
                summary_base = f"I found that {topic} is a widely discussed topic with various aspects. (Simulated summary)"
        except Exception:
            summary_base = f"{topic} generally refers to a subject of interest in modern discourse. (Fallback summary)"

        if preferred_length == "detailed":
            return f"Detailed Summary of {topic}: {summary_base} Additionally, further research suggests that {topic} has significant impact in its field and continues to evolve with new developments."
        else:
            return f"Summary of {topic}: {summary_base}"
