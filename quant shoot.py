import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# Constants
# ============================================================

hbar = 1.054571817e-34       # J s
m = 9.10938356e-31           # electron mass (kg)
eV = 1.602176634e-19         # 1 eV in joules


# ============================================================
# Well width
# ============================================================

L = 5e-9                      # 5 nm

# For 10 nm, use:
# L = 10e-9


# ============================================================
# Euler step size
# ============================================================

N = 5000
h = L / N


# ============================================================
# Solve Schrödinger equation for a given energy
# ============================================================

def solve_sch(E, plot=False):

    x = 0.0

    # Boundary conditions
    psi = 0.0                 # psi(0) = 0
    phi = 1.0                 # psi'(0) = 1

    XX = [x]
    PSI = [psi]

    while x < L:

        # First-order equations:
        #
        # dpsi/dx = phi
        # dphi/dx = -(2mE/hbar^2) psi

        dpsi = phi
        dphi = -(2*m*E/(hbar**2))*psi

        # Euler method
        psi_new = psi + h*dpsi
        phi_new = phi + h*dphi

        x = x + h

        psi = psi_new
        phi = phi_new

        XX.append(x)
        PSI.append(psi)

    if plot:
        plt.plot(np.array(XX)*1e9, PSI,
                 label=f"E = {E/eV:.6f} eV")

    return psi


# ============================================================
# SHOOTING METHOD
# ============================================================

def shooting(E1_eV, E2_eV, tolerance=1e-10):

    # Convert eV to joules
    E1 = E1_eV * eV
    E2 = E2_eV * eV

    # Calculate psi(L) for the two initial guesses
    f1 = solve_sch(E1)
    f2 = solve_sch(E2)

    print("----------------------------------------")
    print("Initial guesses")
    print("----------------------------------------")

    print(f"E1 = {E1_eV:.6f} eV")
    print(f"psi(L) = {f1:.6e}")

    print()

    print(f"E2 = {E2_eV:.6f} eV")
    print(f"psi(L) = {f2:.6e}")

    # --------------------------------------------------------
    # Check whether the two guesses bracket a root
    # --------------------------------------------------------

    if f1 == 0:
        return E1

    if f2 == 0:
        return E2

    if f1*f2 > 0:
        raise ValueError(
            "The two initial guesses do not bracket an eigenvalue.\n"
            "Choose two energies for which psi(L) has opposite signs."
        )

    # --------------------------------------------------------
    # Repeated interpolation
    # --------------------------------------------------------

    iteration = 0

    while True:

        iteration += 1

        # Linear interpolation
        E = E1 + (E2-E1)*(0-f1)/(f2-f1)

        # Shoot using new energy
        f = solve_sch(E)

        print(
            f"Iteration {iteration:2d}: "
            f"E = {E/eV:.10f} eV, "
            f"psi(L) = {f:.6e}"
        )

        # ----------------------------------------------------
        # Check convergence
        # ----------------------------------------------------

        if abs(f) < tolerance:
            return E

        # ----------------------------------------------------
        # Keep the root bracketed
        # ----------------------------------------------------

        if f*f1 < 0:

            E2 = E
            f2 = f

        else:

            E1 = E
            f1 = f


# ============================================================
# FIND DIFFERENT ENERGY LEVELS
# ============================================================

# First energy level
E_ground = shooting(0.010, 0.020)

print()
print("Ground state energy:")
print(f"E1 = {E_ground/eV:.8f} eV")


# Second energy level
E_second = shooting(0.050, 0.070)

print()
print("Second state energy:")
print(f"E2 = {E_second/eV:.8f} eV")


# Third energy level
E_third = shooting(0.120, 0.150)

print()
print("Third state energy:")
print(f"E3 = {E_third/eV:.8f} eV")


# ============================================================
# Plot the wavefunctions
# ============================================================

solve_sch(E_ground, plot=True)
solve_sch(E_second, plot=True)
solve_sch(E_third, plot=True)

plt.xlabel("x (nm)")
plt.ylabel("Wavefunction ψ(x)")
plt.title("Infinite Quantum Well - Shooting Method")
plt.grid()
plt.legend()
plt.show()


# ============================================================
# Analytical values for comparison
# ============================================================

h = 2*np.pi*hbar

E1_exact = h**2/(8*m*L**2)
E2_exact = 4*E1_exact
E3_exact = 9*E1_exact

print()
print("----------------------------------------")
print("Comparison with analytical solution")
print("----------------------------------------")

print(f"Numerical E1 = {E_ground/eV:.8f} eV")
print(f"Exact     E1 = {E1_exact/eV:.8f} eV")

print()

print(f"Numerical E2 = {E_second/eV:.8f} eV")
print(f"Exact     E2 = {E2_exact/eV:.8f} eV")

print()

print(f"Numerical E3 = {E_third/eV:.8f} eV")
print(f"Exact     E3 = {E3_exact/eV:.8f} eV")