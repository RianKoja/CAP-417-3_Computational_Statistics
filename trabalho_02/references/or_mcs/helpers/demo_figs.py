"""
This is a function to help illustrate the proposal of the OR-MCS.

The idea is to create 9 sets of data formed by triplets of datasets, one with no outliers, one with some outliers and one with many outliers. Then, we will apply the OR-MCS to each of them and compare the results.

Data is 2D, the triples will contian:

1. Data is an y=x line with some gaussian noise, while outliers lie in a circle
2. Data is over y=x^2 and outliers are highly noisy
3. Data is over y=e^x and outliers are highly noisy

The goal is to try fitting lines, quadratic curves and exponential curves to all datasets and compare the results of naive least squares, RANSAC and evaluate the results with traditional MCS.

A final figure shall be saved in svg format and a table in .text format should be saved to a local file to be imported on plano_de_estudos.tex
"""
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend to prevent blocking
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import RANSACRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from arch.bootstrap import MCS
import lightgbm as lgb
from joblib import Memory
import warnings
warnings.filterwarnings('ignore')


PATH_HERE = Path(__file__).parent
CACHE_DIR = PATH_HERE.parent / '.cache'
memory = Memory(CACHE_DIR, verbose=0)

@memory.cache
def generate_linear_data(n_points=100, n_outliers=0, noise_std=0.1, seed=42):
    """Generate data following y=x with Gaussian noise and circular outliers."""
    np.random.seed(seed)
    
    # Generate inliers
    x_inliers = np.random.uniform(-5, 5, n_points)
    y_inliers = x_inliers + np.random.normal(0, noise_std, n_points)
    
    # Generate outliers on a circle
    if n_outliers > 0:
        angles = np.random.uniform(0, 2*np.pi, n_outliers)
        radius = np.random.uniform(3, 6, n_outliers)
        x_outliers = radius * np.cos(angles)
        y_outliers = radius * np.sin(angles)
        
        x = np.concatenate([x_inliers, x_outliers])
        y = np.concatenate([y_inliers, y_outliers])
        is_outlier = np.concatenate([np.zeros(n_points, dtype=bool), np.ones(n_outliers, dtype=bool)])
    else:
        x = x_inliers
        y = y_inliers
        is_outlier = np.zeros(n_points, dtype=bool)
    
    return x, y, is_outlier


@memory.cache
def generate_quadratic_data(n_points=100, n_outliers=0, noise_std=0.5, seed=42):
    """Generate data following y=x^2 with Gaussian noise and highly noisy outliers."""
    np.random.seed(seed)
    
    # Generate inliers
    x_inliers = np.random.uniform(-3, 3, n_points)
    y_inliers = x_inliers**2 + np.random.normal(0, noise_std, n_points)
    
    # Generate outliers with high noise
    if n_outliers > 0:
        x_outliers = np.random.uniform(-3, 3, n_outliers)
        y_outliers = np.random.uniform(-5, 15, n_outliers)
        
        x = np.concatenate([x_inliers, x_outliers])
        y = np.concatenate([y_inliers, y_outliers])
        is_outlier = np.concatenate([np.zeros(n_points, dtype=bool), np.ones(n_outliers, dtype=bool)])
    else:
        x = x_inliers
        y = y_inliers
        is_outlier = np.zeros(n_points, dtype=bool)
    
    return x, y, is_outlier


@memory.cache
def generate_exponential_data(n_points=100, n_outliers=0, noise_std=0.3, seed=42):
    """Generate data following y=e^x with Gaussian noise and highly noisy outliers."""
    np.random.seed(seed)
    
    # Generate inliers
    x_inliers = np.random.uniform(-1, 2, n_points)
    y_inliers = np.exp(x_inliers) + np.random.normal(0, noise_std, n_points)
    
    # Generate outliers with high noise
    if n_outliers > 0:
        x_outliers = np.random.uniform(-1, 2, n_outliers)
        y_outliers = np.random.uniform(-2, 10, n_outliers)
        
        x = np.concatenate([x_inliers, x_outliers])
        y = np.concatenate([y_inliers, y_outliers])
        is_outlier = np.concatenate([np.zeros(n_points, dtype=bool), np.ones(n_outliers, dtype=bool)])
    else:
        x = x_inliers
        y = y_inliers
        is_outlier = np.zeros(n_points, dtype=bool)
    
    return x, y, is_outlier


@memory.cache
def fit_linear_least_squares(x, y):
    """Fit linear model using least squares."""
    X = x.reshape(-1, 1)
    model = LinearRegression()
    model.fit(X, y)
    return model


@memory.cache
def fit_quadratic_least_squares(x, y):
    """Fit quadratic model using least squares."""
    X = x.reshape(-1, 1)
    model = make_pipeline(PolynomialFeatures(2), LinearRegression())
    model.fit(X, y)
    return model


@memory.cache
def fit_exponential_least_squares(x, y):
    """Fit exponential model using least squares on log-transformed data."""
    # Filter out non-positive y values for log transformation
    mask = y > 0
    if np.sum(mask) < 2:
        return None
    
    X = x[mask].reshape(-1, 1)
    y_filtered = y[mask]
    
    try:
        log_y = np.log(y_filtered)
        model = LinearRegression()
        model.fit(X, log_y)
        return model
    except Exception:
        return None


@memory.cache
def fit_linear_ransac(x, y, seed=42):
    """Fit linear model using RANSAC."""
    X = x.reshape(-1, 1)
    model = RANSACRegressor(random_state=seed, min_samples=2)
    model.fit(X, y)
    return model


