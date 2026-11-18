import { ArrowUpRight, Bookmark, BookOpen, Code2, GraduationCap, Globe2, PlayCircle, ShieldCheck, Sparkles } from 'lucide-react'
import type { Resource } from '../lib/types'

const iconByKind: Record<string, typeof BookOpen> = { book: BookOpen, course: GraduationCap, video: PlayCircle, documentation: Code2, interactive: Sparkles, website: Globe2, project: Code2, database: Globe2, community: Globe2 }
const kindLabel: Record<string,string> = { book:'BOOKS & TEXTS', course:'COURSES', video:'VIDEO', documentation:'DOCUMENTATION', interactive:'INTERACTIVE', website:'WEBSITES', project:'PROJECTS', database:'DATASETS & DATABASES', community:'COMMUNITIES' }
const levelLabel: Record<string,string> = { beginner:'Beginner', intermediate:'Intermediate', advanced:'Advanced', 'all-levels':'All levels', unknown:'Level not listed' }
export default function ResourceCard({ resource, saved, onSave, onOpen }: { resource:Resource; saved:boolean; onSave:()=>void; onOpen:()=>void }) {
  const Icon=iconByKind[resource.kind] || BookOpen
  return <article className="resource-card">
    <div className="resource-card-top"><span className="kind-label"><Icon size={13}/>{kindLabel[resource.kind] || resource.kind.toUpperCase()}</span><button className={`icon-button save-button ${saved?'is-saved':''}`} aria-label={saved?'Remove bookmark':'Save resource'} onClick={onSave}><Bookmark size={16} fill={saved?'currentColor':'none'}/></button></div>
    <button className="resource-title-button" onClick={onOpen}><h3>{resource.name}</h3><ArrowUpRight size={16}/></button>
    <p className="resource-description">{resource.description}</p>
    <div className="resource-tags">{resource.subjects.slice(0,3).map(s=><span className="tag" key={s.id}>{s.name}</span>)}{resource.subjects.length>3&&<span className="tag">+{resource.subjects.length-3}</span>}</div>
    <div className="resource-card-footer"><span>{levelLabel[resource.level] || 'Level not listed'}</span><span className="dot-separator"/><span>{resource.access_key==='free'?'Free':resource.access_key==='paid'?'Paid':resource.access_key==='mixed'?'Mixed access':'Access not listed'}</span><span className={`verification-dot trust-${resource.verification_level}`} title={resource.verification_label}><ShieldCheck size={13}/></span></div>
  </article>
}
