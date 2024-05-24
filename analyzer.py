import pandas as pd
import os
import re

# Function to load reference data into a list of tuples
def load_reference_data(filename):
    ref_data = pd.read_csv(filename)
    ref_patterns = []
    for _, row in ref_data.iterrows():
        pattern = row['Pattern'].lower()
        category = row['Category']
        ref_patterns.append((pattern, category))
    return ref_patterns

# Function to categorize a transaction using the reference data with regex
def categorize_transaction(description, ref_patterns):
    description = description.lower()
    for pattern, category in ref_patterns:
        if re.search(pattern, description):
            return category
    return 'Other'

# Function to process all CSV files in a directory
def process_bank_statements(directory, reference_data_file, output_file):
    # Load reference data
    reference_patterns = load_reference_data(reference_data_file)
    
    # Initialize an empty DataFrame to hold all transactions
    all_transactions = pd.DataFrame()
    
    # Iterate over all CSV files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            df = pd.read_csv(file_path)
            
            # Assume the description column is named 'Description'
            df['Category'] = df['Description'].apply(lambda x: categorize_transaction(x, reference_patterns))
            
            # Append the categorized transactions to the all_transactions DataFrame
            all_transactions = pd.concat([all_transactions, df], ignore_index=True)
    
    # Save the combined and categorized transactions to a new CSV file
    all_transactions.to_csv(output_file, index=False)
    print(f"Transactions have been categorized and saved to '{output_file}'")

# Directory containing the bank statement CSV files
directory = '/Users/black-pearl/python_ws/statement_analyzer/bankstatements'

# Reference data file
reference_data_file = 'reference_data.csv'

# Output file
output_file = '/Users/black-pearl/python_ws/statement_analyzer/output/consolidated_categorized_bankstatements.csv'

# Process the bank statements
process_bank_statements(directory, reference_data_file, output_file)
