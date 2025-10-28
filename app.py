from flask import Flask, request, jsonify
import os
import sys 
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from typing_extensions import List, TypedDict
from langgraph.graph import START, StateGraph
from langchain_community.vectorstores import Chroma 
from langchain.chat_models import init_chat_model

VECTOR_DB_PATH = "./vector_db_manual"
EMBEDDING_MODEL = "models/embedding-001"

if "GOOGLE_API_KEY" not in os.environ:
    print("ERROR: GOOGLE_API_KEY environment variable not set.")
    sys.exit(1)

app = Flask(__name__)
try:
    embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)

    if not os.path.exists(VECTOR_DB_PATH):
        sys.exit(1)
    vector_store = Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings
    )
    retriever = vector_store.as_retriever() 
    
    llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai")




except Exception as e:
    import traceback
    traceback.print_exc()
    sys.exit(1)

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str

def retrieve(state: State):
    retrieved_docs = retriever.invoke(state["question"])
    return {"context": retrieved_docs}

template = """Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer. Keep the answer as concise as possible.
Always say "thanks for asking!" at the end of the answer.

{context}

Question: {question}

Helpful Answer:"""

prompt = PromptTemplate.from_template(template)

def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    prompt_input = {"question": state["question"], "context": docs_content}
    formatted_prompt = prompt.invoke(prompt_input)
    response = llm.invoke(formatted_prompt)
    answer_content = response.content if hasattr(response, 'content') else str(response)
    return {"answer": answer_content}

graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()

@app.route('/api/ask', methods=['POST'])
def ask_question():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    query = data.get('question')

    if not query:
        return jsonify({"error": "Missing 'question' in request body"}), 400


    try:
        result = graph.invoke({"question": query})
        response = {
            "answer": result['answer'],
        }
        return jsonify(response)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Failed to process query", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)