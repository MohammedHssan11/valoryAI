import json
import os

audit_results_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Archive/audit_results.json"))
with open(audit_results_path) as f:
    data = json.load(f)

for res in data['results']:
    print("="*60)
    print(res['case'])
    print(f"Latency: {res['latency_ms']:.2f} ms")
    resp = res['response'].get('data', {})
    
    engine = resp.get('engine_used', 'MISSING')
    reason = resp.get('routing_reason', 'MISSING')
    print(f"Engine: {engine} | Routing Reason: {reason}")
    
    exp = resp.get('explainability')
    if not exp:
        print("EXPLAINABILITY OBJECT MISSING!")
        continue
    
    router_exp = exp.get('router_explanation')
    print(f"Router Exp: {router_exp}")
    
    conf = exp.get('confidence_explanation', {})
    print(f"Confidence: {conf.get('confidence_level')} - {conf.get('confidence_reason')}")
    
    fair = exp.get('fairness_explanation', {})
    print(f"Fairness: Status={fair.get('status')} | Est={fair.get('estimated_value')} | Target={fair.get('asking_price')} | Diff={fair.get('difference_amount')} ({fair.get('difference_percentage')}%)")
    
    nar = exp.get('narrative_explanation', {})
    print(f"Narrative Summary: {nar.get('summary')}")
    print(f"Narrative Why: {nar.get('why_this_price')}")
    print(f"Narrative Strongest: {nar.get('strongest_factors')}")
    
    comps = exp.get('comparable_evidence', [])
    print(f"Comparables Used: {len(comps)} mapped")
    if comps:
        print(f"  First Comp: ID={comps[0].get('property_id')} Price={comps[0].get('price')} Dist={comps[0].get('distance_km')} Size={comps[0].get('size_sqm')}")
        
    drivers = exp.get('feature_drivers', [])
    print(f"Feature Drivers: {len(drivers)} mapped")
    for d in drivers:
        print(f"  - {d.get('name')}: {d.get('direction')} ({d.get('strength')})")

print("="*60)
print("PERFORMANCE")
print(data['metrics'])
