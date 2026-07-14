"""
grammar.py
Context-Free Grammar for the Smart Grammar-Based FAQ Assistant (DeKUT SCIT).

The grammar models the SYNTAX of the 70 collected student queries.
It does not decide topic/category -- that is handled separately in
classifier.py, since a single CFG cannot cleanly distinguish
"fees" queries from "graduation" queries using syntax alone.

Patterns covered (drawn directly from the 70-question dataset):
  1. WH + copula                -> "Who is the Dean ... ?"
  2. WH + copula + NP            -> "What is a supplementary examination ?"
  3. WH + do/does + NP + VP      -> "When does course registration begin ?"
  4. WH + do + I + VP            -> "How do I register for my courses ?"
  5. WH + modal + I + VP         -> "How can I contact the school ?"
  6. WH + happens + if + I + VP  -> "What happens if I miss a CAT ?"
  7. Yes/No modal question       -> "Can I defer my studies ?"
  8. WH + should + I + VP        -> "Who should I contact ... ?"
"""

import nltk
from nltk import CFG

GRAMMAR_TEXT = r"""
  S -> WHCOP QMARK
  S -> WHDOAUX QMARK
  S -> WHMODALQ QMARK
  S -> WHIFQ QMARK
  S -> YNQ QMARK

  WHCOP -> WH COP NP
  WHCOP -> WH COP NP PP

  WHDOAUX -> WH DOAUX NP VP
  WHDOAUX -> WH DOAUX NP

  WHMODALQ -> WH MODAL PRON VP
  WHMODALQ -> WH DOAUX PRON VP

  WHIFQ -> WH VBZ IF PRON VP
  WHIFQ -> WH VBZ IF NP VP

  YNQ -> MODAL PRON VP
  YNQ -> MODAL PRON VP PP

  VP -> V
  VP -> V NP
  VP -> V PP
  VP -> V NP PP
  VP -> V PP PP

  NP -> DET N
  NP -> DET ADJ N
  NP -> N
  NP -> ADJ N
  NP -> N N
  NP -> DET N N

  PP -> P NP

  WH -> 'what' | 'who' | 'where' | 'when' | 'how' | 'why'
  COP -> 'is' | 'are'
  DOAUX -> 'do' | 'does'
  MODAL -> 'can' | 'should' | 'must'
  VBZ -> 'happens'
  IF -> 'if'
  PRON -> 'i' | 'my'

  V -> 'register' | 'pay' | 'apply' | 'contact' | 'change' | 'defer' | 'obtain' | 'download' | 'collect' | 'choose' | 'know' | 'appeal' | 'sit' | 'fail' | 'repeat' | 'begin' | 'close' | 'miss' | 'submit' | 'qualify' | 'satisfy' | 'confirm'

  N -> 'course' | 'courses' | 'fees' | 'registration' | 'examination' | 'examinations' | 'project' | 'supervisor' | 'attachment' | 'deferment' | 'graduation' | 'transcript' | 'clearance' | 'certificate' | 'requirements' | 'dean' | 'department' | 'programme' | 'semester' | 'arrears' | 'results' | 'documents' | 'balance' | 'letter' | 'presentation' | 'proposal' | 'studies' | 'year' | 'probation' | 'retake' | 'portal' | 'statement' | 'receipt' | 'list' | 'name' | 'school' | 'university' | 'unit' | 'units' | 'admission' | 'cod' | 'chairperson' | 'reasons' | 'reason'

  DET -> 'a' | 'the' | 'my' | 'this' | 'an'
  ADJ -> 'final-year' | 'internal' | 'external' | 'academic' | 'supplementary' | 'special' | 'retake' | 'ordinary'

  P -> 'for' | 'in' | 'to' | 'of' | 'after' | 'before' | 'by' | 'from'

  QMARK -> '?'
"""

grammar = CFG.fromstring(GRAMMAR_TEXT)


def get_parser():
    """Return an NLTK ChartParser built from the grammar above."""
    return nltk.ChartParser(grammar)


if __name__ == "__main__":
    print(f"Grammar loaded with {len(grammar.productions())} production rules.")