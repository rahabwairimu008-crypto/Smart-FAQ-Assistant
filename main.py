"""
main.py
Smart Grammar-Based FAQ Assistant - DeKUT SCIT
Orchestrates: input -> preprocess -> parse -> classify -> respond -> output

Run interactively:   python3 main.py
Run batch test:      python3 main.py --batch
"""

import sys
from parser import parse_query
from classifier import classify, CATEGORIES
from response import get_response


def handle_query(text: str) -> dict:
    tree, tokens = parse_query(text)
    category = classify(text)
    resp = get_response(text, category)

    return {
        "query": text,
        "tokens": tokens,
        "parsed": tree is not None,
        "tree": tree,
        "category": category,
        "category_label": CATEGORIES.get(category, {}).get("label", "Unknown"),
        "response": resp["answer"],
        "answer_source": resp["source"],       # exact | fuzzy | category
        "matched_question": resp["matched_question"],
    }


def print_result(result: dict):
    print("-" * 60)
    print(f"Query      : {result['query']}")
    print(f"Grammar    : {'VALID (matched CFG)' if result['parsed'] else 'no syntactic match'}")
    print(f"Category   : {result['category_label']} ({result['category']})")
    print(f"Answer src : {result['answer_source']}"
          + (f"  (matched: '{result['matched_question']}')" if result['matched_question'] else ""))
    print(f"Response   : {result['response']}")
    if result["tree"]:
        print("Parse tree :")
        print(result["tree"])


def run_interactive():
    print("Smart FAQ Assistant - DeKUT SCIT (type 'exit' to quit)\n")
    while True:
        try:
            text = input("Ask a question: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if text.lower() in ("exit", "quit"):
            break
        if not text:
            continue
        print_result(handle_query(text))


def run_batch():
    sample_queries = [
        "How do I register for my courses?",
        "How do I download my fee statement?",
        "What happens if I miss an examination?",
        "Can I change my project supervisor?",
        "How do I apply for deferment?",
        "What documents are required for graduation clearance?",
        "Who is the dean?",
        "How do I apply for internal attachment?",
    ]
    for q in sample_queries:
        print_result(handle_query(q))


if __name__ == "__main__":
    if "--batch" in sys.argv:
        run_batch()
    else:
        run_interactive()