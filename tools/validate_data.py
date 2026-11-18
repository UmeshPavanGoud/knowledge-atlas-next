from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]
catalog=json.loads((ROOT/'data/catalog.json').read_text(encoding='utf-8'))
tax=json.loads((ROOT/'data/taxonomy.json').read_text(encoding='utf-8'))
paths=json.loads((ROOT/'data/pathways.json').read_text(encoding='utf-8'))
errors=[]; ids=set(); urls=set(); subject_ids={s['id'] for s in tax['subjects']}; domain_ids={d['id'] for d in tax['domains']}
for r in catalog:
    if not r.get('id') or r['id'] in ids: errors.append(f"missing/duplicate id: {r.get('id')}")
    ids.add(r.get('id'))
    if not r.get('url','').startswith(('http://','https://')): errors.append(f"invalid URL: {r.get('id')}")
    if r.get('url') in urls: errors.append(f"duplicate URL: {r.get('url')}")
    urls.add(r.get('url'))
    for s in r.get('subjects',[]):
        if s not in subject_ids: errors.append(f"unknown subject {s} in {r['id']}")
    for d in r.get('domain_ids',[]):
        if d not in domain_ids: errors.append(f"unknown domain {d} in {r['id']}")
for p in paths:
    for st in p['stages']:
        for rid in st['resource_ids']:
            if rid not in ids: errors.append(f"unknown resource {rid} in path {p['id']}")
if errors:
    print('VALIDATION FAILED')
    for e in errors: print(' -',e)
    sys.exit(1)
print(f"VALIDATION PASSED: {len(catalog)} resources, {len(subject_ids)} subjects, {len(domain_ids)} domains, {len(paths)} pathways; all resource and path references resolve.")
