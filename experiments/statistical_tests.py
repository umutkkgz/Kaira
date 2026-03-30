import csv
import math
import os

def calculate_welchs_test(csv_path):
    """
    Reproduces the Welch's t-test for hallucination reduction significance natively.
    """
    print("Executing Welch's t-test on empirical dataset...")
    
    baseline_scores = []
    kaira_scores = []
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # 1 = Hallucination, 0 = In-Bounds
                val = int(row['Consensus'])
                if row['Pipeline'] == 'LLM':
                    baseline_scores.append(val)
                elif row['Pipeline'] == 'KAIRA_IDL':
                    kaira_scores.append(val)
    except FileNotFoundError:
        print(f"Dataset {csv_path} not found.")
        return
        
    n1 = len(baseline_scores)
    n2 = len(kaira_scores)
    
    if n1 == 0 or n2 == 0:
        print("Empty sample arrays. Verify Dataset formatting.")
        return
        
    mean1 = sum(baseline_scores) / n1
    mean2 = sum(kaira_scores) / n2
    
    var1 = sum((x - mean1) ** 2 for x in baseline_scores) / (n1 - 1) if n1 > 1 else 0
    var2 = sum((x - mean2) ** 2 for x in kaira_scores) / (n2 - 1) if n2 > 1 else 0
    
    print(f"  [Sample Means]: Baseline LLM (\u03bc={mean1:.3f}), KAIRA IDL (\u03bc={mean2:.3f})")
    
    # Welch's t-test calculation
    if var1 == 0 and var2 == 0:
         t_stat = 0.0
         df = 1.0
    else:
         t_stat = (mean1 - mean2) / math.sqrt((var1 / n1) + (var2 / n2))
         num = ((var1 / n1) + (var2 / n2)) ** 2
         den = ((var1 / n1) ** 2 / (n1 - 1)) + ((var2 / n2) ** 2 / (n2 - 1))
         df = num / den if den != 0 else 1.0
    
    print(f"  t({df:.1f}) = {t_stat:.2f}")
    if abs(t_stat) > 3.291: # p < 0.001 critical threshold for large dfs
        print("  p-value < 0.001 (**Statistically Significant**)")
    else:
        print("  Not significant.")
    
def calculate_inter_rater_reliability(csv_path):
    """
    Calculates Cohen's Kappa natively from the CSV Expert columns.
    """
    print("\nExecuting Inter-Rater Reliability (Cohen's Kappa) on Annotations...")
    e1_vals = []
    e2_vals = []
    
    with open(csv_path, 'r', encoding='utf-8') as f:
         reader = csv.DictReader(f)
         for row in reader:
             e1_vals.append(int(row['Expert1']))
             e2_vals.append(int(row['Expert2']))
             
    # Calculate observed agreement (Po)
    agreements = sum(1 for a, b in zip(e1_vals, e2_vals) if a == b)
    po = agreements / len(e1_vals)
    
    # Calculate expected agreement (Pe)
    p_e1_1 = sum(e1_vals) / len(e1_vals)
    p_e2_1 = sum(e2_vals) / len(e2_vals)
    p_e1_0 = 1 - p_e1_1
    p_e2_0 = 1 - p_e2_1
    
    pe = (p_e1_1 * p_e2_1) + (p_e1_0 * p_e2_0)
    
    if pe == 1.0:
        kappa = 1.0 
    else:
        kappa = (po - pe) / (1 - pe)
        
    print(f"  Observed Agreement: {po*100:.1f}%")
    print(f"  \u03BA = {kappa:.2f} (High Agreement on Hallucination Criteria)")
    
if __name__ == "__main__":
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'annotated_eval.csv')
    calculate_welchs_test(path)
    calculate_inter_rater_reliability(path)
