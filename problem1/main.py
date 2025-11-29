import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def main():
    # Define paths
    base_path = 'spaceship-titanic'
    train_path = os.path.join(base_path, 'train.csv')
    test_path = os.path.join(base_path, 'test.csv')
    submission_path = os.path.join(base_path, 'sample_submission.csv')

    # 1. Read files
    print("Loading data...")
    try:
        train_df = pd.read_csv(train_path)
        test_df = pd.read_csv(test_path)
        submission_df = pd.read_csv(submission_path)
    except FileNotFoundError as e:
        print(f"Error loading files: {e}")
        return

    # 2. Merge test with submission to get Transported column, then merge with train
    # Merge test and submission on PassengerId
    test_merged = pd.merge(test_df, submission_df, on='PassengerId')
    
    # Concatenate train and test_merged
    all_data = pd.concat([train_df, test_merged], ignore_index=True)
    
    # 3. Total quantity
    print(f"Total data quantity: {len(all_data)}")

    # 4. Find most correlated item with Transported
    # Convert boolean columns to numeric (0/1) for correlation
    # Identify boolean columns. Transported is one. CryoSleep and VIP are others.
    # We need to handle potential NaNs before conversion or let pandas handle it.
    
    # Convert Transported to int (True=1, False=0)
    if 'Transported' in all_data.columns:
        all_data['Transported'] = all_data['Transported'].astype(float)

    # Convert other potential boolean columns
    for col in ['CryoSleep', 'VIP']:
        if col in all_data.columns:
            all_data[col] = all_data[col].astype(float)

    # Select numeric columns only for correlation matrix
    numeric_df = all_data.select_dtypes(include=['number'])
    
    if 'Transported' in numeric_df.columns:
        corr_matrix = numeric_df.corr()
        transported_corr = corr_matrix['Transported'].drop('Transported') # Drop self correlation
        
        # Find the feature with the highest absolute correlation
        most_relevant = transported_corr.abs().idxmax()
        max_corr_val = transported_corr[most_relevant]
        
        print(f"Most correlated feature with Transported: {most_relevant} (Correlation: {max_corr_val:.4f})")
    else:
        print("Transported column not found for correlation analysis.")

    # 5. Age Graph (10s to 70s)
    # Create Age Groups
    def get_age_group(age):
        if pd.isna(age):
            return None
        if age < 10: return '0-9'
        elif age < 20: return '10s'
        elif age < 30: return '20s'
        elif age < 40: return '30s'
        elif age < 50: return '40s'
        elif age < 60: return '50s'
        elif age < 70: return '60s'
        elif age < 80: return '70s'
        else: return '80+'

    all_data['AgeGroup'] = all_data['Age'].apply(get_age_group)
    
    # Filter for requested groups: 10s, 20s, 30s, 40s, 50s, 60s, 70s
    target_groups = ['10s', '20s', '30s', '40s', '50s', '60s', '70s']
    plot_data = all_data[all_data['AgeGroup'].isin(target_groups)].copy()
    
    # Ensure the order of groups in the plot
    plot_data['AgeGroup'] = pd.Categorical(plot_data['AgeGroup'], categories=target_groups, ordered=True)
    
    # Plot
    plt.figure(figsize=(10, 6))
    sns.countplot(data=plot_data, x='AgeGroup', hue='Transported')
    plt.title('Transported Status by Age Group')
    plt.xlabel('Age Group')
    plt.ylabel('Count')
    plt.legend(title='Transported', labels=['False', 'True'])
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    output_img = 'age_transported_graph.png'
    plt.savefig(output_img)
    print(f"Graph saved to {output_img}")
    # plt.show() # Commented out for headless environment

if __name__ == "__main__":
    main()
