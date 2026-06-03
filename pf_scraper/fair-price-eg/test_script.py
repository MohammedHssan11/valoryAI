import os

with open('backend/app/api/routes/pricing.py') as f:
    lines = f.readlines()

with open('backend/app/api/routes/pricing.py', 'w') as f:
    in_explain = False
    for line in lines:
        if 'with timed_span(\"explainability_ms\"):' in line:
            in_explain = True
            f.write(line[4:])
            continue
        if in_explain and line.startswith('        '):
            f.write(line[4:])
            continue
        if in_explain and line.strip() != '' and not line.startswith('        '):
            in_explain = False
        f.write(line)
