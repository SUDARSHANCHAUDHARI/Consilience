import os
import json
import asyncio
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.config import COUNCIL_MODELS, CHAIRMAN_MODEL, MODEL_DISPLAY_NAMES, CONVERSATIONS_DIR
from backend.api_clients import APIClient

app = FastAPI(title="Consilience")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Path(CONVERSATIONS_DIR).mkdir(parents=True, exist_ok=True)

class QueryRequest(BaseModel):
    query: str

class ModelResponse(BaseModel):
    model: str
    model_name: str
    response: str

class ReviewResponse(BaseModel):
    model: str
    model_name: str
    review: str

class CouncilResponse(BaseModel):
    query: str
    stage1_responses: List[ModelResponse]
    stage2_reviews: List[ReviewResponse]
    stage3_final: str
    timestamp: str

@app.post("/api/query", response_model=CouncilResponse)
async def process_query(request: QueryRequest):
    query = request.query
    timestamp = datetime.now().isoformat()
    try:
        print(f"Stage 1: Getting responses from {len(COUNCIL_MODELS)} models...")
        stage1_responses = await get_initial_responses(query)
        print(f"Stage 2: Getting reviews from {len(COUNCIL_MODELS)} models...")
        stage2_reviews = await get_reviews(query, stage1_responses)
        print("Stage 3: Chairman synthesizing final answer...")
        stage3_final = await get_final_answer(query, stage1_responses, stage2_reviews)
        conversation_data = {
            "query": query,
            "stage1_responses": [r.model_dump() for r in stage1_responses],
            "stage2_reviews": [r.model_dump() for r in stage2_reviews],
            "stage3_final": stage3_final,
            "timestamp": timestamp,
        }
        save_conversation(conversation_data)
        return CouncilResponse(
            query=query,
            stage1_responses=stage1_responses,
            stage2_reviews=stage2_reviews,
            stage3_final=stage3_final,
            timestamp=timestamp,
        )
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def get_initial_responses(query: str) -> List[ModelResponse]:
    async def get_response(model: str) -> ModelResponse:
        try:
            response = await APIClient.call_model(
                model=model,
                prompt=query,
                system="You are a helpful AI assistant. Provide a thoughtful, well-reasoned answer to the user's question."
            )
            return ModelResponse(
                model=model,
                model_name=MODEL_DISPLAY_NAMES.get(model, model),
                response=response
            )
        except Exception as e:
            print(f"Error with {model}: {str(e)}")
            return ModelResponse(
                model=model,
                model_name=MODEL_DISPLAY_NAMES.get(model, model),
                response=f"[Error: {str(e)}]"
            )
    responses = list(await asyncio.gather(*[get_response(model) for model in COUNCIL_MODELS]))
    return responses

async def get_reviews(query: str, responses: List[ModelResponse]) -> List[ReviewResponse]:
    async def get_review(model: str) -> ReviewResponse:
        anonymized_responses = "\n\n".join([
            f"Response {i+1}:\n{r.response}"
            for i, r in enumerate(responses)
        ])
        prompt = f"""Original Question: {query}

Here are the responses from other council members (anonymized):

{anonymized_responses}

Please review these responses. Rank them by quality (1 being best, {len(responses)} being worst) and provide brief reasoning for your rankings. Be objective and fair in your assessment."""
        try:
            review = await APIClient.call_model(
                model=model,
                prompt=prompt,
                system="You are an objective reviewer. Analyze the quality, accuracy, and insight of the provided responses."
            )
            return ReviewResponse(
                model=model,
                model_name=MODEL_DISPLAY_NAMES.get(model, model),
                review=review
            )
        except Exception as e:
            print(f"Error with {model} review: {str(e)}")
            return ReviewResponse(
                model=model,
                model_name=MODEL_DISPLAY_NAMES.get(model, model),
                review=f"[Error: {str(e)}]"
            )
    reviews = list(await asyncio.gather(*[get_review(model) for model in COUNCIL_MODELS]))
    return reviews

async def get_final_answer(query: str, responses: List[ModelResponse], reviews: List[ReviewResponse]) -> str:
    all_responses = "\n\n".join([
        f"{r.model_name}:\n{r.response}"
        for r in responses
    ])
    all_reviews = "\n\n".join([
        f"{r.model_name}'s Review:\n{r.review}"
        for r in reviews
    ])
    prompt = f"""Original Question: {query}

COUNCIL RESPONSES:
{all_responses}

COUNCIL REVIEWS:
{all_reviews}

As the Chairman of the Council, synthesize the best insights from all council members into a comprehensive, accurate, and well-reasoned final answer. Draw from the strongest points across all responses, and address any conflicts or contradictions."""
    final_answer = await APIClient.call_model(
        model=CHAIRMAN_MODEL,
        prompt=prompt,
        system="You are the Chairman of the Council. Your role is to synthesize the collective wisdom of all council members into the best possible answer."
    )
    return final_answer

def save_conversation(data: Dict[str, Any]):
    timestamp = data["timestamp"].replace(":", "-")
    filename = f"{CONVERSATIONS_DIR}/conversation_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "models": len(COUNCIL_MODELS)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
