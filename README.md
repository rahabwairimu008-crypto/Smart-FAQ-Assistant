# Smart Grammar-Based FAQ Assistant -- DeKUT School of Computer Science & IT

A text/voice/WhatsApp assistant that answers common student questions
directed to the Dean's or COD's office, using a hand-built
Context-Free Grammar (CFG) to model question syntax, plus a
keyword-based classifier and a lookup-based response engine grounded
in DeKUT's published academic regulations.

## Project files

| File | Purpose |
|---|---|
| `preprocess.py` | Cleans and tokenizes raw text input |
| `grammar.py` | The CFG (Context-Free Grammar) modeling question syntax |
| `parser.py` | Parses tokenized input against the CFG; run directly for an interactive parse-tree viewer |
| `classifier.py` | Assigns a query to one of 8 topic categories (A-H) via keyword matching |
| `response.py` | 78 specific question-answer pairs + category-level fallback answers |
| `main.py` | Orchestrates the full pipeline; run directly for a text Q&A CLI |
| `voice_interface.py` | Voice input/output layer (speech-to-text + text-to-speech) |
| `whatsapp_bot.py` | WhatsApp integration via a Flask + Twilio webhook |
| `test_all_questions.py` | Runs all 78 questions through the pipeline and reports pass/fail stats |
| `requirements.txt` | Python dependencies |

## Setup

```bash
pip install -r requirements.txt
```

If `PyAudio` fails to install (needed for the voice interface's
microphone input), install the system audio library first:

```bash
# Linux
sudo apt install portaudio19-dev espeak-ng
pip install pyaudio

# macOS
brew install portaudio
pip install pyaudio

# Windows
pip install pyaudio   # usually works directly
```

## Usage

### 1. Text mode (core assistant)

```bash
python3 main.py
```

Type a question at the `Ask a question:` prompt. Type `exit` to quit.

Run a quick demo with 8 sample questions instead of typing your own:

```bash
python3 main.py --batch
```

### 2. Parser only (view the CFG parse tree for any question)

```bash
python3 parser.py
```

Type a question at the `Enter a question:` prompt to see its tokens,
whether the grammar could parse it, the bracketed parse tree, and an
ASCII tree diagram. You'll be offered the option to save the tree as a
PNG (saved to `/mnt/user-data/outputs/parse_tree.png` or your working
directory, depending on environment).

### 3. Voice mode

```bash
python3 voice_interface.py
```

Speaks a welcome message, then listens through your microphone,
transcribes your question (needs internet -- uses Google's free Web
Speech API), runs it through the assistant, and speaks the answer back
(fully offline text-to-speech via `pyttsx3`). Say "exit" to stop.

**Requires:** a working microphone and speakers, and an internet
connection for the speech-to-text step only.

### 4. WhatsApp mode

```bash
python3 whatsapp_bot.py
```

Starts a local Flask server. Full one-time setup instructions
(Twilio Sandbox + ngrok) are documented at the top of
`whatsapp_bot.py` -- you'll need a free Twilio account and ngrok (or
similar) to expose your local server to the internet so Twilio can
reach it.

### 5. Run the full test suite

```bash
python3 test_all_questions.py
```

Reports the grammar parse success rate and answer-matching accuracy
across all 78 collected questions -- useful evidence for your report's
evaluation section.

## Notes for the project report

- The grammar currently parses roughly a third of the 78 collected
  questions (run `test_all_questions.py` for the exact current
  figure). The remainder fail mainly due to passive-voice
  constructions (e.g. "What documents are required...") and
  vocabulary gaps, both good material for your "Refactor and
  Evaluate" section.
- Response accuracy is separated from grammar parsing on purpose:
  even a question the CFG can't parse still gets a correct, specific
  answer via the classifier + lookup layer, which is a legitimate
  and explainable robustness design choice.
- Answers in `response.py` are grounded in DeKUT's published academic
  regulations and official pages where verifiable; a few (fee
  clearance percentage, some portal specifics) are flagged in-line as
  unverifiable from public sources and should be confirmed with your
  COD/Finance Office before being presented as final in your
  submission.
