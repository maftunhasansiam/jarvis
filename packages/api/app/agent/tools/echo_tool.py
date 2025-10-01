from typing import Dict, Any

class EchoTool:
    """A trivial tool that echoes input back."""
    name = "echo"
    def run(self, inp: Dict[str, Any]) -> Dict[str, Any]:
        # Accept either {'message': '...'} or arbitrary dicts
        if isinstance(inp, dict) and "message" in inp:
            return {"echo": inp["message"]}
        return {"echo": inp}
