---
title: "Poor man's Chapman-Enskog exercise"
date: 2026-07-18
draft: false
tags: ["physics"]
---
{{< katex >}}
These are notes about deriving the Navier-Stokes equation starting from the Boltzman equation, in a somewhat schematic/simplified way.

The Boltzman equation is
$$ \partial_t f + v\cdot \nabla f = \Gamma(f).$$

Here it is understood that \(f = f(\vec x, \vec v)\) is the density of particles at a particular position \(\vec x\) and velocity \(\vec v\) in phase space. \(\Gamma(f)\) is the collision integral, which I won't even bother to write out, but it is, of course, also a function of \((\vec x, \vec v)\).

The reason I won't write it out is that I will use a simplified collision term
$$
\Gamma(f) \approx -\tau^{-1} (f - f^{eq}),
$$
where \(f^{eq}\) is some equillibrium distribution we want our solution to converge to. This is known as the BGK model, named after Bathnager, Gross and Krook, and it is, of course, an approximation, valid under certain conditions. We won't worry about the conditions, we just see that the r.h.s. has the right dimensions and move on, since modern physics is anyways just glorified dimensional analysis. This relaxation time \(\tau\) is supposed to be of the order of the time between two collisions underwent by a single particle, in the hypothesis that after a couple of collisions underwent by a single particle, the system has reached equillibrium.

We do the Chapman-Enskog Ansatz, but only to first order in \(\varepsilon =\frac{\lambda}{L}\), the Knudsen number.
\(f = f^{(0)} + \varepsilon f^{(1)}\). Here \(\lambda \approx v_{thermal} \tau\) is the mean free path, and \(L\) is the spatial scale at which signifficant changes in \(f\) occur.

The fact that \(f\) changes over distances of order \(L\) means that \(\nabla f \sim f/L\). To make the Knudsen number appear explicitly in the Boltzman equation, we therefore define the dimensionless operator \(\tilde \nabla = L \nabla\). Similarly,
we define a dimensionless time derivative \(\tilde \partial_t = T\partial_t\).

The r.h.s. would tempt us to believe that, in time, the relevant changes in \(f\) are on scales of order \(\tau\). That should be true for microscopic changes, but we can believe that the spatial derivative term induces some kind of slower changes, occuring at times of order \(T\). \(L\) and \(T\) should be related by the typical velocities corresponding to \(f\). This will justify a model assumption we make further, that the temporal Knudsen number \(\frac{\tau}{T}\) equals the spatial one \(\frac{\lambda}{L}\).

The Boltzman equation becomes

$$T^{-1} \tilde{\partial_t} f + L^{-1} v\cdot \tilde\nabla f = - \tau^{-1} (f - f^{eq}).$$
Or, multiplying by \(\tau\) and employing the assumption about the equal Knudsen numbers: 
$$\tilde{\partial}_t f + \frac{T}{L} v \cdot \tilde\nabla f = - \frac{1}{\varepsilon} (f - f^{eq}).$$

We next replace \(f = f^{(0)} + \varepsilon f^{(1)}\) and compare order terms, order by order.
We get, unsurprisingly, \(f^{(0)} = f^{(eq)}\) and, assuming that \(f^{(eq)}\) is constant in time, \(f^{(1)} = -\frac{T}{L}v \cdot \tilde\nabla f^{(0)} \), into which if we replace the \(\tilde \nabla\) we get \(\varepsilon f^{(1)} = -\tau v \cdot \nabla f^{(0)}\).

The next step is to look at the momentum conservation equation, which we get out of the Boltzman equation by integrating it against the collisional invariant \(\psi = v^i\):

$$\partial_t(n u^i) + \partial_j \int v^j v^i f(\vec{v}) \text{d}^3v = 0.$$

After subtracting the continuity equation and doing some standard manipulations, the equation above can be written as

$$\partial_t(nu^i) + u^j\partial_j (n u^i) + \partial_j (n \langle (v- u)^j(v-u)^i\rangle) = 0.$$

The last term is
$$\int \text d^3 v \partial_j[f(\vec v) (v- u)^j(v-u)^i].$$

