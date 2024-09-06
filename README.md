# Implement the basic PSO algorithm.
- PSO: Global topology (everyone knows about gbest)

c1 = c2 = 1.49618

- linear decrease of inertia weight w from 0.9 to 0.4 with iterations
- Other settings are up to you (population/swarm size, number of iterations).

## Important notes
- The equation for velocity computation is a vector equation.
- The initial velocity v0 is 0.
- Velocity is limited to a max of 20% of the search space range in each dimension.

## Tasks
- Implement PSO
- Test PSO on the same test functions
