import glob
import json
from pathlib import Path

def load_runs(pattern):
    runs = {}
    for p in glob.glob(pattern, recursive=True):
        model = Path(p).parts[-2]
        with open(p, "r", encoding="utf-8") as f:
            runs.setdefault(model, []).append(f.read())
    return runs

def normalize_lines(text):
    return {
        line.strip().lower()
        for line in text.splitlines()
        if line.strip() and not line.strip().startswith("#")
    }

def extract_invariants(text):
    lines = normalize_lines(text)
    return {
        l for l in lines
        if any(k in l for k in ["must", "cannot", "always", "requires", "fails if"])
    }

def structural_overlap(a, b):
    if not a and not b:
        return 1.0
    return len(a & b) / max(len(a | b), 1)

def analyze(run_a, run_b):
    inv_a = extract_invariants(run_a)
    inv_b = extract_invariants(run_b)
    return {
        "overlap": structural_overlap(inv_a, inv_b),
        "count_a": len(inv_a),
        "count_b": len(inv_b),
        "intersection": sorted(inv_a & inv_b),
    }

def compare_models(runs):
    results = {}
    models = list(runs.keys())
    for i in range(len(models)):
        for j in range(i + 1, len(models)):
            a, b = models[i], models[j]
            results[f"{a} vs {b}"] = analyze(
                "\n".join(runs[a]),
                "\n".join(runs[b])
            )
    return results

if __name__ == "__main__":
    runs = load_runs("raw_outputs/**/run*.txt")
    results = compare_models(runs)
    print(json.dumps(results, indent=2))
