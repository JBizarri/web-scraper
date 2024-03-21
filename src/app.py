from fastapi import FastAPI

from .scraper import scraper

app = FastAPI()


@app.post("/seed")
async def seed() -> list[str]:
    result = scraper.run()
    return result
