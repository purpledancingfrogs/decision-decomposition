import json
import glob
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

MODEL = SentenceTransformer("all-MiniLM-L6-v2")

def load_runs(path_pattern):
    runs = []
    for p in glob.glob(path_pattern, recursive=True):
        with open(p, "r", encoding="utf-8") as f:
            runs.append({"path": p, "text": f.read()})
    return runs

def extract_sections(text):
    sections = {"observers": "", "descriptions": "", "verdict": ""}
    lower = text.lower()
    for key in sections:
        if key in lower:
            sections[key] = text
    return sections

def embed(text):
    return MODEL.encode([text])

def similarity(a, b):
    return float(cosine_similarity(embed(a), embed(b))[0][0])

def analyze(model_a, model_b, threshold=0.85):
    result = {}
    for k in ["observers", "descriptions", "verdict"]:
        sim = similarity(model_a[k], model_b[k])
        result[k] = {"similarity": sim, "pass": sim >= threshold}
    result["all_pass"] = all(v["pass"] for v in result.values())
    return result

def main():
    outputs = {
        "gpt4": load_runs("cross-model-convergence-benchmark/raw_outputs/gpt4/*.md"),
        "grok": load_runs("cross-model-convergence-benchmark/raw_outputs/grok/*.md"),
        "claude": load_runs("cross-model-convergence-benchmark/raw_outputs/claude/*.md"),
    }

    structured = {}
    for model, runs in outputs.items():
        structured[model] = [extract_sections(r["text"]) for r in runs]

    comparisons = []
    pairs = [("gpt4", "grok"), ("gpt4", "claude"), ("grok", "claude")]
    for a, b in pairs:
        for i in range(min(len(structured[a]), len(structured[b]))):
            comparisons.append({
                "pair": f"{a}-{b}",
                "run": i + 1,
                "analysis": analyze(structured[a][i], structured[b][i])
            })

    result = {
        "threshold": 0.85,
        "comparisons": comparisons
    }

    Path("cross-model-convergence-benchmark/analysis").mkdir(parents=True, exist_ok=True)
    with open("cross-model-convergence-benchmark/analysis/results.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

if __name__ == "__main__":
    main()
