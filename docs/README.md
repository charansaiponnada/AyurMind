# Codebase documentation

`ayurmind_docs.pdf` is the built document — 59 pages covering every module in `src/`,
the ingestion pipeline, the evaluation harness, deployment, and a chapter listing
where the README and the code disagree.

## Source layout

```
docs/
├── ayurmind_docs.tex        preamble, palette, TikZ styles, listing styles
├── sections/
│   ├── 01_overview.tex      what the system is, the two query paths
│   ├── 02_layout.tex        repository map
│   ├── 03_setup.tex         install, env vars, the four-step pipeline
│   ├── 04_ingestion.tex     scraper + chunker + metadata
│   ├── 05_retrieval.tex     embeddings, ChromaDB, retriever
│   ├── 06_llm.tex           the four LLM clients and the fallback chain
│   ├── 07_agents.tex        BaseAgent, three specialists, orchestrator
│   ├── 08_ui.tex            Gradio wiring and the chat handler
│   ├── 09_deployment.tex    HF Spaces, Docker, local sharing
│   ├── 10_evaluation.tex    dataset, metrics, results
│   ├── 11_gaps.tex          README vs code, defect list
│   ├── 12_extending.tex     how to add an agent, provider, or source text
│   └── 13_appendix.tex      API reference, glossary, commit notes
└── ayurmind_docs.pdf        the build output
```

All diagrams are TikZ; the bar chart is pgfplots. Nothing is an external image, so the
document builds from a clean checkout with no asset directory.

## Building

Needs a LaTeX distribution with `tikz`, `pgfplots`, `tcolorbox`, `listings`,
`booktabs`, `tabularx`, `longtable`, `fancyhdr`, `titlesec` and `hyperref`.
Run twice so the table of contents and cross-references resolve.

```bash
pdflatex -interaction=nonstopmode ayurmind_docs.tex
pdflatex -interaction=nonstopmode ayurmind_docs.tex
```

On MiKTeX, add `--enable-installer` on the first run so missing packages install
without prompting.

## Keeping it accurate

Chapter 11 cites file paths and line numbers. When you change `src/`, that chapter is
the first thing to re-check — several of its entries are defects that a future commit
will fix, and a stale defect list is worse than none.
