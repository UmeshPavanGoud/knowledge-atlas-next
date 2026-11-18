# Taxonomy design

The navigation layer uses eight broad domains. Each resource retains precise subject tags and may belong to several subjects. This allows interdisciplinary resources to be found in several contexts without duplicating the resource record.

| Domain | Subjects |
|---|---|
| Mathematical Thinking | Mathematics |
| Natural Sciences | Physics & Astronomy; Chemistry |
| Computing & Software | Programming; Computer Science; Web & Application Development; Database Systems |
| AI & Data | Artificial Intelligence & Machine Learning; Data Science |
| Engineering Systems | Electrical & Electronics; Semiconductors & VLSI; Robotics & Embedded Systems; Aerospace & Space Science; Automotive Engineering; Manufacturing & Materials |
| Security & Digital Infrastructure | Cybersecurity & Cryptography; Computing Tools & Productivity |
| Creative & Interactive Technology | Game Development; Computer Graphics & VFX; Digital Media & Creative Tools |
| Research & Professional Growth | Career & Professional Skills |

## Why this is different

- Domains are broad entry points, not exhaustive academic departments.
- Subjects remain visible as filters and can be expanded over time.
- Provider/platform is a property of a resource, not a top-level navigation tree.
- Free-text resource descriptions and provider categories are retained for detail and search, but they are not used as unbounded filter taxonomies.
- The source's `databases` tag is treated as an alias for `database-systems`; original labels remain preserved in `subjects_original`.

## Future change policy

New top-level domains should be rare. Prefer adding or refining subject tags. An alias must be explicit, reviewed, and non-destructive. Do not infer a subject relationship from a title alone.
