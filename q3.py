import numpy as np
P_Cloudy = 0.5
P_Sprinkler_given_Cloudy = {True: 0.1, False: 0.5}
P_Rain_given_Cloudy = {True: 0.8, False: 0.2}
P_WetGrass_given_Sprinkler_Rain = {
    (True, True): 0.99,
    (True, False): 0.90,
    (False, True): 0.80,
    (False, False): 0.00
}
def monte_carlo_simulation(num_samples=10000):
    count_sprinkler_given_wet_grass = 0
    count_wet_grass = 0

    for _ in range(num_samples):
        cloudy = np.random.rand() < P_Cloudy
        sprinkler = np.random.rand() < P_Sprinkler_given_Cloudy[cloudy]
        rain = np.random.rand() < P_Rain_given_Cloudy[cloudy]
        wet_grass = np.random.rand() < P_WetGrass_given_Sprinkler_Rain[(sprinkler, rain)]
        if wet_grass:
            count_wet_grass += 1
            if sprinkler:
                count_sprinkler_given_wet_grass += 1

    if count_wet_grass == 0:
        return 0  
    return count_sprinkler_given_wet_grass / count_wet_grass

estimated_probability = monte_carlo_simulation()
print(f"Estimated P(Sprinkler=True | WetGrass=True): {estimated_probability}")
