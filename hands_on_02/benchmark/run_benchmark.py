import pandas as pd
import numpy as np
import os

def normalize_noise_type(name):
    name = name.lower()
    if 'white' in name: return 'White'
    if 'pink' in name: return 'Pink'
    if 'red' in name: return 'Red'
    return name

def run_benchmark():
    # Paths
    claude_path = os.path.join('claude-code', 'results', 'noise_moments.csv')
    gemini_path = os.path.join('gemini-cli', 'results', 'noise_moments.csv')
    
    if not os.path.exists(claude_path) or not os.path.exists(gemini_path):
        print("Error: One or more noise_moments.csv files missing.")
        return

    # Load data
    df_claude = pd.read_csv(claude_path)
    df_gemini = pd.read_csv(gemini_path)

    # Normalize noise type names
    df_claude['noise_type_norm'] = df_claude['noise_type'].apply(normalize_noise_type)
    df_gemini['noise_type_norm'] = df_gemini['Type'].apply(normalize_noise_type)

    # Prepare results list
    results = []

    noise_types = ['White', 'Pink', 'Red']
    metrics = [('skewness', 'Skewness'), ('kurtosis_raw', 'Kurtosis')]

    for nt in noise_types:
        for m_claude, m_gemini in metrics:
            c_data = df_claude[df_claude['noise_type_norm'] == nt][m_claude]
            g_data = df_gemini[df_gemini['noise_type_norm'] == nt][m_gemini]
            
            c_mean = c_data.mean()
            c_std = c_data.std()
            g_mean = g_data.mean()
            g_std = g_data.std()
            
            # Difference in values realization by realization
            # We assume realizations are in the same order (0-99)
            # Both agents used SEED=42, but different implementations
            # Let's compute the absolute difference of the means for the report
            abs_diff_mean = abs(c_mean - g_mean)
            
            results.append({
                'noise_type': nt,
                'metric': m_claude,
                'claude_mean': c_mean,
                'claude_std': c_std,
                'gemini_mean': g_mean,
                'gemini_std': g_std,
                'abs_diff_mean': abs_diff_mean
            })

    # Create DataFrame and save
    df_comparison = pd.DataFrame(results)
    output_path = os.path.join('benchmark', 'moments_comparison.csv')
    df_comparison.to_csv(output_path, index=False)
    print(f"Successfully generated {output_path}")

if __name__ == "__main__":
    run_benchmark()
