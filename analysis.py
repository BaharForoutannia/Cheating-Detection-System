import json
import nltk
from difflib import SequenceMatcher
from nltk.corpus import wordnet

THRESHOLD = 0.8
FAST_TIME_LIMIT = 5

def syntactic_similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

def semantic_similarity(sentence1, sentence2):
    def get_synsets(word):
        synsets = wordnet.synsets(word)
        return synsets[0] if synsets else None

    words1 = sentence1.lower().split()
    words2 = sentence2.lower().split()

    total_score = 0
    count = 0

    for w1 in words1:
        syn1 = get_synsets(w1)
        max_score = 0
        for w2 in words2:
            syn2 = get_synsets(w2)
            if syn1 and syn2:
                score = wordnet.path_similarity(syn1, syn2)
                if score and score > max_score:
                    max_score = score
        if max_score:
            total_score += max_score
            count += 1

    return total_score / count if count else 0

# خواندن فایل پاسخ‌ها
with open("answers.json", "r", encoding="utf-8") as f:
    data = json.load(f)

users = list(data.keys())

print("\n🔍 Cheating Analysis:\n")

# Check for similarity
for qnum in range(1, 4):
    for i in range(len(users)):
        for j in range(i + 1, len(users)):
            u1, u2 = users[i], users[j]
            a1 = next((x["description"] for x in data[u1] if x["qnumber"] == qnum), "")
            a2 = next((x["description"] for x in data[u2] if x["qnumber"] == qnum), "")

            syn_score = syntactic_similarity(a1, a2)
            sem_score = semantic_similarity(a1, a2)
            avg_score = (syn_score + sem_score) / 2

            if avg_score >= THRESHOLD:
                percent = int(avg_score * 100)
                print(f"⚠️ Question {qnum}: High similarity ({percent}%) between '{u1}' and '{u2}'")

# Check for fast responses
for user in data:
    for item in data[user]:
        if item["time_taken"] <= FAST_TIME_LIMIT:
            print(f"⏱️ {user} answered Question {item['qnumber']} too fast ({item['time_taken']} seconds) – suspicious!")

print("\n✅ Analysis completed.")

