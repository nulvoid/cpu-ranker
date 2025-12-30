import pandas as pd
import os

weight_single = 0.78
weight_multi = 0.22
l2_bonus = 0.5
l2_exponent = 2.5
l2_scalar = 10
l3_bonus = 0.50
l3_exponent = 2.5
cache_scalar = 1.2
tdp_penalty = 175
scalar = 70

# List of CSV files to ignore
ignore_files = ['placeholder.csv']

# Define folder paths
base_folder = os.path.dirname(os.path.abspath(__file__))
cpus_folder = os.path.join(base_folder, 'CPUs')
out_folder = os.path.join(base_folder, 'Out')

# Get all CSV files in the CPUs folder
csv_files = [os.path.join(cpus_folder, f) for f in os.listdir(cpus_folder)
    if f.endswith('.csv') and f not in ignore_files]

all_results_list = []

for file in csv_files:
    try:
        print(f"Processing file: {file}")

        # Read CSV
        df = pd.read_csv(file, header=None, keep_default_na=False)
        if df.shape != (5,2):
            print(f"File {file} does not have the expected 5x2 format.")
            continue

        # Extract values by row and column
        single_avg = float(df.iloc[0,0])
        multi_avg = float(df.iloc[0,1])
        l2_cache = float(df.iloc[1,0])
        l3_cache = float(df.iloc[1,1])
        cores = int(df.iloc[2,0])
        threads = int(df.iloc[2,1])
        max_power = int(df.iloc[3,0])
        release_year = int(df.iloc[3,1])
        distro = str(df.iloc[4,0])
        desktop_env = str(df.iloc[4,1])
        processor_name = os.path.basename(file).replace('.csv', '')
        print(f"Extracted data for CPU {processor_name}")

        # Assign variables
        all_results_list.append({
            'Processor': processor_name,
            'Distribution': distro,
            'Desktop_Environment': desktop_env,
            'Cores': cores,
            'Threads': threads,
            'L2_Cache': l2_cache,
            'L3_Cache': l3_cache,
            'Max_Power': max_power,
            'Release_Year': release_year,
            'Single': single_avg,
            'Multi': multi_avg
        })
        print(f"Results appended for file: {file}")

    except Exception as e:
        print(f"Error processing file {file}: {e}")
        continue

all_results = pd.DataFrame(all_results_list)
print("All results combined into DataFrame")

if all_results.empty:
    print("No valid results to rank.")
else:
    # Calculate scores
    print("Calculating scores...")
    performance = (all_results['Single'] * weight_single) + (all_results['Multi'] * weight_multi)
    l2 = ((all_results['L2_Cache'] / all_results['Cores']) ** l2_exponent) * l2_bonus * l2_scalar
    l3 = ((all_results['L3_Cache'] / all_results['Cores']) ** l3_exponent) * l3_bonus
    cache = (l2 + l3) ** cache_scalar
    power_cost = ((all_results['Max_Power'] / all_results['Cores']) + (all_results['Max_Power'] / all_results['Threads'])) / 2
    efficiency = performance / (performance + power_cost * tdp_penalty)
    all_results['Score'] = ((performance + cache) * efficiency) * scalar

    # Round all scores to two decimal places for readability
    all_results = all_results.round({
        'Single': 2,
        'Multi': 2,
        'Score': 2
    })

    # Rank processors
    print("Ranking processors...")
    final_rankings = all_results.sort_values(by='Score', ascending=False).reset_index(drop=True)
    final_rankings['Rank'] = final_rankings.index + 1

    # Create Out directory if missing
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
        print(f"Created directory: {out_folder}")

    # Save final rankings
    output_file = os.path.join(out_folder, 'output.csv')
    final_rankings.to_csv(output_file, index=False)
    print(f"Rankings saved to '{output_file}'")
