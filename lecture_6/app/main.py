"""
Main module.
"""


from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# Create app
app = FastAPI()

@app.get("/")
def read_root():
    html_content = "<h2>Hello Docker!</h2>"
    return HTMLResponse(content=html_content)


@app.get("/healthcheck")
async def healthcheck() -> dict:
    return {"status": "ok"}