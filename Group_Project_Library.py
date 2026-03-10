def clear_terminal() :
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def header() :
    print("\033[36m")
    print("*" * 50)
    print("          WING DEFLECTION CALCULATOR\n")
    print("            On a Wing and a Prayer\n\n")
    print("               Brought to you by\n")
    print("       Alessandra, Aeryn, Kyra, Jacob, Jay")
    print("*" * 50)
    print("\033[0m")

def calculate_air_density(h):
 
    L = 0.0065          #  Change in air temp at altitude
    g = 9.81            #  Gravity
    R = 287             #  Gas Constant for air
    rho0 = 1.225        #  Air density at sea level
    T0 = 288.15         #  Temp in K
 
    rho = rho0 + (1 - (L * h) / T0) ** ((g / (R * L)) - 1)  #  Claculate air density at elevation
 
    return rho

def get_flight_conditions():
    while True:
        air_speed = float(input("\nEnter Air Speed (kts): "))
        if air_speed<=50:
            print("The aircraft is moving to slow to fly!")
        elif air_speed<=500:
            break
        else:
            print("That is faster than the aircraft can travel.")
    
    while True:
        altitude = float(input("Enter Altitude (meters): "))
        if altitude<=0:
            print("The aircraft must be off the ground!")
        elif altitude<=13000:
            break
        else:
            print("The aircraft is nearly in space! Try a lower altitude.")
    v = air_speed * 0.51444
 
    return v, altitude

def display_results(plane, material, lift, deflection, L_wing):
 
    print("\n" + "*" * 40)
    print(f"AIRCRAFT: {plane}")
    print(f"MATERIAL: {material}")
    print(f"TOTAL LIFT: {lift:,.3f} N")
    print(f"Estimated Wingtip Deflection: {deflection * 100:.3f} cm")
 
    if deflection > (L_wing * 0.2):
        print("Warning: Structural limits likely exceeded!")
 
    