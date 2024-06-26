# -*- coding: utf-8 -*-
"""Particle Swarm Optimisation (PSO).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1dyMfkX3myNe8cG_J88iJUnt9DyDPswuk
"""

# Implement the basic PSO algorithm.

# PSO:
# Global topology (everyone knows about gbest)
# c1 = c2 = 1.49618
# linear decrease of inertia weight w from 0.9 to 0.4 with iterations
# Other settings are up to you (population/swarm size, number of iterations).

# ! Important notes !

# The equation for velocity computation is a vector equation.
# The initial velocity v0 is 0.
# Velocity is limited to a max of 20% of the search space range in each dimension.
# Tasks

# 1) Implement PSO
# 2) Test PSO on the same test functions

# Import Libraries
import numpy as np

# Define test functions
# Sphere function
def sphere(x):
    return np.sum(x**2)

# Schwefel function
def schwefel(x):
    return 418.9829 * len(x) - np.sum(x * np.sin(np.sqrt(np.abs(x))))

# Rastrigin function
def rastrigin(x):
    return 10 * len(x) + np.sum(x**2 - 10 * np.cos(2 * np.pi * x))

# Define PSO algorithm
def pso(pop_size, dim, bounds, max_iter, obj_func, topology='global', c1=1.49618, c2=1.49618, w_range=(0.9, 0.4)):
    # Initialization
    swarm = np.random.uniform(bounds[0], bounds[1], size=(pop_size, dim))
    velocity = np.zeros_like(swarm)
    pbest = swarm.copy()
    pbest_values = np.array([obj_func(p) for p in pbest])

    if topology == 'global':
        gbest = pbest[np.argmin(pbest_values)]
        gbest_value = np.min(pbest_values)
    elif topology == 'ring':
        gbest = pbest[np.argmin(pbest_values)]
        gbest_value = np.min(pbest_values)
        # Define ring topology
        neighbors = {i: [(i - j) % pop_size for j in range(1, pop_size // 2 + 1)] + [(i + j) % pop_size for j in range(1, pop_size // 2 + 1)] for i in range(pop_size)}

    # Main loop
    for iteration in range(max_iter):
        w = w_range[0] - (w_range[0] - w_range[1]) * iteration / max_iter  # Linearly decrease inertia weight

        for i in range(pop_size):
            # Velocity update
            r1, r2 = np.random.rand(dim), np.random.rand(dim)
            if topology == 'global':
                velocity[i] = w * velocity[i] + c1 * r1 * (pbest[i] - swarm[i]) + c2 * r2 * (gbest - swarm[i])
            elif topology == 'ring':
                ring_neighbors = neighbors[i]
                velocity[i] = w * velocity[i] + c1 * r1 * (pbest[i] - swarm[i]) + c2 * r2 * (pbest[ring_neighbors].mean(axis=0) - swarm[i])

            # Velocity clipping
            v_max = 0.2 * (bounds[1] - bounds[0])
            velocity[i] = np.clip(velocity[i], -v_max, v_max)

            # Position update
            swarm[i] += velocity[i]

            # Position clipping
            swarm[i] = np.clip(swarm[i], bounds[0], bounds[1])

            # Update personal best
            if obj_func(swarm[i]) < pbest_values[i]:
                pbest[i] = swarm[i]
                pbest_values[i] = obj_func(swarm[i])

        # Update global best
        if topology == 'global':
            gbest_index = np.argmin(pbest_values)
            if pbest_values[gbest_index] < gbest_value:
                gbest = pbest[gbest_index]
                gbest_value = pbest_values[gbest_index]
        elif topology == 'ring':
            gbest_index = np.argmin(pbest_values)
            if pbest_values[gbest_index] < gbest_value:
                gbest = pbest[gbest_index]
                gbest_value = pbest_values[gbest_index]

    return gbest, gbest_value

# Test PSO on Sphere, Schwefel, and Rastrigin functions
pop_size = 50
dim = 10
max_iter = 100

# Define bounds for each function
bounds = {
    'sphere': (-5.12, 5.12),
    'schwefel': (-500, 500),
    'rastrigin': (-5.12, 5.12)
}

# Test PSO with Global Topology
print("PSO - Global Topology:")
for obj_func, func_bounds in zip([sphere, schwefel, rastrigin], bounds.values()):
    best_solution, best_value = pso(pop_size, dim, func_bounds, max_iter, obj_func, topology='global', c1=1.49618, c2=1.49618, w_range=(0.9, 0.4))
    print(f"{obj_func.__name__}: Best Value = {best_value}, Best Solution = {best_solution}")

# Test PSO with Ring Topology
print("\nPSO - Ring Topology:")
for obj_func, func_bounds in zip([sphere, schwefel, rastrigin], bounds.values()):
    best_solution, best_value = pso(pop_size, dim, func_bounds, max_iter, obj_func, topology='ring', c1=1.49618, c2=1.49618, w_range=(0.9, 0.4))
    print(f"{obj_func.__name__}: Best Value = {best_value}, Best Solution = {best_solution}")

