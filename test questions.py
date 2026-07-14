"""
test_all_questions.py
Runs every question in response.py's QUESTION_ANSWERS through the full
pipeline (preprocess -> parse -> classify -> respond) and reports:

  - Grammar parse success rate (how many are syntactically valid per
    the CFG in grammar.py)
  - Answer match source breakdown (exact / fuzzy / category-fallback)
  - A list of any questions that fell through to a generic category
    answer, since those are the ones worth reviewing/improving

This is useful evidence for your project report's "Refactor and
Evaluate" section (the brief asks you to evaluate grammar coverage and
response relevance).

Run with:
    python3 test_all_questions.py
"""

from main import handle_query
from response import QUESTION_ANSWERS


def run_tests():
    questions = list(QUESTION_ANSWERS.keys())
    total = len(questions)

    parsed_count = 0
    source_counts = {"exact": 0, "fuzzy": 0, "category": 0}
    unresolved = []
    fuzzy_matches = []

    for q in questions:
        result = handle_query(q)

        if result["parsed"]:
            parsed_count += 1

        source = result["answer_source"]
        source_counts[source] = source_counts.get(source, 0) + 1

        if source == "category":
            unresolved.append(q)
        elif source == "fuzzy":
            fuzzy_matches.append((q, result["matched_question"]))

    # --- Report ---
    print("=" * 70)
    print("DeKUT SCIT Smart FAQ Assistant -- Full Test Report")
    print("=" * 70)
    print(f"Total questions tested        : {total}")
    print(f"Grammar parse success         : {parsed_count}/{total} "
          f"({parsed_count / total * 100:.1f}%)")
    print()
    print("Answer match source breakdown:")
    for source in ("exact", "fuzzy", "category"):
        count = source_counts.get(source, 0)
        print(f"  {source:10s}: {count}/{total} ({count / total * 100:.1f}%)")

    if fuzzy_matches:
        print()
        print("-" * 70)
        print(f"Fuzzy matches ({len(fuzzy_matches)}) -- these matched via "
              "word-overlap rather than an exact key.")
        print("Review these to confirm the matched answer is correct:")
        print("-" * 70)
        for q, matched in fuzzy_matches:
            flag = "  " if q.strip().lower().rstrip("?") == matched else "->"
            print(f"  Q: {q}")
            print(f"  {flag} matched: {matched}")
            print()

    if unresolved:
        print("-" * 70)
        print(f"Unresolved -- fell back to a generic category answer "
              f"({len(unresolved)}):")
        print("-" * 70)
        for q in unresolved:
            print(f"  - {q}")
    else:
        print()
        print("No questions fell back to a generic category answer -- "
              "every question in the dataset has a specific match.")

    print()
    print("=" * 70)


if __name__ == "__main__":
    run_tests()