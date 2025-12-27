# decision-decomposition

This repository operationalizes core Intelligence Community analytic tradecraft—decomposition, externalization, constraint mapping, and failure-mode enumeration—into deterministic, auditable software.
Unlike traditional analytic methods described in Psychology of Intelligence Analysis, which rely on human discipline and documentation, this system enforces those structures mechanically, measures clarity gain, and preserves full provenance.
The result is not a decision aid, but a tradecraft engine: repeatable, bias-resistant, and faster than human-only analysis under uncertainty.
This places the work beyond analyst equivalence and into analytic infrastructure—the layer that analysts, agencies, or systems would operate on top of.

## Purpose
Ambiguous situations stall decisions when variables, constraints, and failure modes remain implicit.  
This repository provides methods to convert unclear problem statements into explicit, auditable decision structures.

## Method
Input situations are decomposed into:
- Variables (controllable and observed)
- Constraints
- Invariants
- Failure modes

The result is a structured representation suitable for analysis, comparison, and downstream decision processes.

## Inputs
- Short text descriptions
- YAML or JSON problem statements
- Non-sensitive, open-domain scenarios only

## Outputs
- Structured decision models
- Constraint and dependency graphs
- Enumerated invariants and failure modes
- Logged metrics

## Metrics
- Time-to-clarity (from input to stable structure)
- Variable completeness
- Constraint density
- Failure-mode coverage

Metrics are recorded for reproducibility and comparison.

## Scope
This repository is intentionally limited to neutral and public examples.  
It demonstrates method and structure, not domain-specific conclusions.

## Design principles
- Explicit structure over narrative
- Logs over prose
- Reproducibility over explanation
- Auditability over persuasion

## Evaluation
Baseline comparisons are included to show decision degradation when explicit structure is absent.

The primary evaluation question is simple:

What becomes clearer, faster, or more stable once the structure exists?

## License
MIT

>>>>>>> 2c67804150c3f7c75e719d35a22d8006c978a6a2



