# Product vision and experience specification

## North star

**Atlas helps a learner move from curiosity to capability.** The first interaction should answer “where do I begin?” without requiring the user to understand the repository's taxonomy.

## Primary user journeys

### 1. I am curious about a topic

Open Discover → search naturally → browse results → filter by format, subject, access and level → inspect the source confidence → open the provider's destination.

### 2. I want a sequence, not a pile of links

Open Learning Paths → select a route → work through stages → open the stage resources → mark progress locally. A pathway is guidance, not a rigid syllabus or a claim that every step is required.

### 3. I want to connect disciplines

Open Knowledge Map → inspect the broad domains and precise subjects → discover intersections derived from multi-subject catalog records. The app labels the graph's limits, and does not present co-occurrence as prerequisite evidence.

### 4. I want to keep useful resources

Bookmark items into Saved. The first release stores bookmarks and pathway progress in browser local storage. No account is needed and no personal learning history is sent to the server.

## Navigation model

- **Discover** — intent-oriented home, universal search, eight broad fields and selected pathways.
- **Explore library** — one canonical search experience with filters.
- **Learning paths** — structured routes and local progress.
- **Knowledge map** — cross-disciplinary discovery.
- **Saved resources** — browser-local collection.

A field card is an entry point into Explore with the domain filter selected; it is not a second independent resource index. A resource keeps one canonical ID even if it appears under multiple subjects.

## Content-card requirements

Every result card shows a clear format, title, useful short description, subject tags, level (including “not listed”), access (including “not listed”) and a source-confidence indicator. Details show the original source status, provenance, curator note and destination.

## Visual language

The implementation uses a dark-first editorial interface, restrained violet/teal accents, clear typography, compact metadata, generous spacing and responsive cards. The palette is decorative, not a semantic quality rating. A light theme is included. The interface is designed around fast scanning and predictable actions rather than dashboard clutter.

## Product honesty

- Do not call a URL “verified” solely because it exists in YAML.
- Do not display popularity, ratings, rankings or “best” scores without a defined and defensible source.
- Do not label the recommendation endpoint as AI; it is a transparent shared-subject match.
- Do not fabricate course duration, price, language, prerequisites, certificate or completion claims when metadata is absent.
- Do not claim the knowledge map is a prerequisite graph; its edges only mean that a catalog record carries both subject tags.
