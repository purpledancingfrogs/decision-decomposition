import json
import argparse
from pathlib import Path
from collections import Counter

def tokenize(text):
    return [t for t in text.lower().split() if t.isalnum() or t.isalpha()]

def jaccard(a, b):
    A, B = set(a), set(b)
    return len(A & B) / max(1, len(A | B))

def cosine_counts(a, b):
    ca, cb = Counter(a), Counter(b)
    keys = set(ca) | set(cb)
    dot = sum(ca[k] * cb[k] for k in keys)
    na = sum(v*v for v in ca.values()) ** 0.5
    nb = sum(v*v for v in cb.values()) ** 0.5
    return 0.0 if na == 0 or nb == 0 else dot / (na * nb)

def score(texts):
    toks = [tokenize(t) for t in texts]
    pairwise = []
    for i in range(len(toks)):
        for j in range(i+1, len(toks)):
            pairwise.append({
                "jaccard": jaccard(toks[i], toks[j]),
                "cosine": cosine_counts(toks[i], toks[j])
            })
    if not pairwise:
        return {"pairs": 0, "jaccard_mean": 0.0, "cosine_mean": 0.0}
    return {
        "pairs": len(pairwise),
        "jaccard_mean": sum(p["jaccard"] for p in pairwise) / len(pairwise),
        "cosine_mean": sum(p["cosine"] for p in pairwise) / len(pairwise)
    }

def load_texts(root):
    return [p.read_text(encoding="utf-8") for p in Path(root).rglob("*.txt")]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inputs", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    texts = load_texts(args.inputs)
    result = score(texts)

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(result, indent=2), encoding="utf-8")

if __name__ == "__main__":
    main()