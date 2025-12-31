import re

completed_symbol = "💫"

async def isAuthenticated(displayName):
    default = r"‹ \d+ › ASR"
    if re.search(default, displayName):
        return True
    else:
        return False
