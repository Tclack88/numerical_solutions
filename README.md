# numerical_solutions
Numerical solutions to differential equations. Animated

![https://github.com/Tclack88/blog/blob/gh-pages/assets/dynamical_systems/dynamic systems.png](https://github.com/Tclack88/blog/blob/gh-pages/assets/dynamical_systems/dynamic systems.png)

Read more about the project [on my blog](https://tclack88.github.io/blog/code/2022/07/29/dynamical_system_modeling.html)

non-standard dependencies:

                matplotlib      -       pip install matplotlib
                pygame          -       pip install pygame
                scipy           -       pip install scipy
                numpy           -       pip install numpy

Animations implemented separately: 
- using Matplotlib's Animation library
- pygame (I've had past experience from this and it performs much faster)

It's not quite modular. The system of equations must be found, but the plotting has to be revisited in both pieces of code and you have to be careful in choosing what to draw/render.
