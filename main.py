"""
Doctor Voice Agent - Twilio + OpenAI Realtime API
Full phone call system (inbound)

Based on official Twilio + OpenAI Realtime samples, customized for medical use case.
"""

import os
import json
import base64
import asyncio
import logging
from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.websockets import WebSocketDisconnect
from twilio.twiml.voice_response import VoiceResponse, Connect
from dotenv import load_dotenv
import websockets
from openai import AsyncOpenAI

from system_prompt import SYSTEM_PROMPT
from tools.appointment import get_available_slots, book_appointment, cancel_appointment, list_appointments
from tools.web_search import search_web
from tools.knowledge import query_knowledge_base

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DoctorAgent")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PORT = int(os.getenv("PORT", 5050))
PUBLIC_URL = os.getenv("PUBLIC_URL", "")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is required")

app = FastAPI(title="Doctor Voice Agent")
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

TOOLS = [
    {
        "type": "function",
        "name": "get_available_slots",
        "description": "Get available appointment slots for a specific date (YYYY-MM-DD)",
        "parameters": {
            "type": "object",
            "properties": {
                "date": {"type": "string", "description": "Date in YYYY-MM-DD format"},
                "duration_minutes": {"type": "integer", "description": "Duration in minutes", "default": 30}
            },
            "required": ["date"]
        }
    },
    {
        "type": "function",
        "name": "book_appointment",
        "description": "Book a new appointment for the patient",
        "parameters": {
            "type": "object",
            "properties": {
                "patient_name": {"type": "string"},
                "phone": {"type": "string"},
                "slot": {"type": "string", "description": "Full datetime e.g. 2026-09-21 10:30"},
                "reason": {"type": "string", "default": "General consultation"}
            },
            "required": ["patient_name", "phone", "slot"]
        }
    },
    {
        "type": "function",
        "name": "cancel_appointment",
        "description": "Cancel an existing appointment",
        "parameters": {
            "type": "object",
            "properties": {
                "phone": {"type": "string"},
                "slot": {"type": "string", "description": "Optional specific slot"}
            },
            "required": ["phone"]
        }
    },
    {
        "type": "function",
        "name": "list_appointments",
        "description": "List appointments for a phone number",
        "parameters": {
            "type": "object",
            "properties": {
                "phone": {"type": "string"}
            },
            "required": ["phone"]
        }
    },
    {
        "type": "function",
        "name": "search_web",
        "description": "Search the web for general health information (never for diagnosis or medicine)",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string"}
            },
            "required": ["query"]
        }
    },
    {
        "type": "function",
        "name": "query_knowledge_base",
        "description": "Search the clinic knowledge base for information about timings, doctors, policies etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string"}
            },
            "required": ["query"]
        }
    }
]


async def execute_tool(name: str, arguments: dict) -> str:
    try:
        if name == "get_available_slots":
            return get_available_slots(
                arguments.get("date"),
                arguments.get("duration_minutes", 30)
            )
        elif name == "book_appointment":
            return book_appointment(
                arguments.get("patient_name"),
                arguments.get("phone"),
                arguments.get("slot"),
                arguments.get("reason", "General consultation")
            )
        elif name == "cancel_appointment":
            return cancel_appointment(
                arguments.get("phone"),
                arguments.get("slot")
            )
        elif name == "list_appointments":
            return list_appointments(arguments.get("phone"))
        elif name == "search_web":
            return await search_web(arguments.get("query"))
        elif name == "query_knowledge_base":
            return query_knowledge_base(arguments.get("query"))
        else:
            return f"Unknown tool: {name}"
    except Exception as e:
        logger.error(f"Tool error {name}: {e}")
        return f"Error executing {name}: {str(e)}"


