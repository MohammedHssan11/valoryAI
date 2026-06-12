import pandas as pd
import os
import glob

# Define the directory containing your jsonl files
input_dir = 'data_eg'
output_dir = 'csv_output'

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Find all .jsonl files (ignoring .checkpoint files to avoid duplicates/noise)
files = [f for f in glob.glob(f"{input_dir}/*.jsonl") if "checkpoint" not in f]

for file_path in files:
    # Get the filename without extension
    file_name = os.path.basename(file_path).replace('.jsonl', '')
    
    print(f"Converting {file_name}...")
    
    try:
        # Read JSONL file
        # lines=True is required for .jsonl format
        df = pd.read_json(file_path, lines=True)
        
        # Define output path
        csv_path = os.path.join(output_dir, f"{file_name}.csv")
        
        # Export to CSV
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"Successfully saved to: {csv_path}")
        
    except Exception as e:
        print(f"Failed to convert {file_name}: {e}")

print("\nAll conversions complete!")