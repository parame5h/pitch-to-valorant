from fastapi import FastAPI
from pydantic import BaseModel
from agents import jett, viper, reyna, sova, sage
import asyncio
from tools import utils
import schemas
from fastapi.responses import StreamingResponse
import json
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")



async def event_streamer(pitch: str, keywords: str):
    group1 = [
        asyncio.to_thread(jett.ask_jett, pitch, keywords),
        asyncio.to_thread(viper.ask_viper, pitch, keywords),
    ]
    results = {}
    for coro in asyncio.as_completed(group1):
        result = await coro
        key = result["agent"].lower()
        results[key] = result
        yield f"data: {json.dumps(results[key])}\n\n"

    await asyncio.sleep(15)  # Wait for 15 seconds before asking Reyna and Sova to avoid rate limiting
    group2 = [
        asyncio.to_thread(reyna.ask_reyna, pitch, keywords),
        asyncio.to_thread(sova.ask_sova, pitch, keywords),
    ]
    for coro in asyncio.as_completed(group2):
        result = await coro
        key = result["agent"].lower()
        results[key] = result
        yield f"data: {json.dumps(results[key])}\n\n"
    
    sage_result = await asyncio.to_thread(sage.ask_sage, results.get('jett'), results.get('viper'), results.get('reyna'), results.get('sova'))
    yield f"data: {json.dumps(sage_result)}\n\n"

@app.post("/analyze")
async def analyze_pitch(pitch_request: schemas.PitchRequest):
    pitch = pitch_request.pitch
    keywords = utils.extract_keywords(pitch)
    return StreamingResponse(event_streamer(pitch, keywords), media_type="text/event-stream")
        