from typing import Dict, Any
import httpx

class HttpTool:
    """Simple http_request tool using httpx. Only GET supported in M1."""
    name = "http_request"
    def run(self, inp: Dict[str, Any]) -> Dict[str, Any]:
        # expected input: {'url': 'https://...'} or context with 'goal' containing a url
        url = None
        if isinstance(inp, dict) and "url" in inp:
            url = inp["url"]
        elif isinstance(inp, dict) and "goal" in inp:
            # naive extraction: if 'http' substring present
            g = inp["goal"]
            for token in g.split():
                if token.startswith("http://") or token.startswith("https://"):
                    url = token
                    break
        if not url:
            raise ValueError("no_url_provided")
        # perform simple GET
        with httpx.Client(timeout=10.0) as client:
            r = client.get(url)
            return {"status_code": r.status_code, "text_preview": r.text[:1000]}
