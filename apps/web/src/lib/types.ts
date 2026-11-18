export type Subject = { id: string; name: string }
export type Domain = { id: string; name: string; eyebrow: string; icon: string; description: string; color: string; count: number }
export type Resource = {
  id: string; name: string; category: string; description: string; difficulty: string; level: string;
  resource_type: string; kind: string; best_for: string; access: string; access_key: string; url: string;
  platform_type: string; verification_status: string; verification_level: string; verification_label: string;
  focus_area: string; notes: string; provenance: string[]; source_categories: string[];
  subjects: Subject[]; domain_ids: string[]
}
export type ResourceResponse = { items: Resource[]; total: number; limit: number; offset: number; has_more: boolean }
export type Facets = { domains: Domain[]; subjects: (Subject & { domain_id: string; count: number })[]; types: {id:string;count:number}[]; levels: {id:string;count:number}[]; access: {id:string;count:number}[]; verification: {id:string;count:number}[] }
export type PathStep = { position:number; title:string; description:string; resource_ids:string[]; resources:Resource[] }
export type Pathway = { id:string; title:string; description:string; domain_ids:string[]; resource_count:number; stage_count:number; steps?:PathStep[] }
export type Overview = { resource_count:number; domain_count:number; subject_count:number; pathway_count:number; video_resources:number; access_not_listed:number; page_checks_recorded:number; progress_storage:string }
export type KnowledgeMap = { nodes:{id:string;name:string;domain_id:string;count:number}[]; edges:{source:string;target:string;weight:number}[]; method:string }