@memory.cache
def fit_quadratic_ransac(x, y, seed=42):
    """Fit quadratic model using RANSAC."""
    X = x.reshape(-1, 1)
    model = RANSACRegressor(
        estimator=make_pipeline(PolynomialFeatures(2), LinearRegression()),
        random_state=seed,
        min_samples=3
    )
    model.fit(X, y)
    return model


@memory.cache
def fit_exponential_ransac(x, y, seed=42):
    """Fit exponential model using RANSAC on log-transformed data."""
    mask = y > 0
    if np.sum(mask) < 2:
        return None
    
    X = x[mask].reshape(-1, 1)
    y_filtered = y[mask]
    
    try:
        log_y = np.log(y_filtered)
        model = RANSACRegressor(random_state=seed, min_samples=2)
        model.fit(X, log_y)
        
        # Create a full inlier mask that matches the original data length
        full_inlier_mask = np.zeros(len(y), dtype=bool)
        # Get the inlier mask from the filtered data
        filtered_inlier_mask = model.inlier_mask_
        # Map back to original indices
        mask_indices = np.where(mask)[0]
        full_inlier_mask[mask_indices[filtered_inlier_mask]] = True
        
        # Store the full mask in the model
        model.full_inlier_mask_ = full_inlier_mask
        
        return model, mask
    except:
        return None


@memory.cache
def fit_lightgbm(x, y, seed=42):
    """Fit LightGBM model."""
    X = x.reshape(-1, 1)
    model = lgb.LGBMRegressor(
        random_state=seed,
        n_estimators=100,
        learning_rate=0.1,
        max_depth=3,
        verbose=-1
    )
    model.fit(X, y)
    return model


@memory.cache
def fit_lightgbm_ransac(x, y, seed=42):
    """Fit LightGBM model with RANSAC for outlier robustness."""
    X = x.reshape(-1, 1)
    base_estimator = lgb.LGBMRegressor(
        random_state=seed,
        n_estimators=50,  # Fewer estimators since RANSAC will fit many times
        learning_rate=0.1,
        max_depth=3,
        min_child_samples=1,  # Allow fitting with very few samples
        verbose=-1
    )
    # Use min_samples as a fraction to adapt to dataset size
    # 0.5 means use 50% of data as minimum (more robust to outliers)
    model = RANSACRegressor(
        estimator=base_estimator,
        random_state=seed,
        min_samples=0.5,  # Use 50% of data as minimum sample size
        max_trials=100,   # More trials to find good consensus
        residual_threshold=None  # Auto-determine threshold from MAD
    )
    model.fit(X, y)
    return model


@memory.cache
def _calculate_mcs_pvalue_cached(losses_tuple, seed=42):
    """
    Internal cached version that takes hashable arguments.
    losses_tuple: tuple of (model_names, losses_arrays)
    """
    model_names, *loss_arrays = losses_tuple
    losses_dict = {name: losses for name, losses in zip(model_names, loss_arrays)}
    
    # Convert dict to DataFrame format expected by arch.bootstrap.MCS
    losses_df = pd.DataFrame(losses_dict)
    
    # Check if any models have identical losses (causes MCS to fail)
    # This happens when models are exactly the same (e.g., no outliers so LS = RANSAC)
    correlation_matrix = losses_df.corr()
    
    # Find pairs of models with correlation >= 0.9999 (essentially identical)
    identical_pairs = []
    for i in range(len(model_names)):
        for j in range(i+1, len(model_names)):
            if correlation_matrix.iloc[i, j] >= 0.9999:
                identical_pairs.append((model_names[i], model_names[j]))
    
    if identical_pairs:
        # If models are identical, assign equal p-values (1.0 means in confidence set)
        print(f"  Warning: Models with nearly identical losses detected: {identical_pairs}")
        print(f"  Assigning equal p-values for identical models.")
        
        # Check mean losses to determine which are best
        mean_losses = losses_df.mean()
        min_loss = mean_losses.min()
        
        # Models with minimum mean loss get p-value = 1.0 (in the confidence set)
        # Others get p-value proportional to their relative loss
        pvalues = {}
        for model in model_names:
            if mean_losses[model] <= min_loss * 1.0001:  # Within 0.01% of minimum
                pvalues[model] = 1.0
            else:
                # Proportional p-value based on relative performance
                pvalues[model] = max(0.0, 1.0 - (mean_losses[model] - min_loss) / min_loss)
        
        print(f"  P-values (based on mean losses): {pvalues}")
        return pvalues
    
    # Use simple MCS parameters that work well
    mcs = MCS(losses_df, size=0.10, seed=seed)
    mcs.compute()
    
    # Extract p-values from the MCS results
    # pvalues is a Series with model names as index
    pvalues = mcs.pvalues['Pvalue']
    
    # Debug: print MCS results
    print(f"  MCS Results (n={len(losses_df)}, models={len(model_names)}):")
    print(f"  Included models: {list(mcs.included)}")
    print(f"  P-values: {pvalues.to_dict()}")
    
    return pvalues.to_dict()


def calculate_mcs_pvalue(losses_dict, seed=42):
    """
    Calculate Model Confidence Set (MCS) p-values using the arch package.
    
    Parameters:
    -----------
    losses_dict : dict
        Dictionary with model names as keys and loss arrays as values
    
    Returns:
    --------
    dict : Dictionary with model names as keys and p-values as values
    """
    # Convert to hashable tuple format for caching
    model_names = tuple(losses_dict.keys())
    loss_arrays = tuple(tuple(losses_dict[name]) for name in model_names)
    losses_tuple = (model_names,) + loss_arrays
    
    return _calculate_mcs_pvalue_cached(losses_tuple, seed)


