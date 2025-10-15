import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq

app = FastAPI()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

class UserRequest(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"Status": "O cérebro da Aurora está online na Vercel, com o poder da Groq!"}

@app.post("/api/generate-response")
async def generate_response(request: UserRequest):
    if not client.api_key:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY não foi configurada no servidor.")

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": """Você é Aurora, uma assistente virtual em português do Brasil. Seja concisa e direta. Para pedidos que envolvem abrir programas ou sites, responda APENAS com um JSON. Exemplos de JSON: {"action": "open_app", "target": "spotify"}, {"action": "open_url", "target": "https://google.com"}. Para outras perguntas, responda normalmente."""
                },
                {
                    "role": "user",
                    "content": request.text,
                }
            ],
            model="llama3-8b-8192",
        )

        response_text = chat_completion.choices[0].message.content
        print(f"Prompt: '{request.text}' -> Resposta: '{response_text}'")
        return {"response": response_text}

    except Exception as e:
        print(f"Ocorreu um erro com a API da Groq: {e}")
        raise HTTPException(status_code=503, detail=f"Erro de comunicação com a API da IA: {e}")