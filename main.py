from fastapi import FastAPI
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from dotenv import load_dotenv
import uvicorn

from fastapi.middleware.cors import CORSMiddleware



load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # allow all origins (for testing)
    allow_credentials=True,
    allow_methods=["*"],        # allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],        # allow all headers
)
model = ChatOpenAI(model="gpt-4.1")
app=FastAPI()

class QueryRequest(BaseModel):
    url: str
    query: str

@app.post("/ask")
def ask_ai(request: QueryRequest):
    loader = WebBaseLoader(
        request.url,
        header_template={"User-Agent": "Mozilla/5.0"}
    )
    docs = loader.load()
    content = docs[0].page_content if docs else "No content found"

    prompt = PromptTemplate(
        input_variables=["content", "query"],
        template="""
You are an assistant. Use the webpage content to answer.

Webpage:
{content}

Question:
{query}

Answer (if unclear, say 'Not enough information in page'):
""",
    )

    chain = prompt | model
    result = chain.invoke({"content": content, "query": request.query})

    answer = result.content.strip()

    # ✅ Check if answer is valid
    if not answer or "not enough information" in answer.lower():
        return {"answer": "⚠️ No clear answer could be generated from the webpage."}
    return {"answer": answer}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
 