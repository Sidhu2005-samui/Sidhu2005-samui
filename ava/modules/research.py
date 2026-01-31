import urllib.request
import urllib.parse
import json
import re

class ResearchModule:
    def __init__(self):
        self.user_agent = 'AvaAssistant/1.0 (Personal AI Assistant)'

    def search(self, query):
        try:
            # Using Wikipedia REST API for reliable, real-world research
            formatted_query = query.strip().replace(' ', '_')
            encoded_query = urllib.parse.quote(formatted_query)
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_query}"

            req = urllib.request.Request(url, headers={'User-Agent': self.user_agent})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                if 'extract' in data:
                    return data['extract']
                return data.get('description', f"I found some info on {query} but couldn't get a summary.")
        except Exception as e:
            # If Wikipedia fails (e.g. page not found), try a generic message
            return f"I researched '{query}' but couldn't find a definitive summary. It's a broad topic that often appears in various contexts."

    def summarize(self, text, max_sentences=2):
        if not text:
            return "No information found to summarize."
        # Simple sentence splitter
        sentences = re.split(r'(?<=[.!?])\s+', text)
        summary = ' '.join(sentences[:max_sentences]).strip()
        return summary
