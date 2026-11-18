from pathlib import Path
import json, yaml
ROOT=Path(__file__).resolve().parents[1]
raw=yaml.safe_load((ROOT/'source-archive/catalog-original.yaml').read_text(encoding='utf-8'))
tax=json.loads((ROOT/'data/taxonomy.json').read_text(encoding='utf-8'))
aliases=tax.get('aliases',{})
subject_ids={s['id'] for s in tax['subjects']}
subject_to_domain={s['id']:s['domain_id'] for s in tax['subjects']}
rows=[]
for source in raw:
    r=dict(source)
    r['source_file']=r.pop('archive_source_file','archive')
    r['subjects_original']=list(r.get('subjects',[]))
    r['subjects']=list(dict.fromkeys(aliases.get(s,s) for s in r.get('subjects',[])))
    r['subjects']=[s for s in r['subjects'] if s in subject_ids]
    r['domain_ids']=list(dict.fromkeys(subject_to_domain[s] for s in r['subjects']))
    value=str(r.get('difficulty','')).lower()
    if not value or value=='unknown': level='unknown'
    elif 'beginner' in value and 'advanced' in value: level='all-levels'
    elif 'beginner' in value: level='beginner'
    elif 'advanced' in value or 'graduate' in value: level='advanced'
    elif 'undergraduate' in value or 'intermediate' in value: level='intermediate'
    elif 'all levels' in value or value=='mixed': level='all-levels'
    else: level='unknown'
    r['level']=level
    platform=str(r.get('platform_type','')).lower()
    r['kind']={'youtube':'video','book':'book','university':'course','online-course':'course','website':'website','interactive':'interactive','documentation':'documentation','discovery':'community','project-learning':'project','github':'project','database':'database'}.get(platform,'other')
    access=str(r.get('access','Unknown')).lower()
    r['access_key']='free' if access=='free' or access=='online reading' else 'paid' if access=='paid' else 'mixed' if access.startswith('mixed') or 'paid' in access else 'unknown'
    verification=str(r.get('verification_status','')).lower()
    if 'not-independently-verified' in verification or 'not independently verified' in verification:
        r['verification_level']='upstream-only'; r['verification_label']='Source-index entry · destination not independently checked'
    elif 'verification pending' in verification or 'pending' in verification:
        r['verification_level']='pending'; r['verification_label']='Direct destination check pending'
    elif 'about page checked' in verification:
        r['verification_level']='page-check-recorded'; r['verification_label']='Page check recorded in source notes'
    elif 'reviewed-in-source-pdf' in verification or 'recorded-in-source-pdf' in verification:
        r['verification_level']='source-reviewed'; r['verification_label']='Recorded or reviewed in supplied source material'
    else:
        r['verification_level']='source-identified'; r['verification_label']='Identified in a source index; live status not guaranteed'
    rows.append(r)
(ROOT/'data/catalog.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(f"Rebuilt {len(rows)} catalog records. Run `python tools/validate_data.py` next.")
