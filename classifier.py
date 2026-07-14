"""
classifier.py
Assigns a query to one of the 8 categories (A-H) used in the project brief.

Note: the CFG in grammar.py models SYNTAX (question form), not topic.
Category classification is done here via keyword matching against the
parsed/lowercased tokens, since a single small CFG cannot reliably
distinguish "fees" from "graduation" using structure alone. This mirrors
how the two concerns are typically separated in this kind of project:
grammar handles form, classifier handles meaning/category.
"""

CATEGORIES = {
    "A_SCHOOL_INFO": {
        "label": "School Information & Programmes",
        "keywords": ["dean", "programme", "admission", "located", "contact",
                     "change my course", "bachelor", "requirements"],
    },
    "B_REGISTRATION": {
        "label": "Course Registration",
        "keywords": ["registration", "register", "portal", "add", "drop",
                     "deadline"],
    },
    "C_FEES": {
        "label": "Fees and Finance",
        "keywords": ["fee", "fees", "balance", "statement", "receipt",
                     "arrears", "pay"],
    },
    "D_EXAMS": {
        "label": "Examinations & Academic Progress",
        "keywords": ["examination", "exam", "cat", "supplementary", "retake",
                     "probation", "repeat", "discontinued", "appeal",
                     "results"],
    },
    "E_DEFERMENT": {
        "label": "Deferment and Readmission",
        "keywords": ["defer", "deferment", "readmission", "readmitted"],
    },
    "F_ATTACHMENT": {
        "label": "Internal and External Attachment",
        "keywords": ["attachment", "internal", "external"],
    },
    "G_PROJECT": {
        "label": "Final Year Project",
        "keywords": ["project", "supervisor", "proposal", "presentation"],
    },
    "H_GRADUATION": {
        "label": "Graduation and Clearance",
        "keywords": ["graduation", "clearance", "transcript", "certificate",
                     "graduate"],
    },
}


def classify(text: str) -> str:
    """Return the best-matching category key, or 'UNKNOWN'."""
    text = text.lower()
    best_cat, best_score = "UNKNOWN", 0

    for cat, info in CATEGORIES.items():
        score = sum(1 for kw in info["keywords"] if kw in text)
        if score > best_score:
            best_cat, best_score = cat, score

    return best_cat


if __name__ == "__main__":
    tests = [
        "How do I download my fee statement?",
        "Can I change my project supervisor?",
        "How do I apply for deferment?",
        "What documents are required for graduation clearance?",
    ]
    for t in tests:
        print(t, "->", classify(t))