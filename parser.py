"""
parser.py
Attempts to parse a tokenized query against the grammar in grammar.py.
"""

from grammar import get_parser
from preprocess import tokenize

_parser = get_parser()


def parse_query(text: str):
    """
    Try to parse a raw query string.
    Returns (tree_or_None, tokens).
    tree is None if the grammar could not derive the sentence.
    """
    tokens = tokenize(text)
    try:
        trees = list(_parser.parse(tokens))
    except ValueError:
        # token not in grammar's lexicon
        return None, tokens

    if trees:
        return trees[0], tokens
    return None, tokens


def save_tree_image(tree, out_path: str):
    """
    Save a parse tree as a PNG, without needing Tkinter (which isn't
    available in this environment). Renders the tree's ASCII-art form
    (from tree.pretty_print()) as a monospace image using matplotlib.
    """
    import io
    import contextlib
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # Capture the ASCII tree that tree.pretty_print() normally prints
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        tree.pretty_print()
    ascii_tree = buf.getvalue()

    lines = ascii_tree.rstrip("\n").split("\n")
    n_lines = max(len(lines), 1)
    max_width = max((len(line) for line in lines), default=1)

    fig_width = max(6, max_width * 0.11)
    fig_height = max(2, n_lines * 0.35)
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.axis("off")
    ax.text(
        0.01, 0.99, ascii_tree,
        family="monospace", fontsize=12,
        va="top", ha="left", transform=ax.transAxes,
    )
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def run_interactive():
    print("CFG Parser - DeKUT SCIT FAQ Assistant (type 'exit' to quit)\n")
    while True:
        try:
            text = input("Enter a question: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if text.lower() in ("exit", "quit"):
            break
        if not text:
            continue

        tree, tokens = parse_query(text)
        print(f"Tokens : {tokens}")
        if tree:
            print("Status : PARSED\n")
            print("Bracketed form:")
            print(tree)
            print("\nTree diagram:")
            tree.pretty_print()

            save = input("Save this parse tree to a file? (y/N): ").strip().lower()
            if save == "y":
                import os
                os.makedirs("/mnt/user-data/outputs", exist_ok=True)
                out_path = "/mnt/user-data/outputs/parse_tree.png"
                save_tree_image(tree, out_path)
                print(f"Saved to {out_path}\n")
        else:
            print("Status : NO PARSE -- the grammar could not derive this sentence.")
            print("         Check that every word is in grammar.py's lexicon, and that")
            print("         the sentence structure matches one of the defined patterns.\n")


if __name__ == "__main__":
    run_interactive()