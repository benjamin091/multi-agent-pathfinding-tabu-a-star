# Multi-Agent Path Finding using Tabu Search and A*

## Project Overview

This project addresses the Multi-Agent Path Finding (MAPF) problem using a hybrid approach that combines the classical A* algorithm with the metaheuristic Tabu Search. The goal is to efficiently compute collision-free paths for multiple agents navigating in a shared environment.

## Key Features

- Implementation of A* for individual agent path planning.  
- Tabu Search metaheuristic to resolve conflicts and improve overall multi-agent path plans.  
- Hybrid approach leverages strengths of both exact search (A*) and metaheuristic optimization (Tabu Search).  
- Designed to handle complex, constrained multi-agent scenarios.

## Methodology

- **A*** is used to generate initial paths for each agent independently.  
- **Tabu Search** iteratively improves the joint solution by exploring alternative path combinations while avoiding cycles through tabu lists.  
- Conflict detection and resolution ensure collision-free trajectories.  
- Optimization focuses on metrics such as total path length, makespan, or number of conflicts.

## Usage

- Define environment and agent start/goal positions.  
- Run the A* algorithm to compute initial individual paths.  
- Apply Tabu Search to refine and coordinate paths among agents.  
- Evaluate solution quality and computational performance.

## Tools & Technologies

- Python
- Custom implementation of A* and Tabu Search  
- Visualization tools for path and conflict analysis (optional)

## Deliverables

- Source code for A* and Tabu Search.  
- Example scenarios and test cases.  
- Documentation explaining algorithms, design decisions, and experimental results.

---

## Contact

For questions or feedback, please open an issue or contact the maintainer.
