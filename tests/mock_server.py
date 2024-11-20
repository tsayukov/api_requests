"""Mock server for testing."""

from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def root():
    return {"success": True}
