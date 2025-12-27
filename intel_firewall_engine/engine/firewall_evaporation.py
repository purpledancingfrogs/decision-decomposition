"""Firewall Evaporation
Simulates information loss under enforced boundary conditions.
"""

def evaporate(states, rate=0.1):
    return {k: v * (1 - rate) for k, v in states.items()}