It has two contributions, one from \(f^{(0)} = f^{(eq)}\), and another one from \(\varepsilon f^{(1)}\).
The contribution from \(f^{(0)}\) is what we identify as the static pressure (see e.g. Harris 2.3 for a physical rationalization of this).

We make modeling choice that \(n\) is constant, so that, after dividing by \(n\), this equation becomes:

$$\partial_t u^i + u^j \partial_j u^i + \partial_j (P^{(0)})^{ij} + \frac{1}{n}\partial_j T^{ij} = 0,$$

where \((P^{(0)})^{ij}\) corresponds to the zeroth-order contribution (static pressure) and \(T^{ij}\) to the first order. The first three terms correspond to the Euler equation, while, as we will see next, the last term will give us viscosity.


It is time we choose a reasonable expression for \(f^{(0)}\). What else but the Maxwell distribution:

$$f^{(0)}(\vec x, \vec v) = n(\vec x)\frac{1}{\mathcal N(\beta(\vec x))} \exp\left[-\beta(\vec x) \frac{m (\vec{v} - \vec{u})^2}{2}\right].$$

We will, however, make the simplifying assumption that the inverse temperature \(\beta\) and the density \(n\) are constant throughout space. Considering temperature and density variations would give us some additional diffusion terms, maybe.

We replace in the expression of \(\varepsilon f^{(1)}\)
$$ \varepsilon f^{(1)} = -\tau \vec v \cdot \nabla f^{(0)} = -\tau f^{0}\vec v \cdot \nabla \log {f^0} = - \tau \beta m f^{0} v^i (\vec v - \vec u)\cdot \partial_i \vec u.$$

Next we compute 
$$ T^{ij}(\vec x) = \int \text{d}^3v \varepsilon f^{(1)}(\vec x, \vec v) (v -u)^i(v-u)^j \\= -\tau\beta m\int \text{d}^3 v f^{(0)} v^k (v-u)^l \partial_k u^l (v-u)^i (v-u)^j \\= -\tau\beta m n\partial_k u^l \int \text{d}^3 c f_G(\vec c) c^k c^l c^i c^j,
$$
where in the last step we used \(\vec c = \vec v - \vec u\), \(f^{0}(\vec v) = n f_G(\vec c)\) and we subtracted \(0 = \int \text{d}^3 c f_G u^k c^l c^i c^j\).
Here, \(f_G(\vec c) = \frac{1}{\mathcal N} \exp(-\beta m \frac{\vec c^2}{2})\), the gaussian distribution of the peculiar velocity \(\vec c\).

The integral is 
$$
\int \mathrm{d}^3 c\, f_G(\vec c)\, c^k c^l c^i c^j
= (\beta m)^{-2}\left(\delta^{kl}\delta^{ij}+\delta^{ki}\delta^{lj}+\delta^{kj}\delta^{li}\right).
$$

After replacing in the expression for \(T^{ij}\) and contracting the \(k, l\) indices, we are left with
$$
T^{ij} = -\tau\frac{k_B T}{m} n \left(\nabla \cdot u \delta^{ij} + \partial_i u^j + \partial_j u^i\right). $$

Due to our assumption of incompressibility, we should here admit that \(\nabla \cdot u = 0\), but if we had not done it, this term would have represented a bulk viscosity, which has the effect of producing a modified effective pressure. Let's ignore the corresponding term.

Next, computing the last term in the equation above, we see
$$
\frac{1}{n} \partial_j T^{ij} = -\tau \frac{k_B T}{m}\Delta u^i,
$$

Leading to the Navier-Stokes equation
$$
\partial_t u^i + u^j \partial_j u^i + \partial_i p - \gamma \Delta u^i = 0,
$$
where we have used that 
$$ (P^{(0)})^{ij} = p \delta^{ij}, $$
and we have identified the kinematic viscosity
$$
\gamma = \tau \frac{k_B T}{m}.
$$

Thus, we have related a rough description of microscopic collisions, in terms of \(\tau, T, m\) to a macroscopic parameters, the kinematic viscosity. What more can you want from life?
