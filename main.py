"""
main.py
--------
Test script for MedicalRAGEngine.
"""

# --- Load environment variables ---
from dotenv import load_dotenv
import os

load_dotenv(override=True)  # ensures .env variables are loaded

# Optional: check if key is loaded
if not os.environ.get("ANTHROPIC_API_KEY"):
    print("⚠ WARNING: ANTHROPIC_API_KEY not found! Set it in .env or environment variables.")
else:
    print("✅ ANTHROPIC_API_KEY loaded successfully!")

# --- Import engine ---
from rag_engine import MedicalRAGEngine

def main():
    # Initialize the RAG engine
    engine = MedicalRAGEngine()

    print("\n✅ Medical RAG Engine is ready!\n")

    # Simple loop to test queries
    while True:
        query = input("Enter your medical question (or 'exit' to quit): ").strip()
        if query.lower() in ["exit", "quit"]:
            print("Exiting...")
            break

        result = engine.generate_answer(query)
        print("\n--- Answer ---")
        print(result["answer"])
        print("\n--- Sources ---")
        print(result["sources"])
        print("\n--- Context Chunks ---")
        for i, chunk in enumerate(result["context_chunks"], 1):
            print(f"\nChunk {i}:\n{chunk[:500]}...")  # print first 500 chars
        print("\n============================\n")

if __name__ == "__main__":
    main()