from fastapi import FastAPI
from llm_engine import get_llm_responses
from utils import calculate_agreement
from trust_engine import detect_hallucination, calculate_trust_score
from rag_system import get_wikipedia_evidence
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS (frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "TrustGuard AI Backend Running"}


@app.post("/ask")
def ask_question(question: str):

    # 🔹 Step 1: Get responses from all LLMs
    responses = get_llm_responses(question)

    # 🔹 Step 2: Agreement (semantic similarity)
    agreement = calculate_agreement(responses)

    # 🔹 Step 3: Hallucination detection
    hallucination = detect_hallucination(
        agreement["agreement_percentage"]
    )

    # 🔹 Step 4: Evidence (RAG)
    evidence = get_wikipedia_evidence(question)

    # 🔹 Step 5: Trust score
    trust_score = calculate_trust_score(
        agreement["agreement_percentage"],
        hallucination,
        evidence
    )

    # 🔹 Step 6: Final Answer (best meaningful answer)
    valid_answers = [
        v for v in responses.values()
        if v and v != "Model not available"
    ]

    final_answer = max(valid_answers, key=len) if valid_answers else "No answer"

    # 🔥 Step 7: Verification (NEW)
    if evidence["evidence"] != "No evidence found":
        verification = "✔ Verified"
    else:
        verification = "❌ Not Verified"

    # 🔥 Step 8: Best Model Detection (NEW)
    best_model = None

    for model, answer in responses.items():
        if answer == final_answer:
            best_model = model
            break

    # fallback (if no exact match)
    if not best_model:
        best_model = list(responses.keys())[0]

    # 🔹 Final Response
    return {
        "question": question,
        "responses": responses,
        "agreement_analysis": agreement,
        "hallucination_risk": hallucination,
        "evidence": evidence,
        "verification": verification,   # ✅ NEW
        "best_model": best_model,       # ✅ NEW
        "final_answer": final_answer,
        "trust_score": trust_score
    }