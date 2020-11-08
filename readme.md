# Its looking a lot like Science
# McGill Physics Hackathon 2020
# Dima Romanov, Peter Kaloyannis, Simon Tartarovsky, Henri Lamarre, Alex Beaudin

Procedural generation of SnowFlakes using two different generation Algorithms

1- simon_attempt.py
Generates Branches using Monte Carlo cost functions

2- alex-reiter/src/cell.py
Simulates snowflake using Reiter's method, a cellular automata model of formation. 
The model is governed by Laplace's equation, and the diffusion equation. 
The magnitude of these effects os governed by the aforementioned constants.

3- basic_ray_tracer.py
Real-time raytracing the snowflakes generated using the Monte Carlo simulation.
This is entirely in python. 


## The Reiter method
The second method we tried uses cellular automata to generate snowflakes. 
This model is deterministic, which means it produces slightly less visually interesting.
However, it the evolution is governed by 3 constants, which can be modified over time for more
interesting results. 

### Getting Started
Just run cell.py!
The code can be found in the alex-reiter branch in the src folder. 
Dependencies are numpy, scipy, and matplotlib.
