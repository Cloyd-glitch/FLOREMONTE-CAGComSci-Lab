import matplotlib.pyplot as plt
from decimal import Decimal, getcontext, ROUND_FLOOR, ROUND_HALF_UP


# 1. SETUP: High Precision Environment

# We set the precision to 150 digits so we can clearly see 
# the difference at the 100th decimal place.
getcontext().prec = 150 

# This is "True Pi" to 100+ digits for our reference
true_pi_str = "3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148086513282306647"

# 2. THE FORMULA: Volume of a Sphere
# Formula: V = (4/3) * pi * r^3

def calculate_sphere_volume(pi_value):
    # We use a large radius (100 meters) to amplify the difference
    radius = Decimal('100.0') 
    
    # IMPORTANT: We use Decimal for the fraction 4/3 to keep high precision
    fraction = Decimal('4') / Decimal('3')
    
    # Calculate Volume
    volume = fraction * pi_value * (radius ** 3)
    return volume

# 3. HELPER FUNCTIONS (Truncate vs Round)

def get_truncated_pi(n_decimals):
    # Slice the string to keep "3." + n decimals
    return Decimal(true_pi_str[:2 + n_decimals])

def get_rounded_pi(n_decimals):
    # Create a full Decimal and round it to n places
    d = Decimal(true_pi_str)
    quantizer = Decimal('1.' + '0' * n_decimals)
    return d.quantize(quantizer, rounding=ROUND_HALF_UP)


# 4. PERFORM THE EXPERIMENT

decimals_to_test = [20, 40, 60, 100]

# Calculate a "Perfect" baseline using the full length string
best_pi = Decimal(true_pi_str)
best_result = calculate_sphere_volume(best_pi)

trunc_diffs = []
round_diffs = []

print(f"{'Decimals':<10} | {'Type':<10} | {'Calculated Volume':<30} | {'Error (Difference)'}")
print("-" * 85)

for n in decimals_to_test:
    # --- Test Truncation ---
    pi_trunc = get_truncated_pi(n)
    vol_trunc = calculate_sphere_volume(pi_trunc)
    diff_trunc = abs(vol_trunc - best_result)
    trunc_diffs.append(diff_trunc)
    
    # --- Test Rounding ---
    pi_round = get_rounded_pi(n)
    vol_round = calculate_sphere_volume(pi_round)
    diff_round = abs(vol_round - best_result)
    round_diffs.append(diff_round)
    
    # Print results (showing only first 25 chars of volume to keep table clean)
    print(f"{n:<10} | {'Trunc':<10} | {str(vol_trunc)[:25]}... | {diff_trunc:.2E}")
    print(f"{n:<10} | {'Round':<10} | {str(vol_round)[:25]}... | {diff_round:.2E}")

# 5. VISUALIZATION

plt.figure(figsize=(10, 6))

# Plotting Truncation Errors (Red Circle)
plt.plot(decimals_to_test, trunc_diffs, marker='o', linestyle='-', label='Truncation Error', color='red')

# Plotting Rounding Errors (Blue Square)
plt.plot(decimals_to_test, round_diffs, marker='s', linestyle='--', label='Rounding Error', color='blue')

# Use Log Scale because the error shrinks massively (from e-20 to e-100)
plt.yscale('log') 

plt.xlabel('Decimal Places of Pi Used')
plt.ylabel('Error Magnitude (Difference from True Volume)')
plt.title('Sphere Volume Calculation: Error by Pi Precision')
plt.grid(True, which="both", ls="-", alpha=0.3)
plt.legend()

plt.show()