def evaluate_model(x, y, model, model_type='linear'):
    """Evaluate model and return metrics including losses for MCS."""
    X = x.reshape(-1, 1)
    
    try:
        if model_type == 'exponential':
            if isinstance(model, tuple):
                model, mask = model
                X_filtered = x[mask].reshape(-1, 1)
                y_filtered = y[mask]
                log_y_pred = model.predict(X_filtered)
                y_pred_full = np.zeros_like(y)
                y_pred_full[mask] = np.exp(log_y_pred)
                y_pred = y_pred_full[mask]
                residuals = y_filtered - y_pred
                squared_errors = residuals ** 2
            else:
                mask = y > 0
                X_filtered = x[mask].reshape(-1, 1)
                y_filtered = y[mask]
                log_y_pred = model.predict(X_filtered)
                y_pred = np.exp(log_y_pred)
                residuals = y_filtered - y_pred
                squared_errors = residuals ** 2
        else:
            if hasattr(model, 'predict'):
                y_pred = model.predict(X)
                residuals = y - y_pred
                squared_errors = residuals ** 2
            else:
                return {'rmse': np.inf, 'mae': np.inf, 'losses': None}
        
        rmse = np.sqrt(mean_squared_error(y_filtered if model_type == 'exponential' else y, y_pred))
        mae = mean_absolute_error(y_filtered if model_type == 'exponential' else y, y_pred)
        
        return {'rmse': rmse, 'mae': mae, 'losses': squared_errors}
    except Exception:
        return {'rmse': np.inf, 'mae': np.inf, 'losses': None}


