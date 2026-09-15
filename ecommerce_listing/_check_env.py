import importlib.util, sys
def have(mod):
    return importlib.util.find_spec(mod) is not None
for m in ["playwright", "pandas", "openpyxl", "fastapi", "openai", "dotenv"]:
    print(m, "OK" if have(m) else "MISSING")