@app.get("/", response_class=HTMLResponse)
async def index_page():
    return """
    <html>
        <head><title>Doctor Voice Agent</title></head>
        <body style="font-family: sans-serif; max-width: 700px; margin: 40px auto; padding: 20px;">
            <h1>Doctor Voice Agent</h1>
            <p>Twilio + OpenAI Realtime API</p>
            <p>Status: <strong style="color: green;">Running</strong></p>
            <p>Webhook URL for Twilio: <code>/incoming-call</code></p>
            <p>Make sure your PUBLIC_URL is set and ngrok is running.</p>
        </body>
    </html>
    """


@app.api_route("/incoming-call", methods=["GET", "POST"])
async def handle_incoming_call(request: Request):
    response = VoiceResponse()
    response.say("Connecting you to Dr. Aisha, please wait a moment.", voice="Polly.Amy")
    connect = Connect()
    connect.stream(url=f"wss://{request.url.hostname}/media-stream")
    response.append(connect)
    return HTMLResponse(content=str(response), media_type="application/xml")


@app.websocket("/media-stream")
async def media_stream(websocket: WebSocket):
    await websocket.accept()
    logger.info("Twilio client connected")

    openai_ws = await websockets.connect(
        "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-12-17",
        extra_headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "OpenAI-Beta": "realtime=v1"
        }
    )
    logger.info("Connected to OpenAI Realtime API")

    stream_sid = None

    async def receive_from_twilio():
        nonlocal stream_sid
        try:
            async for message in websocket.iter_text():
                data = json.loads(message)
                if data["event"] == "media":
                    audio_append = {
                        "type": "input_audio_buffer.append",
                        "audio": data["media"]["payload"]
                    }
                    await openai_ws.send(json.dumps(audio_append))
                elif data["event"] == "start":
                    stream_sid = data["start"]["streamSid"]
                    logger.info(f"Stream started: {stream_sid}")
                elif data["event"] == "stop":
                    logger.info("Stream stopped")
                    break
        except WebSocketDisconnect:
            logger.info("Twilio disconnected")
        except Exception as e:
            logger.error(f"Error in receive_from_twilio: {e}")
        finally:
            await openai_ws.close()

    async def send_to_twilio():
        nonlocal stream_sid
        try:
            async for openai_message in openai_ws:
                response = json.loads(openai_message)
                if response.get("type") == "session.created":
                    session_update = {
                        "type": "session.update",
                        "session": {
                            "turn_detection": {"type": "server_vad"},
                            "input_audio_format": "g711_ulaw",
                            "output_audio_format": "g711_ulaw",
                            "voice": "alloy",
                            "instructions": SYSTEM_PROMPT,
                            "modalities": ["text", "audio"],
                            "temperature": 0.6,
                            "tools": TOOLS
                        }
                    }
                    await openai_ws.send(json.dumps(session_update))
                    logger.info("Session configured with Doctor system prompt + tools")
                elif response.get("type") == "response.audio.delta" and response.get("delta"):
                    try:
                        audio_payload = base64.b64encode(
                            base64.b64decode(response["delta"])
                        ).decode("utf-8")
                        await websocket.send_json({
                            "event": "media",
                            "streamSid": stream_sid,
                            "media": {"payload": audio_payload}
                        })
                    except Exception as e:
                        logger.error(f"Error sending audio to Twilio: {e}")
                elif response.get("type") == "response.function_call_arguments.done":
                    function_name = response.get("name")
                    call_id = response.get("call_id")
                    arguments = json.loads(response.get("arguments", "{}"))
                    logger.info(f"Tool call: {function_name} | {arguments}")
                    result = await execute_tool(function_name, arguments)
                    await openai_ws.send(json.dumps({
                        "type": "conversation.item.create",
                        "item": {
                            "type": "function_call_output",
                            "call_id": call_id,
                            "output": result
                        }
                    }))
                    await openai_ws.send(json.dumps({"type": "response.create"}))
                elif response.get("type") == "error":
                    logger.error(f"OpenAI error: {response}")
        except Exception as e:
            logger.error(f"Error in send_to_twilio: {e}")

    await asyncio.gather(receive_from_twilio(), send_to_twilio())


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
