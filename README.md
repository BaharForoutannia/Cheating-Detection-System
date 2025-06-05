# Cheating Detection System

A Flask-based web application designed to flag potential exam cheating by analyzing answer patterns and response times. The system presents a secure login interface and delivers questions one at a time, recording each student’s answers and response times. After the quiz, an analysis script evaluates the answers for both syntactic and semantic similarity (leveraging NLTK’s WordNet) and identifies unusually quick responses. This helps instructors automatically pinpoint suspicious activity for further review.


---


## 🌟 Key Features

User Authentication: Secure login page to distinguish each student.

Sequential Questions: Displays one question at a time and tracks the exact response time for each answer.

Answer Recording: Stores all responses along with timestamps in a JSON file for easy processing.

Cheating Analysis Script: A separate analysis.py computes pairwise answer similarities and flags suspicious cases.

Semantic Similarity Detection: Uses NLTK’s WordNet to measure semantic closeness between different answers.

Fast-Response Flags: Detects answers submitted in an unusually short time (below a configurable threshold).

Report Generation: Outputs a concise report of flagged answers and potential cheating incidents.


---


## 🔧 Technology Stack

Python – Core programming language.

Flask – Lightweight web framework for the quiz interface.

NLTK (Natural Language Toolkit) – For natural language processing and semantic analysis.

WordNet – Lexical database used via NLTK for semantic similarity.

JSON – Stores question responses and metadata.

HTML/CSS/JavaScript – Front-end for the login page and question display.


---


## 🚀 Setup Instructions

1.Clone the repository:
git clone https://github.com/BaharForoutannia/algorithm_project.git cd cheating-detection 

2.Create a Python virtual environment (recommended):
python -m venv venv
source venv/bin/activate

3.Install dependencies:
pip install Flask nltk

Optionally, if a requirements.txt is provided:
pip install -r requirements.txt 

4.Download NLTK data:
The analysis script requires the WordNet corpora. In a Python shell or script, run:

import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')

This will fetch the WordNet database and its Open Multilingual WordNet data.


---


## 📊 Project Structure

cheating-detection/

│

├── app.py               # Main Flask application (login, question views)

├── analysis.py          # Post-quiz analysis script for detecting cheating

├── requirements.txt     # Python dependencies (Flask, NLTK, etc.)

├── README.md            # (This file)

│

├── templates/           # HTML templates for Flask

│    ├── login.html       # User login page

│    ├── questions.html    # Displays each questions and captures answer

│    └── single_question.html      # Displays a question and captures answer

│

├── static/              # Static files (CSS, JS, images)

│    └── style.css              

│

└── data/                # Data directory

     └── answers.json     # JSON file storing all user responses and timings

app.py – Implements the Flask routes for login, serving questions, and recording answers.

analysis.py – Reads the answers.json, computes syntactic and semantic similarities, and flags fast responses.

templates/ – Contains HTML templates for the web interface.

data/answers.json – Accumulates each student’s answers, question IDs, and response times.

requirements.txt – Lists Python packages (if provided).


---


## 📋 Usage Guide

1.Running the Flask App:

Start the quiz application by running:

flask run 

or

python app.py 

Navigate to http://127.0.0.1:5000 in a web browser. Log in with provided credentials (or register as configured), then proceed through the quiz questions in sequence. Each answer and the time taken will be stored in data/answers.json.

2.Running the Analysis Script:

After collecting responses, execute the analysis:

python analysis.py data/answers.json 

This will process the JSON file and print or save a report of any suspicious findings (see sample below). No web server is required for this step; it’s a standalone analysis.


---


## Detection Logic Details

The core cheating detection works on two fronts:

1.Response Time Analysis:

Each answer is timestamped. If the time delta from showing a question to submitting an answer falls below a predefined threshold (e.g. 2 seconds), the response is flagged as suspicious. Such rapid responses may indicate guessing or automated completion.

2.Answer Similarity Analysis:

For every pair of submitted answers (across different users for the same question), the script computes: 

- Syntactic similarity: 

A basic text comparison (e.g. edit distance or common substring ratio) to catch identical or near-identical answers.

- Semantic similarity:

Leveraging NLTK’s WordNet interface, each answer is tokenized and key words are matched via their synsets. We use the WordNet path similarity metric: for two word senses (synsets), synset1.path_similarity(synset2) returns a score between 0 and 1 based on their distance in the lexical hierarchy. Higher scores indicate closer meaning. The script aggregates these scores (e.g. averaging best-matched word pairs) to estimate how similar the overall answers are in meaning.

If the similarity score exceeds a set threshold (for example, 0.8) or if answers share many synonyms/hypernyms, the pair is flagged for review. This catches cases where students copy each other using different wording (e.g. synonyms).

Example Process:

To compare “Cats are cute” and “Cats are adorable”, the WordNet synsets for “cute” and “adorable” yield a high path similarity (they are near synonyms), triggering a flag. Meanwhile, a student answer submitted in 0.5 seconds would also be highlighted as anomalously fast.


---


## Sample Analysis Output

Below is an example of what the analysis might report on the console or log:

Cheating Analysis Report

Question 1:
- Users Alice and Bob have highly similar answers (semantic similarity = 0.92). 
Question 2:
- User Charlie answered unusually fast (response time = 1.2s).
Question 4:
- Users Alice and Eve have identical answers (syntactic match).

Each bullet shows a flagged event: either a pair of users with similar answers (semantic/syntactic) or a user with a very quick response. In practice, the output can be formatted as plain text, JSON, or integrated into an instructor dashboard.


---


## 🔄 Future Improvements

- Advanced NLP Models: Replace or augment WordNet with transformer-based embeddings (e.g. BERT/SBERT or Universal Sentence Encoder) for more robust semantic matching. These models capture context better than simple synonym matching.
- Database Integration: Use a relational or NoSQL database (instead of a JSON file) to scale to many students and support real-time queries.
- User Interface Enhancements: Provide an admin dashboard to visualize flagged responses, statistics on average response times, and allow instructors to review/correct flags.
- Configurable Thresholds: Make similarity and time thresholds configurable per test or question difficulty, possibly with machine-learning calibration.
- Multi-language Support: Extend NLP support to handle non-English answers by integrating multilingual wordnets or translation layers.
- Continuous Monitoring: Implement real-time monitoring during exams (e.g. live flagging of short response times).
- Security Enhancements: Enforce stronger authentication (e.g. two-factor login) and secure sessions to prevent login abuse.
