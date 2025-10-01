# Tool registry for M1. Keep it simple: a dict mapping name->tool instance.
from .echo_tool import EchoTool
from .http_tool import HttpTool

registry = {}

# instantiate and register safe tools
registry["echo"] = EchoTool()
registry["http_request"] = HttpTool()

def get(name: str):
    return registry.get(name)