def plot_dataset_triplet(datasets_triplet, results_triplet, dataset_type, output_file):
    """Create a 3x4 plot showing one triplet of datasets (no/some/many outliers)."""
    fig, axes = plt.subplots(3, 4, figsize=(24, 12))
    fig.suptitle(f'{dataset_type} Data: Comparison of LS, RANSAC, LightGBM, and RANSAC+LightGBM', 
                 fontsize=14, y=0.995)
    
    outlier_levels = ['No Outliers', 'Some Outliers', 'Many Outliers']
    
    for idx, (outlier_level, (x, y, is_outlier)) in enumerate(zip(outlier_levels, datasets_triplet)):
        row = idx
        
        # Sort for plotting
        sort_idx = np.argsort(x)
        x_sorted = x[sort_idx]
        
        # Separate true inliers and outliers
        x_inliers = x[~is_outlier]
        y_inliers = y[~is_outlier]
        x_outliers = x[is_outlier]
        y_outliers = y[is_outlier]
        
        # Plot 1: Least Squares
        ax1 = axes[row, 0]
        ax1.scatter(x_inliers, y_inliers, alpha=0.6, s=30, c='blue', label='Inliers', marker='o')
        if len(x_outliers) > 0:
            ax1.scatter(x_outliers, y_outliers, alpha=0.6, s=30, c='red', label='Outliers', marker='o')
        ax1.set_title(f'{outlier_level} - Least Squares', fontsize=11)
        ax1.grid(True, alpha=0.3)
        ax1.legend(fontsize=9)
        
        # Plot 2: RANSAC
        ax2 = axes[row, 1]
        ax2.set_title(f'{outlier_level} - RANSAC', fontsize=11)
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: LightGBM
        ax3 = axes[row, 2]
        ax3.scatter(x_inliers, y_inliers, alpha=0.6, s=30, c='blue', label='Inliers', marker='o')
        if len(x_outliers) > 0:
            ax3.scatter(x_outliers, y_outliers, alpha=0.6, s=30, c='red', label='Outliers', marker='o')
        ax3.set_title(f'{outlier_level} - LightGBM', fontsize=11)
        ax3.grid(True, alpha=0.3)
        ax3.legend(fontsize=9)
        
        # Plot 4: RANSAC + LightGBM
        ax4 = axes[row, 3]
        ax4.set_title(f'{outlier_level} - RANSAC+LightGBM', fontsize=11)
        ax4.grid(True, alpha=0.3)
        
        # Add fit lines if models exist
        if idx in results_triplet:
            ls_model, ransac_model, lgbm_model, lgbm_ransac_model, model_type = results_triplet[idx]
            
            try:
                X_plot = x_sorted.reshape(-1, 1)
                
                # Least Squares prediction
                if ls_model is not None:
                    if model_type == 'exponential':
                        mask = y > 0
                        y_pred_ls = np.exp(ls_model.predict(X_plot))
                    else:
                        y_pred_ls = ls_model.predict(X_plot)
                    ax1.plot(x_sorted, y_pred_ls, 'k-', linewidth=2.5, label='LS Fit', alpha=0.8)
                    ax1.legend(fontsize=9)
                
                # RANSAC prediction
                if ransac_model is not None:
                    if model_type == 'exponential':
                        if isinstance(ransac_model, tuple):
                            ransac_model_obj, _ = ransac_model
                        else:
                            ransac_model_obj = ransac_model
                        y_pred_ransac = np.exp(ransac_model_obj.predict(X_plot))
                    else:
                        ransac_model_obj = ransac_model
                        y_pred_ransac = ransac_model_obj.predict(X_plot)
                    
                    ax2.plot(x_sorted, y_pred_ransac, 'k-', linewidth=2.5, label='RANSAC Fit', alpha=0.8)
                    
                    # Show RANSAC classification
                    if hasattr(ransac_model_obj, 'inlier_mask_'):
                        # For exponential models, use the full_inlier_mask_
                        if model_type == 'exponential' and hasattr(ransac_model_obj, 'full_inlier_mask_'):
                            ransac_inlier_mask = ransac_model_obj.full_inlier_mask_
                        else:
                            ransac_inlier_mask = ransac_model_obj.inlier_mask_
                        
                        # Points that are true inliers and classified as inliers by RANSAC
                        true_positive = ~is_outlier & ransac_inlier_mask
                        # Points that are true outliers and classified as outliers by RANSAC  
                        true_negative = is_outlier & ~ransac_inlier_mask
                        # Points that are true inliers but classified as outliers by RANSAC
                        false_negative = ~is_outlier & ~ransac_inlier_mask
                        # Points that are true outliers but classified as inliers by RANSAC
                        false_positive = is_outlier & ransac_inlier_mask
                        
                        # Plot with different markers based on true class and RANSAC classification
                        if np.any(true_positive):
                            ax2.scatter(x[true_positive], y[true_positive], c='blue', alpha=0.7, s=40, 
                                      marker='o', label='Inliers (correctly classified)', edgecolors='darkblue', linewidths=1.5)
                        if np.any(true_negative):
                            ax2.scatter(x[true_negative], y[true_negative], c='red', alpha=0.7, s=40, 
                                      marker='x', label='Outliers (correctly classified)', linewidths=2.5)
                        if np.any(false_negative):
                            ax2.scatter(x[false_negative], y[false_negative], c='blue', alpha=0.7, s=40, 
                                      marker='x', label='Inliers (misclassified)', linewidths=2.5)
                        if np.any(false_positive):
                            ax2.scatter(x[false_positive], y[false_positive], c='red', alpha=0.7, s=40, 
                                      marker='o', label='Outliers (misclassified)', edgecolors='darkred', linewidths=1.5)
                    else:
                        # Fallback: just show true labels
                        ax2.scatter(x_inliers, y_inliers, alpha=0.6, s=30, c='blue', label='Inliers', marker='o')
                        if len(x_outliers) > 0:
                            ax2.scatter(x_outliers, y_outliers, alpha=0.6, s=30, c='red', label='Outliers', marker='o')
                    
                    ax2.legend(fontsize=8, loc='best')
                
                # LightGBM prediction
                if lgbm_model is not None:
                    y_pred_lgbm = lgbm_model.predict(X_plot)
                    ax3.plot(x_sorted, y_pred_lgbm, 'k-', linewidth=2.5, label='LightGBM Fit', alpha=0.8)
                    ax3.legend(fontsize=9)
                
                # RANSAC + LightGBM prediction
                if lgbm_ransac_model is not None:
                    y_pred_lgbm_ransac = lgbm_ransac_model.predict(X_plot)
                    ax4.plot(x_sorted, y_pred_lgbm_ransac, 'k-', linewidth=2.5, label='RANSAC+LightGBM Fit', alpha=0.8)
                    
                    # Show RANSAC classification for LightGBM
                    if hasattr(lgbm_ransac_model, 'inlier_mask_'):
                        ransac_inlier_mask = lgbm_ransac_model.inlier_mask_
                        
                        # Points that are true inliers and classified as inliers by RANSAC
                        true_positive = ~is_outlier & ransac_inlier_mask
                        # Points that are true outliers and classified as outliers by RANSAC  
                        true_negative = is_outlier & ~ransac_inlier_mask
                        # Points that are true inliers but classified as outliers by RANSAC
                        false_negative = ~is_outlier & ~ransac_inlier_mask
                        # Points that are true outliers but classified as inliers by RANSAC
                        false_positive = is_outlier & ransac_inlier_mask
                        
                        # Plot with different markers based on true class and RANSAC classification
                        if np.any(true_positive):
                            ax4.scatter(x[true_positive], y[true_positive], c='blue', alpha=0.7, s=40, 
                                      marker='o', label='Inliers (correctly classified)', edgecolors='darkblue', linewidths=1.5)
                        if np.any(true_negative):
                            ax4.scatter(x[true_negative], y[true_negative], c='red', alpha=0.7, s=40, 
                                      marker='x', label='Outliers (correctly classified)', linewidths=2.5)
                        if np.any(false_negative):
                            ax4.scatter(x[false_negative], y[false_negative], c='blue', alpha=0.7, s=40, 
                                      marker='x', label='Inliers (misclassified)', linewidths=2.5)
                        if np.any(false_positive):
                            ax4.scatter(x[false_positive], y[false_positive], c='red', alpha=0.7, s=40, 
                                      marker='o', label='Outliers (misclassified)', edgecolors='darkred', linewidths=1.5)
                    else:
                        # Fallback: just show true labels
                        ax4.scatter(x_inliers, y_inliers, alpha=0.6, s=30, c='blue', label='Inliers', marker='o')
                        if len(x_outliers) > 0:
                            ax4.scatter(x_outliers, y_outliers, alpha=0.6, s=30, c='red', label='Outliers', marker='o')
                    
                    ax4.legend(fontsize=8, loc='best')
                    
            except Exception as e:
                print(f"Error plotting {dataset_type} dataset {idx}: {e}")
        
        # Set labels
        if row == 2:
            ax1.set_xlabel('x', fontsize=10)
            ax2.set_xlabel('x', fontsize=10)
            ax3.set_xlabel('x', fontsize=10)
            ax4.set_xlabel('x', fontsize=10)
        
        ax1.set_ylabel('y', fontsize=10)
        ax2.set_ylabel('y', fontsize=10)
        ax3.set_ylabel('y', fontsize=10)
        ax4.set_ylabel('y', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(output_file, format='svg', dpi=150, bbox_inches='tight')
    print(f"Figure saved to {output_file}")
    
    # Also save as PDF for LaTeX compatibility
    pdf_file = output_file.with_suffix('.pdf')
    plt.savefig(pdf_file, format='pdf', dpi=150, bbox_inches='tight')
    print(f"Figure also saved to {pdf_file}")
    plt.close()


def create_results_table(datasets_all, results_all, output_file='results_table.tex'):
    """Create a LaTeX table with evaluation metrics including MCS p-values."""
    
    dataset_names = ['Linear (No)', 'Linear (Some)', 'Linear (Many)',
                     'Quadratic (No)', 'Quadratic (Some)', 'Quadratic (Many)',
                     'Exponential (No)', 'Exponential (Some)', 'Exponential (Many)']
    
    # Collect all metrics
    metrics_data = []
    
    for idx, (dataset_name, (x, y, is_outlier)) in enumerate(zip(dataset_names, datasets_all)):
        print(f"  Processing dataset {idx+1}/9: {dataset_name}...")
        if idx in results_all:
            ls_model, ransac_model, lgbm_model, lgbm_ransac_model, model_type = results_all[idx]
            
            # Evaluate LS model
            ls_metrics = evaluate_model(x, y, ls_model, model_type)
            
            # Evaluate RANSAC model
            ransac_metrics = evaluate_model(x, y, ransac_model, model_type)
            
            # Evaluate LightGBM model
            lgbm_metrics = evaluate_model(x, y, lgbm_model, 'lightgbm')
            
            # Evaluate RANSAC + LightGBM model
            lgbm_ransac_metrics = evaluate_model(x, y, lgbm_ransac_model, 'lightgbm')
            
            # Calculate MCS p-values if losses are available
            if (ls_metrics['losses'] is not None and ransac_metrics['losses'] is not None 
                and lgbm_metrics['losses'] is not None and lgbm_ransac_metrics['losses'] is not None):
                # Ensure equal length by padding/truncating if needed
                min_len = min(len(ls_metrics['losses']), len(ransac_metrics['losses']), 
                             len(lgbm_metrics['losses']), len(lgbm_ransac_metrics['losses']))
                losses_dict = {
                    'LS': ls_metrics['losses'][:min_len],
                    'RANSAC': ransac_metrics['losses'][:min_len],
                    'LightGBM': lgbm_metrics['losses'][:min_len],
                    'RANSAC+LightGBM': lgbm_ransac_metrics['losses'][:min_len]
                }
                print(f"    Computing MCS p-values for {dataset_name} (n={min_len})...")
                mcs_pvalues = calculate_mcs_pvalue(losses_dict)
                print(f"    MCS calculation complete for {dataset_name}")
                ls_mcs = mcs_pvalues.get('LS', 0.0)
                ransac_mcs = mcs_pvalues.get('RANSAC', 0.0)
                lgbm_mcs = mcs_pvalues.get('LightGBM', 0.0)
                lgbm_ransac_mcs = mcs_pvalues.get('RANSAC+LightGBM', 0.0)
            else:
                ls_mcs = 0.0
                ransac_mcs = 0.0
                lgbm_mcs = 0.0
                lgbm_ransac_mcs = 0.0
            
            # Store metrics
            metrics_data.append({
                'name': dataset_name,
                'ls_rmse': ls_metrics['rmse'],
                'ransac_rmse': ransac_metrics['rmse'],
                'lgbm_rmse': lgbm_metrics['rmse'],
                'lgbm_ransac_rmse': lgbm_ransac_metrics['rmse'],
                'ls_mae': ls_metrics['mae'],
                'ransac_mae': ransac_metrics['mae'],
                'lgbm_mae': lgbm_metrics['mae'],
                'lgbm_ransac_mae': lgbm_ransac_metrics['mae'],
                'ls_mcs': ls_mcs,
                'ransac_mcs': ransac_mcs,
                'lgbm_mcs': lgbm_mcs,
                'lgbm_ransac_mcs': lgbm_ransac_mcs
            })
        else:
            metrics_data.append(None)
    
    # Function to get color based on normalized value within a row
    def get_color_code_for_row(values, inverse=False):
        """Return LaTeX color commands for a row of values.
        inverse=False: red for high values, green for low (RMSE, MAE)
        inverse=True: green for high values, red for low (MCS p-values)
        """
        # Filter out inf values for min/max calculation
        valid_values = [v for v in values if v != np.inf]
        
        if not valid_values or len(valid_values) < 2:
            # If all same or only one value, return empty colors
            return [''] * len(values)
        
        min_val = min(valid_values)
        max_val = max(valid_values)
        
        
        colors = []
        for value in values:
            if value == np.inf:
                colors.append('')
                continue
            
            # If all values are equal, use mid-tone yellow (norm=0.5)
            if min_val == max_val:
                norm = 0.5
            else: # Normalize to 0-1
                norm = (value - min_val) / (max_val - min_val)


            
            # if not a number, add no color
            if not isinstance(norm, (int, float)) or norm != norm:  # Check for NaN
                colors.append('')
                continue

            if inverse:
                norm = 1 - norm  # Invert for MCS (higher is better)
            
            # Create color gradient: green (0) -> yellow (0.5) -> red (1)
            if norm < 0.5:
                # Green to yellow
                r = int(norm * 2 * 255)
                g = 255
            else:
                # Yellow to red
                r = 255
                g = int((1 - (norm - 0.5) * 2) * 255)
            
            colors.append(f"\\cellcolor[RGB]{{{r},{g},0}}")
        
        return colors
    
    with open(output_file, 'w') as f:
        # Write LaTeX table header
        f.write("\\begin{table}[htbp]\n")
        f.write("\\centering\n")
        f.write("\\caption{Comparison of Fitting Methods: RMSE, MAE, and MCS p-values. ")
        f.write("Color coding: green indicates better performance, red indicates worse performance. ")
        f.write("See Figures~\\ref{fig:demo_linear}, \\ref{fig:demo_quadratic}, and \\ref{fig:demo_exponential} for visualizations.}\n")
        f.write("\\label{tab:demo_results}\n")
        f.write("\\resizebox{\\textwidth}{!}{%\n")  # Scale table to fit page width
        f.write("\\begin{tabular}{|l|cccc|cccc|cccc|}\n")
        f.write("\\hline\n")
        f.write("\\multirow{2}{*}{Dataset} & \\multicolumn{4}{c|}{RMSE} & \\multicolumn{4}{c|}{MAE} & \\multicolumn{4}{c|}{MCS p-value} \\\\\n")
        f.write(" & LS & RANSAC & LightGBM & R+LightGBM & LS & RANSAC & LightGBM & R+LightGBM & LS & RANSAC & LightGBM & R+LightGBM \\\\\n")
        f.write("\\hline\n")
        
        for idx, data in enumerate(metrics_data):
            if data is not None:
                # Get color codes for each row (comparing methods within each metric)
                rmse_values = [data['ls_rmse'], data['ransac_rmse'], data['lgbm_rmse'], data['lgbm_ransac_rmse']]
                mae_values = [data['ls_mae'], data['ransac_mae'], data['lgbm_mae'], data['lgbm_ransac_mae']]
                mcs_values = [data['ls_mcs'], data['ransac_mcs'], data['lgbm_mcs'], data['lgbm_ransac_mcs']]
                
                rmse_colors = get_color_code_for_row(rmse_values, inverse=False)
                mae_colors = get_color_code_for_row(mae_values, inverse=False)
                mcs_colors = get_color_code_for_row(mcs_values, inverse=True)
                
                f.write(f"{data['name']} & ")
                f.write(f"{rmse_colors[0]}{data['ls_rmse']:.3f} & ")
                f.write(f"{rmse_colors[1]}{data['ransac_rmse']:.3f} & ")
                f.write(f"{rmse_colors[2]}{data['lgbm_rmse']:.3f} & ")
                f.write(f"{rmse_colors[3]}{data['lgbm_ransac_rmse']:.3f} & ")
                f.write(f"{mae_colors[0]}{data['ls_mae']:.3f} & ")
                f.write(f"{mae_colors[1]}{data['ransac_mae']:.3f} & ")
                f.write(f"{mae_colors[2]}{data['lgbm_mae']:.3f} & ")
                f.write(f"{mae_colors[3]}{data['lgbm_ransac_mae']:.3f} & ")
                f.write(f"{mcs_colors[0]}{data['ls_mcs']:.3f} & ")
                f.write(f"{mcs_colors[1]}{data['ransac_mcs']:.3f} & ")
                f.write(f"{mcs_colors[2]}{data['lgbm_mcs']:.3f} & ")
                f.write(f"{mcs_colors[3]}{data['lgbm_ransac_mcs']:.3f} \\\\\n")
            else:
                f.write(f"{dataset_names[idx]} & - & - & - & - & - & - & - & - & - & - & - & - \\\\\n")
        
        f.write("\\hline\n")
        f.write("\\end{tabular}\n")
        f.write("}%\n")  # Close resizebox
        f.write("\\end{table}\n")
    
    print(f"Results table saved to {output_file}")


def create_confusion_matrix_table(datasets_all, results_all, output_file='confusion_matrices.tex'):
    """Create a LaTeX table with confusion matrices for RANSAC-based methods.
    
    Calculates True Positive, False Positive, True Negative, and False Negative rates
    for RANSAC and RANSAC+LightGBM methods in detecting outliers.
    """
    
    dataset_names = ['Linear (No)', 'Linear (Some)', 'Linear (Many)',
                     'Quadratic (No)', 'Quadratic (Some)', 'Quadratic (Many)',
                     'Exponential (No)', 'Exponential (Some)', 'Exponential (Many)']
    
    # Collect confusion matrix data
    confusion_data = []
    
    for idx, (dataset_name, (x, y, is_outlier)) in enumerate(zip(dataset_names, datasets_all)):
        print(f"  Computing confusion matrix for {dataset_name}...")
        
        if idx not in results_all:
            confusion_data.append(None)
            continue
        
        ls_model, ransac_model, lgbm_model, lgbm_ransac_model, model_type = results_all[idx]
        
        n_total = len(is_outlier)
        n_true_outliers = np.sum(is_outlier)
        n_true_inliers = n_total - n_true_outliers
        
        # Calculate metrics for RANSAC
        ransac_metrics = {'tp': 0, 'fp': 0, 'tn': 0, 'fn': 0}
        if ransac_model is not None:
            # Get RANSAC inlier mask
            if model_type == 'exponential' and isinstance(ransac_model, tuple):
                ransac_model_obj, _ = ransac_model
                if hasattr(ransac_model_obj, 'full_inlier_mask_'):
                    ransac_inlier_mask = ransac_model_obj.full_inlier_mask_
                else:
                    ransac_inlier_mask = np.ones(len(is_outlier), dtype=bool)
            elif hasattr(ransac_model, 'inlier_mask_'):
                ransac_inlier_mask = ransac_model.inlier_mask_
            else:
                ransac_inlier_mask = np.ones(len(is_outlier), dtype=bool)
            
            # RANSAC classifies as outlier = ~ransac_inlier_mask
            # True Positive: correctly identified outliers (is_outlier=True, classified as outlier)
            ransac_metrics['tp'] = np.sum(is_outlier & ~ransac_inlier_mask)
            # False Positive: incorrectly identified as outliers (is_outlier=False, classified as outlier)
            ransac_metrics['fp'] = np.sum(~is_outlier & ~ransac_inlier_mask)
            # True Negative: correctly identified inliers (is_outlier=False, classified as inlier)
            ransac_metrics['tn'] = np.sum(~is_outlier & ransac_inlier_mask)
            # False Negative: missed outliers (is_outlier=True, classified as inlier)
            ransac_metrics['fn'] = np.sum(is_outlier & ransac_inlier_mask)
        
        # Calculate metrics for RANSAC+LightGBM
        lgbm_ransac_metrics = {'tp': 0, 'fp': 0, 'tn': 0, 'fn': 0}
        if lgbm_ransac_model is not None and hasattr(lgbm_ransac_model, 'inlier_mask_'):
            lgbm_ransac_inlier_mask = lgbm_ransac_model.inlier_mask_
            
            lgbm_ransac_metrics['tp'] = np.sum(is_outlier & ~lgbm_ransac_inlier_mask)
            lgbm_ransac_metrics['fp'] = np.sum(~is_outlier & ~lgbm_ransac_inlier_mask)
            lgbm_ransac_metrics['tn'] = np.sum(~is_outlier & lgbm_ransac_inlier_mask)
            lgbm_ransac_metrics['fn'] = np.sum(is_outlier & lgbm_ransac_inlier_mask)
        
        # Calculate rates (percentages)
        def calc_rates(metrics, n_true_outliers, n_true_inliers):
            rates = {}
            # True Positive Rate (Sensitivity/Recall): TP / (TP + FN)
            if n_true_outliers > 0:
                rates['tpr'] = metrics['tp'] / n_true_outliers * 100
            else:
                rates['tpr'] = np.nan  # No outliers to detect
            
            # False Positive Rate: FP / (FP + TN)
            if n_true_inliers > 0:
                rates['fpr'] = metrics['fp'] / n_true_inliers * 100
            else:
                rates['fpr'] = np.nan
            
            # True Negative Rate (Specificity): TN / (TN + FP)
            if n_true_inliers > 0:
                rates['tnr'] = metrics['tn'] / n_true_inliers * 100
            else:
                rates['tnr'] = np.nan
            
            # False Negative Rate: FN / (FN + TP)
            if n_true_outliers > 0:
                rates['fnr'] = metrics['fn'] / n_true_outliers * 100
            else:
                rates['fnr'] = np.nan
            
            return rates
        
        ransac_rates = calc_rates(ransac_metrics, n_true_outliers, n_true_inliers)
        lgbm_ransac_rates = calc_rates(lgbm_ransac_metrics, n_true_outliers, n_true_inliers)
        
        confusion_data.append({
            'name': dataset_name,
            'n_outliers': n_true_outliers,
            'n_inliers': n_true_inliers,
            'ransac': ransac_rates,
            'lgbm_ransac': lgbm_ransac_rates
        })
    
    # Function to get color based on normalized value (0-100 scale)
    def get_color_code(value, inverse=False):
        """Return LaTeX color command for a single value on 0-100 scale.
        inverse=False: green for high values, red for low (TPR, TNR)
        inverse=True: red for high values, green for low (FPR, FNR)
        """
        if np.isnan(value):
            return ''
        
        # Normalize to 0-1 range (assuming values are 0-100%)
        norm = value / 100.0
        norm = max(0.0, min(1.0, norm))  # Clamp to [0, 1]
        
        if inverse:
            norm = 1 - norm  # Invert for error rates (lower is better)
        
        # Create color gradient: red (0) -> yellow (0.5) -> green (1)
        if norm < 0.5:
            # Red to yellow
            r = 255
            g = int(norm * 2 * 255)
        else:
            # Yellow to green
            r = int((1 - (norm - 0.5) * 2) * 255)
            g = 255
        
        return f"\\cellcolor[RGB]{{{r},{g},0}}"
    
    # Write LaTeX table
    with open(output_file, 'w') as f:
        f.write("\\begin{table}[htbp]\n")
        f.write("\\centering\n")
        f.write("\\caption{Confusion Matrix Metrics for RANSAC-based Methods. ")
        f.write("TPR: True Positive Rate, FPR: False Positive Rate, ")
        f.write("TNR: True Negative Rate, FNR: False Negative Rate. ")
        f.write("Values in \\%. Color coding: green indicates better performance, red indicates worse.}\n")
        f.write("\\label{tab:confusion_matrices}\n")
        f.write("\\resizebox{\\textwidth}{!}{%\n")
        f.write("\\begin{tabular}{|l|cc|cccc|cccc|}\n")
        f.write("\\hline\n")
        f.write("\\multirow{2}{*}{Dataset} & \\multicolumn{2}{c|}{Data} & ")
        f.write("\\multicolumn{4}{c|}{RANSAC} & \\multicolumn{4}{c|}{RANSAC+LightGBM} \\\\\n")
        f.write(" & Inliers & Outliers & TPR & FPR & TNR & FNR & TPR & FPR & TNR & FNR \\\\\n")
        f.write("\\hline\n")
        
        for data in confusion_data:
            if data is not None:
                # Format values, handling NaN
                def fmt(val, inverse=False):
                    if np.isnan(val):
                        return "-"
                    color = get_color_code(val, inverse=inverse)
                    return f"{color}{val:.1f}"
                
                f.write(f"{data['name']} & ")
                f.write(f"{data['n_inliers']} & {data['n_outliers']} & ")
                # RANSAC metrics
                f.write(f"{fmt(data['ransac']['tpr'], inverse=False)} & ")  # TPR: higher is better
                f.write(f"{fmt(data['ransac']['fpr'], inverse=True)} & ")   # FPR: lower is better
                f.write(f"{fmt(data['ransac']['tnr'], inverse=False)} & ")  # TNR: higher is better
                f.write(f"{fmt(data['ransac']['fnr'], inverse=True)} & ")   # FNR: lower is better
                # RANSAC+LightGBM metrics
                f.write(f"{fmt(data['lgbm_ransac']['tpr'], inverse=False)} & ")  # TPR: higher is better
                f.write(f"{fmt(data['lgbm_ransac']['fpr'], inverse=True)} & ")   # FPR: lower is better
                f.write(f"{fmt(data['lgbm_ransac']['tnr'], inverse=False)} & ")  # TNR: higher is better
                f.write(f"{fmt(data['lgbm_ransac']['fnr'], inverse=True)} \\\\\n")  # FNR: lower is better
            else:
                f.write("- & - & - & - & - & - & - & - & - & - & - \\\\\n")
        
        f.write("\\hline\n")
        f.write("\\end{tabular}\n")
        f.write("}%\n")
        f.write("\\end{table}\n")
    
    print(f"Confusion matrix table saved to {output_file}")


def main(seed=42):
    """Main function to generate all datasets, fit models, and create outputs."""
    # Set global random seed for reproducibility
    np.random.seed(seed)
    
    print("Generating datasets...")
    
    # Generate 9 datasets with controlled seeds
    datasets = []
    
    # Linear datasets
    datasets.append(generate_linear_data(n_points=100, n_outliers=0, seed=seed))
    datasets.append(generate_linear_data(n_points=80, n_outliers=20, seed=seed+1))
    datasets.append(generate_linear_data(n_points=50, n_outliers=50, seed=seed+2))
    
    # Quadratic datasets
    datasets.append(generate_quadratic_data(n_points=100, n_outliers=0, seed=seed+3))
    datasets.append(generate_quadratic_data(n_points=80, n_outliers=20, seed=seed+4))
    datasets.append(generate_quadratic_data(n_points=50, n_outliers=50, seed=seed+5))
    
    # Exponential datasets
    datasets.append(generate_exponential_data(n_points=100, n_outliers=0, seed=seed+6))
    datasets.append(generate_exponential_data(n_points=80, n_outliers=20, seed=seed+7))
    datasets.append(generate_exponential_data(n_points=50, n_outliers=50, seed=seed+8))
    
    print("Fitting models...")
    
    # Fit models to each dataset
    results = {}
    
    # Linear datasets (indices 0-2)
    for idx in range(3):
        x, y, is_outlier = datasets[idx]
        ls_model = fit_linear_least_squares(x, y)
        ransac_model = fit_linear_ransac(x, y, seed=seed+idx)
        lgbm_model = fit_lightgbm(x, y, seed=seed+idx)
        lgbm_ransac_model = fit_lightgbm_ransac(x, y, seed=seed+idx)
        results[idx] = (ls_model, ransac_model, lgbm_model, lgbm_ransac_model, 'linear')
    
    # Quadratic datasets (indices 3-5)
    for idx in range(3, 6):
        x, y, is_outlier = datasets[idx]
        ls_model = fit_quadratic_least_squares(x, y)
        ransac_model = fit_quadratic_ransac(x, y, seed=seed+idx)
        lgbm_model = fit_lightgbm(x, y, seed=seed+idx)
        lgbm_ransac_model = fit_lightgbm_ransac(x, y, seed=seed+idx)
        results[idx] = (ls_model, ransac_model, lgbm_model, lgbm_ransac_model, 'quadratic')
    
    # Exponential datasets (indices 6-8)
    for idx in range(6, 9):
        x, y, is_outlier = datasets[idx]
        ls_model = fit_exponential_least_squares(x, y)
        ransac_model = fit_exponential_ransac(x, y, seed=seed+idx)
        lgbm_model = fit_lightgbm(x, y, seed=seed+idx)
        lgbm_ransac_model = fit_lightgbm_ransac(x, y, seed=seed+idx)
        results[idx] = (ls_model, ransac_model, lgbm_model, lgbm_ransac_model, 'exponential')
    
    print("Creating visualizations and tables...")
    
    # Create three separate plots (one for each data type)
    # Linear datasets (indices 0-2)
    linear_datasets = datasets[0:3]
    linear_results = {i: results[i] for i in range(3)}
    plot_dataset_triplet(linear_datasets, linear_results, 'Linear', 
                        output_file=PATH_HERE / 'demo_results_linear.svg')
    
    # Quadratic datasets (indices 3-5)
    quadratic_datasets = datasets[3:6]
    quadratic_results = {i-3: results[i] for i in range(3, 6)}
    plot_dataset_triplet(quadratic_datasets, quadratic_results, 'Quadratic', 
                        output_file=PATH_HERE / 'demo_results_quadratic.svg')
    
    # Exponential datasets (indices 6-8)
    exponential_datasets = datasets[6:9]
    exponential_results = {i-6: results[i] for i in range(6, 9)}
    plot_dataset_triplet(exponential_datasets, exponential_results, 'Exponential', 
                        output_file=PATH_HERE / 'demo_results_exponential.svg')
    
    # Create results table
    create_results_table(datasets, results, output_file=PATH_HERE / 'results_table.tex')
    
    # Create confusion matrix table for RANSAC-based methods
    print("Creating confusion matrix table...")
    create_confusion_matrix_table(datasets, results, output_file=PATH_HERE / 'confusion_matrices.tex')
    
    print("Done! Check demo_results_*.pdf, results_table.tex, and confusion_matrices.tex")


if __name__ == "__main__":
    main()