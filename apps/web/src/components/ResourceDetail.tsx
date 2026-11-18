import { useEffect, useState } from 'react'
import { ArrowUpRight, Bookmark, ExternalLink, ShieldAlert, X } from 'lucide-react'
import { request } from '../lib/api'
import type { Resource } from '../lib/types'
export default function ResourceDetail({resource,saved,onSave,onClose,onSelectRelated}:{resource:Resource;saved:boolean;onSave:()=>void;onClose:()=>void;onSelectRelated:(resource:Resource)=>void}) {
 const [related,setRelated]=useState<Resource[]>([])
 useEffect(()=>{let active=true;request<{items:Resource[]}>(`/api/v1/resources/${resource.id}/related`).then(data=>{if(active)setRelated(data.items)}).catch(()=>{if(active)setRelated([])});return()=>{active=false}},[resource.id])
 return <div className="drawer-backdrop" role="presentation" onMouseDown={e=>{if(e.target===e.currentTarget)onClose()}}><aside className="resource-drawer" role="dialog" aria-modal="true" aria-label={`${resource.name} details`}>
  <div className="drawer-header"><span className="overline">RESOURCE PROFILE</span><button className="icon-button" onClick={onClose} aria-label="Close details"><X size={19}/></button></div>
  <div className="drawer-content"><div className="drawer-icon"><span>✳</span></div><div className="kind-label">{resource.category}</div><h2>{resource.name}</h2><p className="drawer-description">{resource.description}</p>
   <div className="drawer-actions"><a className="button button-primary" href={resource.url} target="_blank" rel="noreferrer">Open learning resource <ExternalLink size={15}/></a><button className={`button button-secondary ${saved?'is-saved':''}`} onClick={onSave}><Bookmark size={15} fill={saved?'currentColor':'none'}/>{saved?'Saved':'Save'}</button></div>
   <section className="detail-section"><h4>Why it may be useful</h4><p>{resource.best_for || 'The catalog does not yet contain a specific use note.'}</p></section>
   {resource.focus_area&&<section className="detail-section"><h4>Focus area</h4><p>{resource.focus_area}</p></section>}
   {related.length>0&&<section className="detail-section"><h4>Related discoveries</h4><p className="related-hint">Connected by shared subject tags in the catalog.</p><div className="related-list">{related.slice(0,5).map(item=><button className="related-resource" key={item.id} onClick={()=>onSelectRelated(item)}><span>{item.name}</span><ArrowUpRight size={13}/></button>)}</div></section>}
   <section className="detail-section"><h4>Classification</h4><div className="detail-tags">{resource.subjects.map(s=><span className="tag" key={s.id}>{s.name}</span>)}</div><div className="detail-meta"><div><span>Difficulty</span><strong>{resource.difficulty}</strong></div><div><span>Format</span><strong>{resource.resource_type}</strong></div><div><span>Access</span><strong>{resource.access}</strong></div><div><span>Provider type</span><strong>{resource.platform_type}</strong></div></div></section>
   <section className="trust-panel"><div className="trust-icon"><ShieldAlert size={17}/></div><div><strong>Catalog confidence</strong><p>{resource.verification_label}. A listing is a discovery pointer, not an endorsement or a guarantee that a provider's content, price or availability is unchanged.</p></div></section>
   {resource.notes&&<section className="detail-section"><h4>Curator notes</h4><p>{resource.notes}</p></section>}
   <section className="detail-section"><h4>Source trail</h4><ul className="provenance-list">{resource.provenance.map((p,i)=><li key={i}>{p}</li>)}</ul></section>
   <div className="resource-id">ATLAS ID <code>{resource.id}</code></div>
  </div></aside></div>
}
