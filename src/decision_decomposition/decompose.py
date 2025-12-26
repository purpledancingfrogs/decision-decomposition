import time
from typing import Dict, Any
from .model import Variable, Constraint, Invariant, FailureMode, DecisionModel

def decompose(problem: Dict[str, Any]) -> Dict[str, Any]:
    start = time.time()

    variables = []
    for k in problem.get("knowns", {}).keys():
        variables.append(Variable(name=k, kind="observed"))
    for k in problem.get("unknowns", []):
        variables.append(Variable(name=k, kind="observed"))

    for k in ["crew_allocation", "load_shedding_policy"]:
        variables.append(Variable(name=k, kind="controllable"))

    constraints = [Constraint(expression=c) for c in problem.get("constraints", [])]

    invariants = [
        Invariant(expression="critical_services_priority > general_distribution"),
        Invariant(expression="frequency_violation increases cascading_risk"),
    ]

    failure_modes = [
        FailureMode(
            description="Delayed load shedding causes transformer damage",
            trigger="demand > capacity for extended duration",
        ),
        FailureMode(
            description="Generator fuel depletion at hospitals",
            trigger="fuel_resupply_delay",
        ),
    ]

    model = DecisionModel(
        variables=variables,
        constraints=constraints,
        invariants=invariants,
        failure_modes=failure_modes,
    )

    elapsed = round(time.time() - start, 3)

    return {
        "model": model,
        "metrics": {
            "time_to_clarity_seconds": elapsed,
            "variable_count": len(variables),
            "constraint_count": len(constraints),
            "failure_mode_count": len(failure_modes),
        },
    }
