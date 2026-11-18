from pathlib import Path
import json, re, collections
ROOT=Path(__file__).resolve().parents[1]
catalog=json.loads((ROOT/'data/catalog.json').read_text(encoding='utf-8'))
known={r['id'] for r in catalog}
paths=[]
for path in sorted((ROOT/'source-archive/pathways-original').glob('*.md')):
    lines=path.read_text(encoding='utf-8').splitlines()
    title=next((re.sub(r'^#\s*','',line).strip() for line in lines if line.startswith('# ')),path.stem.title())
    title=re.sub(r'^[^A-Za-z0-9]+','',title)
    description=''
    for i,line in enumerate(lines):
        if line.startswith('# '):
            description=next((x.strip() for x in lines[i+1:] if x.strip() and not x.lstrip().startswith(('>','#','- [ ]'))),'')
            break
    stages=[]; current=None
    for line in lines:
        match=re.match(r'^##\s+(?:\d+\.\s*)?(.+)',line)
        if match:
            if current: stages.append(current)
            current={'title':match.group(1).strip(),'resource_ids':[],'description':''}
        elif current:
            candidates=re.findall(r'`([a-z0-9]+(?:-[a-z0-9]+)*)`',line)
            candidates+=re.findall(r'\]\([^)]*#([a-z0-9]+(?:-[a-z0-9]+)*)\)',line)
            for rid in candidates:
                if rid in known and rid not in current['resource_ids']:
                    current['resource_ids'].append(rid)
            if line.strip() and not line.startswith(('-', '>','##','#')) and not current['description']:
                current['description']=line.strip()
    if current: stages.append(current)
    stages=[stage for stage in stages if stage['resource_ids'] or stage['description']]
    used={rid for stage in stages for rid in stage['resource_ids']}
    domain_counts=collections.Counter(d for r in catalog if r['id'] in used for d in r.get('domain_ids',[]))
    paths.append({'id':path.stem,'title':title,'description':description,'stages':stages,'domain_ids':[d for d,_ in domain_counts.most_common(3)],'resource_count':len(used),'stage_count':len(stages),'source_file':path.name})
(ROOT/'data/pathways.json').write_text(json.dumps(paths,ensure_ascii=False,indent=2),encoding='utf-8')
print(f"Rebuilt {len(paths)} pathways with {sum(p['resource_count'] for p in paths)} resource references. Run `python tools/validate_data.py` next.")
