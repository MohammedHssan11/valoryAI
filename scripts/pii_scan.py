import os
import json
import pandas as pd
import re

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
data_dir = os.path.join(ROOT_DIR, "pf_scraper", "data_eg")
files_to_scan = ['all_egypt.jsonl', 'commercial_buy.jsonl', 'commercial_rent.jsonl']

# Regex patterns
patterns = {
    'Email': r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
    'Phone': r'(?:\+20|0020|0)?1[0125]\d{8}', # Egypt phone numbers specifically
    'WhatsApp Link': r'(?:wa\.me|api\.whatsapp\.com|chat\.whatsapp\.com)',
    'Contact Keyword': r'(?i)(?:call|contact|agent|whatsapp|broker|company)'
}

results = []

for filename in files_to_scan:
    filepath = os.path.join(data_dir, filename)
    if not os.path.exists(filepath):
        continue
    
    print(f"Scanning {filename}...")
    try:
        # Load sample to avoid memory crash, or full if possible. Let's do a large random sample or full.
        # Since we just want existence proof, scanning first 10,000 rows is extremely indicative.
        # But let's try full since it's 60MB.
        df = pd.read_json(filepath, lines=True)
        
        # We need to flatten nested dicts/lists to strings for regex searching
        for col in df.columns:
            # We don't need to scan numeric IDs, lat/lng, price, etc for emails/phones
            if col in ['id', 'latitude', 'longitude', 'price', 'price_raw_value', 'bedrooms', 'bathrooms', 'size']:
                continue
                
            col_data = df[col].astype(str)
            
            for p_name, regex in patterns.items():
                matches = col_data[col_data.str.contains(regex, regex=True, na=False)]
                if not matches.empty:
                    # extract actual matching substring if possible
                    sample_text = matches.iloc[0]
                    
                    # For phone/email/wa we extract the match. For keywords we just show context
                    match_obj = re.search(regex, sample_text)
                    if match_obj:
                        val = match_obj.group(0)
                        
                        # Redact
                        if p_name == 'Email':
                            parts = val.split('@')
                            redacted = parts[0][:2] + "***@" + parts[1]
                        elif p_name in ['Phone', 'WhatsApp Link']:
                            redacted = val[:4] + "***" + val[-2:]
                        else:
                            # Just show a bit of the surrounding context for contact/agent keywords
                            idx = sample_text.lower().find(val.lower())
                            ctx = sample_text[max(0, idx-15):min(len(sample_text), idx+30)]
                            redacted = f"...{ctx}..."
                            
                        # If the keyword matched 'location' or 'category' natively, skip
                        if p_name == 'Contact Keyword' and col in ['category', 'property_type']:
                            continue
                            
                        results.append({
                            'Dataset': filename,
                            'Column': col,
                            'Pattern': p_name,
                            'Example': redacted,
                            'Risk': 'HIGH' if p_name in ['Email', 'Phone', 'WhatsApp Link'] else 'MEDIUM'
                        })
                        # Break out of this pattern for this column (we just need one proof)
                        # We continue to next pattern
    except Exception as e:
        print(f"Error scanning {filename}: {e}")

print("\n--- RESULTS ---")
# Deduplicate similar results
seen = set()
for r in results:
    key = (r['Dataset'], r['Column'], r['Pattern'])
    if key not in seen:
        print(f"Dataset: {r['Dataset']} | Column: {r['Column']} | Type: {r['Pattern']} | Redacted: {r['Example']} | Risk: {r['Risk']}")
        seen.add(key)
