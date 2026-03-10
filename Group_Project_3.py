#	Clear the terminal
from matplotlib.pylab import choice
import sys
import Group_Project_Library as lib
lib.clear_terminal()
lib.header()

# 	User Inputs - select type of aircraft and wing material
#	Input flight speed and altitude
#   LIst of 6 different aircraft

def calculate_deflection() :    # Gather variable choices
    # 1- Aircraft data (wingspan in meters, reference area in m^2)
    aircraft = {
        "Sailplane (High Performance)" : {"span" : 21.0, "area" : 13.2},
        "Cesna 172" : {"span" : 11.0, "area" : 16.2},
        "Gulfstream G500" : {"span" : 26.5, "area" : 88.0},
        "Boeing 737-800" : {"span" : 35.8, "area" : 124.6},
        "Boeing 787-10" : {"span" : 60.1, "area" : 361.0},
        "Lockheed C-5 Galaxy" : {"span" : 67.9, "area" : 576.0},
    }

    materials = {
        "Carbon Fiber (CFRP)" : 150e9,
        "Aluminum (7075)" : 71.7e9,
        "Titanium Alloy" : 113e9,
        "Sitka Spruce (Wood)" : 11e9,
        "Concrete" : 28e9
    }


    # Select the airplane
    planes = list(aircraft.keys())
    for i, name in enumerate(planes, 1) :
        print(f"{i}. {name}")
    while True:
        choice = int(input("\nSelect Aircraft (1-6): "))
        if 1 <= choice <= len(planes):
            plane_choice = planes[choice - 1]
            break
        else:
            print("Out of range. Please select a valid number.")
    # Select the wing material
    mats = list(materials.keys())
    for j, name in enumerate(mats, 1) :
        print(f"{j}. {name}")
    while True:
        m_choice = int(input("\nSelect Wing Material (1-5): "))
        if 1<= m_choice <= len(mats):
            mat_choice = mats[m_choice-1]
            if mat_choice == "Concrete":
                print("A plane with concrete wings isn't going to get off the ground!")
                continue
            break
        else:
            print("Out of range. Please select a valid number.")
    

    #   This is a list of inputs and calculations

    v, h = lib.get_flight_conditions()

    rho = lib.calculate_air_density(h)

    print(f"Air density at {h} meters is", round(rho, 3), "kg/m^3")

    cl = 0.6  #This is the lift constant (L) using a higher than typical Cl for general calculations
    E = materials[mat_choice]

    #  This is for determining the thickness profile for the wing depending on AC chosen

    #  Structural Geometry (I value)
    plane_name = plane_choice

    if "Sailplane" in plane_name :
        thickness_factor = 0.03  #  very thin
    else:
        thickness_factor = 0.12  #Standard airfoil thickness


    span = aircraft[plane_name]["span"]
    area = aircraft[plane_name]["area"]

    #  Moment of Inertia (approximated for a wing box)
    #  I = (width * height^3) / 12
    avg_chord = area / span
    height = avg_chord * thickness_factor
    I = (avg_chord * (height**3)) / 12


    #  Let's calculate


    lift = 0.5 * rho * (v**2) * area * cl
    q = (lift / 2) / (span / 2)  #  Load per meter on one wing

    #  Cantilever Deflection: (q * l^4) / (8 * E * I)
    #  L is the length of one wing (half-span)
    L_wing = span / 2
    deflection = (q * (L_wing**4)) / (8 * E * I)

    #  Time to print stuff

    
    lib.display_results(plane_name, mat_choice, lift, deflection, L_wing)

    # # Calculate deflection at different points along the wing
 
    w = lift/L_wing
    deflection = []
    positions = []
    steps = 100
 
    for i in range(steps + 1) :
        x = L_wing * i / steps
        y = (w * x**2 / (24 * E * I)) * (6 * L_wing**2 - 4 * L_wing * x + x**2)
        positions.append(x)
        deflection.append(y)
    print("Deflection along the wing:")
    for i in range(len(positions)) :
        print("x = {:.2f}m, deflection = {:.6f}m".format(positions[i], deflection[i]))
    print()
 
    #Plot visualizing wing deflection
    for i in range(len(positions)):
        import pandas as pd
        import matplotlib.pyplot as plt
 
        plt.figure(figsize=(10,5))
        plt.plot(positions, deflection, label='Deflection of the wing', color='red', linestyle='--')
        plt.xlabel('Position [m]')
        plt.ylabel('Deflection [m]')
        plt.title('Deflection on the wing visualized')
        plt.ylim((min(deflection)-2), (max(deflection)+2))
        plt.legend()
        plt.grid(True)
        plt.axis('equal')
        plt.tight_layout()
        plt.show()
        break
 
    
if __name__ == "__main__" :
    calculate_deflection()