const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, 
        HeadingLevel, AlignmentType, BorderStyle, WidthType, ShadingType, LevelFormat } = require('docx');
const fs = require('fs');

const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };

const doc = new Document({
  styles: {
    default: { 
      document: { 
        run: { font: "Arial", size: 24 } 
      } 
    },
    paragraphStyles: [
      { 
        id: "Heading1", 
        name: "Heading 1", 
        basedOn: "Normal", 
        next: "Normal", 
        quickFormat: true,
        run: { size: 32, bold: true, font: "Arial", color: "1F4788" },
        paragraph: { spacing: { before: 360, after: 240 }, outlineLevel: 0 }
      },
      { 
        id: "Heading2", 
        name: "Heading 2", 
        basedOn: "Normal", 
        next: "Normal", 
        quickFormat: true,
        run: { size: 28, bold: true, font: "Arial", color: "2E5C8A" },
        paragraph: { spacing: { before: 280, after: 180 }, outlineLevel: 1 }
      },
      { 
        id: "Heading3", 
        name: "Heading 3", 
        basedOn: "Normal", 
        next: "Normal", 
        quickFormat: true,
        run: { size: 26, bold: true, font: "Arial", color: "4A7BA7" },
        paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 }
      },
    ]
  },
  numbering: {
    config: [
      { 
        reference: "bullets",
        levels: [
          { 
            level: 0, 
            format: LevelFormat.BULLET, 
            text: "•", 
            alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } }
          }
        ]
      },
      { 
        reference: "numbers",
        levels: [
          { 
            level: 0, 
            format: LevelFormat.DECIMAL, 
            text: "%1.", 
            alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } }
          }
        ]
      }
    ]
  },
  sections: [{
    properties: {
      page: {
        size: {
          width: 12240,
          height: 15840
        },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    children: [
      // Title
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 240 },
        children: [
          new TextRun({
            text: "AyurMind: A Multi-Agent RAG Framework for Intelligent Ayurvedic Prakriti Assessment and Personalized Wellness Recommendations",
            bold: true,
            size: 32,
            font: "Arial"
          })
        ]
      }),

      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 480 },
        children: [
          new TextRun({
            text: "Research Proposal for MBCC 2026",
            size: 24,
            italics: true
          })
        ]
      }),

      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 480 },
        children: [
          new TextRun({
            text: "Conference Tracks: Ayurveda • Natural Language Processing for Indian Languages • Cognitive Science and AI",
            size: 22,
            color: "666666"
          })
        ]
      }),

      // Executive Summary
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("Executive Summary")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [
          new TextRun({
            text: "Problem: ",
            bold: true
          }),
          new TextRun("Ayurvedic diagnosis requires rare expert practitioners, and current AI systems hallucinate incorrect medical advice from ancient texts, making traditional knowledge inaccessible and unreliable for modern healthcare applications.")
        ]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [
          new TextRun({
            text: "Solution: ",
            bold: true
          }),
          new TextRun("We create an intelligent multi-agent system that accurately retrieves and reasons over Ayurvedic texts to provide personalized Prakriti assessment and treatment recommendations without hallucinations.")
        ]
      }),

      new Paragraph({
        spacing: { after: 480 },
        children: [
          new TextRun({
            text: "Method: ",
            bold: true
          }),
          new TextRun("Using specialized RAG-powered agents (Prakriti assessor, Dosha analyzer, Treatment recommender) coordinated by an orchestrator, all running on open-source Llama-3 models with ChromaDB vector storage of digitized Ayurvedic scriptures.")
        ]
      }),

      // Research Problem
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("1. Research Problem")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("1.1 Background")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [
          new TextRun("Ayurveda, a 5,000-year-old system of medicine rooted in Indian Knowledge Systems (IKS), offers holistic approaches to health and wellness. The core principle of Ayurvedic diagnosis involves determining an individual's Prakriti (constitutional type) and Vikriti (current imbalances) to provide personalized treatment recommendations.")
        ]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [
          new TextRun("However, accessing authentic Ayurvedic knowledge faces several critical challenges:")
        ]
      }),

      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [
          new TextRun({
            text: "Scarcity of Expert Practitioners: ",
            bold: true
          }),
          new TextRun("Qualified Ayurvedic doctors are limited, especially in rural areas, creating accessibility barriers for millions seeking traditional healthcare.")
        ]
      }),

      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [
          new TextRun({
            text: "AI Hallucination Problem: ",
            bold: true
          }),
          new TextRun("Large Language Models (LLMs) like GPT-4 and Claude generate plausible-sounding but factually incorrect Ayurvedic advice, potentially causing harm when users follow inaccurate recommendations.")
        ]
      }),

      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [
          new TextRun({
            text: "Knowledge Preservation: ",
            bold: true
          }),
          new TextRun("Ancient Ayurvedic texts (Charaka Samhita, Sushruta Samhita, Ashtanga Hridaya) contain invaluable wisdom but remain locked in Sanskrit and classical languages, inaccessible to modern practitioners and patients.")
        ]
      }),

      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        spacing: { after: 240 },
        children: [
          new TextRun({
            text: "Limited AI Integration: ",
            bold: true
          }),
          new TextRun("Existing Ayurvedic apps use rigid rule-based systems that lack the nuanced reasoning required for personalized diagnosis and treatment planning.")
        ]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("1.2 Research Gap")]
      }),

      new Paragraph({
        spacing: { after: 480 },
        children: [
          new TextRun("No existing system combines the retrieval accuracy of RAG (Retrieval-Augmented Generation) with the specialized reasoning capabilities of multi-agent architectures for Ayurvedic diagnosis. Current approaches either suffer from hallucinations (pure LLMs) or lack flexibility (rule-based systems).")
        ]
      }),

      // Proposed Solution
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("2. Proposed Solution: AyurMind")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("2.1 System Overview")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [
          new TextRun("AyurMind is a multi-agent RAG framework where specialized AI agents collaborate to provide holistic Ayurvedic consultations. Each agent is empowered with retrieval capabilities from authenticated Ayurvedic texts, ensuring factual accuracy while maintaining the reasoning flexibility of modern LLMs.")
        ]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("2.2 Architecture")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [
          new TextRun("The system consists of four specialized agents:")
        ]
      }),

      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [
          new TextRun({
            text: "Prakriti Assessor Agent: ",
            bold: true
          }),
          new TextRun("Determines the user's constitutional type (Vata, Pitta, Kapha, or combinations) by analyzing physical characteristics, behavioral patterns, and psychological traits through guided questioning.")
        ]
      }),

      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [
          new TextRun({
            text: "Dosha Imbalance Detector Agent: ",
            bold: true
          }),
          new TextRun("Identifies current health imbalances (Vikriti) by correlating reported symptoms with disease causation patterns documented in classical texts.")
        ]
      }),

      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [
          new TextRun({
            text: "Treatment Recommender Agent: ",
            bold: true
          }),
          new TextRun("Suggests personalized interventions including dietary modifications, lifestyle changes, herbal remedies, and therapeutic practices based on Prakriti-Vikriti analysis.")
        ]
      }),

      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        spacing: { after: 240 },
        children: [
          new TextRun({
            text: "Orchestrator Agent: ",
            bold: true
          }),
          new TextRun("Coordinates agent interactions, manages conversation flow, synthesizes recommendations from specialist agents, and presents holistic guidance to users.")
        ]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [
          new TextRun({
            text: "Key Innovation: ",
            bold: true,
            italics: true
          }),
          new TextRun("Unlike single-agent systems, our multi-agent architecture mirrors the collaborative diagnostic process in traditional Ayurvedic practice, where different aspects of health are analyzed independently before synthesis.")
        ]
      }),

      // System Architecture
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("3. System Architecture")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [
          new TextRun("The AyurMind system employs a layered architecture that separates concerns while enabling seamless integration between components. This section presents two complementary views of the system: the structural architecture showing component relationships, and the operational data flow showing runtime behavior.")
        ]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("3.1 Architectural Overview")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [
          new TextRun("The system architecture follows a six-layer design pattern, progressing from user interaction at the top to knowledge storage at the bottom. Each layer has well-defined responsibilities and interfaces:")
        ]
      }),

      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [
          new TextRun({
            text: "User Interface Layer: ",
            bold: true
          }),
          new TextRun("Provides bilingual (English/Hindi) web interface via Gradio, handles user input/output, manages conversation state.")
        ]
      }),

      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [
          new TextRun({
            text: "Orchestration Layer: ",
            bold: true
          }),
          new TextRun("Central coordinator that decomposes queries, delegates to specialist agents, and synthesizes responses into holistic recommendations.")
        ]
      }),

      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [
          new TextRun({
            text: "Specialized Agent Layer: ",
            bold: true
          }),
          new TextRun("Three domain-specific agents (Prakriti Assessor, Dosha Detector, Treatment Recommender) that perform focused reasoning with retrieved context.")
        ]
      }),

      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [
          new TextRun({
            text: "RAG Layer: ",
            bold: true
          }),
          new TextRun("Implements semantic retrieval pipeline using LangChain for document processing, sentence-transformers for embeddings, and ChromaDB for vector storage.")
        ]
      }),

      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [
          new TextRun({
            text: "Language Model Layer: ",
            bold: true
          }),
          new TextRun("Hosts Llama-3-8B (or Mistral-7B) via Ollama for local inference, shared by orchestrator and all specialist agents.")
        ]
      }),

      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        spacing: { after: 240 },
        children: [
          new TextRun({
            text: "Knowledge Base Layer: ",
            bold: true
          }),
          new TextRun("Contains processed and indexed Ayurvedic classical texts (Charaka Samhita, Sushruta Samhita, Ashtanga Hridaya) organized by topic and chapter.")
        ]
      }),

      new Paragraph({
        spacing: { after: 360 },
        children: [
          new TextRun({
            text: "Figure 1: System Architecture Diagram",
            bold: true,
            italics: true
          })
        ]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [
          new TextRun({
            text: "[See architecture_diagram.mermaid for complete structural view]",
            italics: true,
            color: "666666"
          })
        ]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [
          new TextRun("The architecture diagram illustrates component relationships and data pathways. Solid arrows represent primary data flow (queries, responses, retrieved content), while dashed arrows indicate LLM API calls. Color coding distinguishes functional layers: blue for user interface, orange for orchestration, green for specialized agents, purple for RAG infrastructure, pink for language models, and yellow for knowledge repositories.")
        ]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("3.2 Operational Data Flow")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [
          new TextRun("When a user submits a health query, the system executes a four-phase workflow orchestrated by the central coordination agent:")
        ]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [
          new TextRun({
            text: "Phase 1 - Constitutional Assessment:",
            bold: true
          })
        ]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [
          new TextRun("The Prakriti Assessor Agent analyzes physical and behavioral characteristics to determine the user's constitutional type. It queries the RAG pipeline for relevant text sections describing Vata, Pitta, and Kapha traits, then combines retrieved context with user information to generate a Prakriti classification. This assessment provides the foundation for personalized recommendations in subsequent phases.")
        ]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [
          new TextRun({
            text: "Phase 2 - Imbalance Detection:",
            bold: true
          })
        ]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [
          new TextRun("The Dosha Imbalance Detector correlates reported symptoms with disease causation patterns documented in classical texts. It retrieves sections on pathology, symptom manifestations, and diagnostic criteria. By synthesizing this knowledge with the user's symptom profile and constitutional type, the agent identifies current Dosha imbalances (Vikriti) and their severity.")
        ]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [
          new TextRun({
            text: "Phase 3 - Treatment Recommendation:",
            bold: true
          })
        ]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [
          new TextRun("The Treatment Recommender Agent generates personalized interventions based on Prakriti and Vikriti analysis. It retrieves therapeutic protocols, dietary guidelines, herbal formulations, and lifestyle practices specific to the identified imbalances. Recommendations are tailored to the user's constitution, ensuring compatibility and effectiveness.")
        ]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [
          new TextRun({
            text: "Phase 4 - Synthesis and Presentation:",
            bold: true
          })
        ]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [
          new TextRun("The Orchestrator synthesizes outputs from all three specialist agents into a coherent consultation report. It resolves any conflicts between recommendations, adds explanatory context, includes citations to source texts, and formats the response for user presentation. The final output provides holistic guidance addressing constitution, current state, and treatment path.")
        ]
      }),

      new Paragraph({
        spacing: { after: 360 },
        children: [
          new TextRun({
            text: "Figure 2: Data Flow Sequence Diagram",
            bold: true,
            italics: true
          })
        ]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [
          new TextRun({
            text: "[See dataflow_diagram.mermaid for complete operational sequence]",
            italics: true,
            color: "666666"
          })
        ]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [
          new TextRun("The sequence diagram traces a complete user interaction from query submission through multi-phase agent collaboration to final response delivery. Color-coded rectangles highlight distinct operational phases, while swim lanes show concurrent activities across system components. The diagram emphasizes the grounding mechanism: every agent decision point involves RAG retrieval, ensuring recommendations trace back to authenticated classical sources.")
        ]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("3.3 Key Architectural Decisions")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [
          new TextRun("Several design choices distinguish AyurMind from conventional AI health systems:")
        ]
      }),

      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [
          new TextRun({
            text: "Multi-Agent vs Single-Agent: ",
            bold: true
          }),
          new TextRun("Decomposition into specialized agents mirrors the Ayurvedic diagnostic process where constitution, imbalance, and treatment are evaluated through distinct analytical lenses. This specialization improves retrieval relevance and reasoning quality compared to monolithic single-agent approaches.")
        ]
      }),

      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [
          new TextRun({
            text: "RAG vs Fine-Tuning: ",
            bold: true
          }),
          new TextRun("While fine-tuning could adapt the base LLM to Ayurvedic domain, RAG offers critical advantages: no hallucinations (all outputs grounded in retrieved text), easy knowledge updates (add new texts without retraining), and explicit source attribution (users can verify recommendations). RAG addresses the core problem of AI hallucination in medical contexts.")
        ]
      }),

      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [
          new TextRun({
            text: "Local Deployment: ",
            bold: true
          }),
          new TextRun("Using Ollama for local LLM inference eliminates API costs, ensures patient privacy (no data leaves user's machine), enables offline operation, and makes the system accessible in resource-constrained settings. This aligns with the goal of democratizing Ayurvedic knowledge.")
        ]
      }),

      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        spacing: { after: 480 },
        children: [
          new TextRun({
            text: "Layered Architecture: ",
            bold: true
          }),
          new TextRun("Clear separation between UI, orchestration, agents, retrieval, and knowledge layers enables modular development, independent testing of components, and future extensibility (e.g., adding new agents for pulse diagnosis or replacing the LLM backend without affecting other layers).")
        ]
      }),

      // Technical Implementation
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("4. Technical Implementation")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("5.1 Technology Stack (Open Source)")]
      }),

      // Technology Table
      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [2800, 6560],
        rows: [
          new TableRow({
            children: [
              new TableCell({
                borders,
                width: { size: 2800, type: WidthType.DXA },
                shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ 
                  children: [new TextRun({ text: "Component", bold: true })] 
                })]
              }),
              new TableCell({
                borders,
                width: { size: 6560, type: WidthType.DXA },
                shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ 
                  children: [new TextRun({ text: "Technology", bold: true })] 
                })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders,
                width: { size: 2800, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("LLM")] })]
              }),
              new TableCell({
                borders,
                width: { size: 6560, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ 
                  children: [new TextRun("Llama-3-8B / Mistral-7B (via Ollama - local deployment)")] 
                })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders,
                width: { size: 2800, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("Agent Framework")] })]
              }),
              new TableCell({
                borders,
                width: { size: 6560, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ 
                  children: [new TextRun("LangGraph / CrewAI (multi-agent orchestration)")] 
                })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders,
                width: { size: 2800, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("RAG Framework")] })]
              }),
              new TableCell({
                borders,
                width: { size: 6560, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ 
                  children: [new TextRun("LangChain (document processing, retrieval pipeline)")] 
                })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders,
                width: { size: 2800, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("Vector Database")] })]
              }),
              new TableCell({
                borders,
                width: { size: 6560, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ 
                  children: [new TextRun("ChromaDB (semantic search over Ayurvedic texts)")] 
                })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders,
                width: { size: 2800, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("Embeddings")] })]
              }),
              new TableCell({
                borders,
                width: { size: 6560, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ 
                  children: [new TextRun("sentence-transformers (multilingual models for English/Hindi)")] 
                })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders,
                width: { size: 2800, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("User Interface")] })]
              }),
              new TableCell({
                borders,
                width: { size: 6560, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ 
                  children: [new TextRun("Gradio (interactive web interface with chat)")] 
                })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders,
                width: { size: 2800, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("Knowledge Base")] })]
              }),
              new TableCell({
                borders,
                width: { size: 6560, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ 
                  children: [new TextRun("Digitized Ayurvedic texts (Charaka Samhita, Sushruta Samhita, Ashtanga Hridaya - public domain translations)")] 
                })]
              })
            ]
          })
        ]
      }),

      new Paragraph({ text: "", spacing: { after: 240 } }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("5.2 RAG Pipeline Design")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_3,
        children: [new TextRun("Document Processing")]
      }),

      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [
          new TextRun({
            text: "Text Extraction: ",
            bold: true
          }),
          new TextRun("Convert PDF/HTML versions of Ayurvedic texts into structured plain text")
        ]
      }),

      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [
          new TextRun({
            text: "Semantic Chunking: ",
            bold: true
          }),
          new TextRun("Split texts into logical sections (slokas, chapters, treatment protocols) maintaining context boundaries")
        ]
      }),

      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [
          new TextRun({
            text: "Metadata Tagging: ",
            bold: true
          }),
          new TextRun("Annotate chunks with source text, chapter, topic (Prakriti/Vikriti/Treatment), and Sanskrit terms")
        ]
      }),

      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        spacing: { after: 240 },
        children: [
          new TextRun({
            text: "Vector Embedding: ",
            bold: true
          }),
          new TextRun("Generate semantic embeddings using multilingual sentence transformers, store in ChromaDB")
        ]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_3,
        children: [new TextRun("Retrieval Strategy")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [
          new TextRun("Each agent performs specialized retrieval:")
        ]
      }),

      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [
          new TextRun({
            text: "Prakriti Agent → ",
            bold: true
          }),
          new TextRun("Retrieves constitution definitions, characteristic traits")
        ]
      }),

      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [
          new TextRun({
            text: "Dosha Agent → ",
            bold: true
          }),
          new TextRun("Retrieves disease causation, symptom correlations")
        ]
      }),

      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        spacing: { after: 240 },
        children: [
          new TextRun({
            text: "Treatment Agent → ",
            bold: true
          }),
          new TextRun("Retrieves therapeutic protocols, dietary guidelines, herbal formulations")
        ]
      }),

      new Paragraph({
        spacing: { after: 480 },
        children: [
          new TextRun("Top-K retrieval (K=5) with relevance scoring ensures agents access most pertinent classical knowledge for each query.")
        ]
      }),

      // Research Methodology
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("5. Research Methodology")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("5.1 Dataset Preparation")]
      }),

      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [
          new TextRun({
            text: "Source Texts: ",
            bold: true
          }),
          new TextRun("Charaka Samhita (focus on Vimana Sthana, Chikitsa Sthana), Sushruta Samhita, Ashtanga Hridaya (English translations available in public domain)")
        ]
      }),

      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [
          new TextRun({
            text: "Test Cases: ",
            bold: true
          }),
          new TextRun("Develop 30 clinical scenarios covering various Prakriti types and common imbalances (e.g., Vata aggravation causing anxiety, Pitta imbalance causing acidity)")
        ]
      }),

      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        spacing: { after: 240 },
        children: [
          new TextRun({
            text: "Ground Truth: ",
            bold: true
          }),
          new TextRun("Consult 3-5 qualified Ayurvedic practitioners (BAMS degree holders with 5+ years experience) to provide expert diagnoses and treatment plans for test cases")
        ]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("5.2 Experimental Design")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [
          new TextRun("We conduct comparative evaluation across three conditions:")
        ]
      }),

      // Comparison Table
      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [2340, 2340, 2340, 2340],
        rows: [
          new TableRow({
            children: [
              new TableCell({
                borders,
                width: { size: 2340, type: WidthType.DXA },
                shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ 
                  children: [new TextRun({ text: "System", bold: true })] 
                })]
              }),
              new TableCell({
                borders,
                width: { size: 2340, type: WidthType.DXA },
                shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ 
                  children: [new TextRun({ text: "Architecture", bold: true })] 
                })]
              }),
              new TableCell({
                borders,
                width: { size: 2340, type: WidthType.DXA },
                shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ 
                  children: [new TextRun({ text: "Knowledge Source", bold: true })] 
                })]
              }),
              new TableCell({
                borders,
                width: { size: 2340, type: WidthType.DXA },
                shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ 
                  children: [new TextRun({ text: "Expected Issue", bold: true })] 
                })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders,
                width: { size: 2340, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ 
                  children: [new TextRun({ text: "Baseline: Vanilla LLM", bold: true })] 
                })]
              }),
              new TableCell({
                borders,
                width: { size: 2340, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("Single Llama-3")] })]
              }),
              new TableCell({
                borders,
                width: { size: 2340, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("Pre-training only")] })]
              }),
              new TableCell({
                borders,
                width: { size: 2340, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("Hallucinations")] })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders,
                width: { size: 2340, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ 
                  children: [new TextRun({ text: "Condition 2: Single-Agent RAG", bold: true })] 
                })]
              }),
              new TableCell({
                borders,
                width: { size: 2340, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("Single Llama-3")] })]
              }),
              new TableCell({
                borders,
                width: { size: 2340, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("RAG over texts")] })]
              }),
              new TableCell({
                borders,
                width: { size: 2340, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("Generic reasoning")] })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders,
                width: { size: 2340, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ 
                  children: [new TextRun({ text: "AyurMind: Multi-Agent RAG", bold: true })] 
                })]
              }),
              new TableCell({
                borders,
                width: { size: 2340, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("4 specialized agents")] })]
              }),
              new TableCell({
                borders,
                width: { size: 2340, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("Targeted RAG per agent")] })]
              }),
              new TableCell({
                borders,
                width: { size: 2340, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("Specialized + holistic")] })]
              })
            ]
          })
        ]
      }),

      new Paragraph({ text: "", spacing: { after: 240 } }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("5.3 Evaluation Metrics")]
      }),

      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [
          new TextRun({
            text: "Prakriti Classification Accuracy: ",
            bold: true
          }),
          new TextRun("Percentage agreement with expert-assigned constitutional types")
        ]
      }),

      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [
          new TextRun({
            text: "Treatment Relevance Score: ",
            bold: true
          }),
          new TextRun("Expert rating (1-5 scale) on appropriateness of dietary, lifestyle, and herbal recommendations")
        ]
      }),

      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [
          new TextRun({
            text: "Hallucination Rate: ",
            bold: true
          }),
          new TextRun("Percentage of recommendations not grounded in retrieved Ayurvedic texts")
        ]
      }),

      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [
          new TextRun({
            text: "Response Completeness: ",
            bold: true
          }),
          new TextRun("Coverage of diagnosis, reasoning, and treatment (binary checklist)")
        ]
      }),

      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        spacing: { after: 480 },
        children: [
          new TextRun({
            text: "Bilingual Performance: ",
            bold: true
          }),
          new TextRun("Accuracy comparison for English vs Hindi queries")
        ]
      }),

      // Expected Results
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("6. Expected Results")]
      }),

      // Results Table
      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [3120, 2080, 2080, 2080],
        rows: [
          new TableRow({
            children: [
              new TableCell({
                borders,
                width: { size: 3120, type: WidthType.DXA },
                shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ 
                  children: [new TextRun({ text: "Metric", bold: true })] 
                })]
              }),
              new TableCell({
                borders,
                width: { size: 2080, type: WidthType.DXA },
                shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ 
                  children: [new TextRun({ text: "Vanilla LLM", bold: true })] 
                })]
              }),
              new TableCell({
                borders,
                width: { size: 2080, type: WidthType.DXA },
                shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ 
                  children: [new TextRun({ text: "Single-Agent RAG", bold: true })] 
                })]
              }),
              new TableCell({
                borders,
                width: { size: 2080, type: WidthType.DXA },
                shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ 
                  children: [new TextRun({ text: "AyurMind", bold: true, color: "1F7B3E" })] 
                })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders,
                width: { size: 3120, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("Prakriti Accuracy")] })]
              }),
              new TableCell({
                borders,
                width: { size: 2080, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("45%")] })]
              }),
              new TableCell({
                borders,
                width: { size: 2080, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("68%")] })]
              }),
              new TableCell({
                borders,
                width: { size: 2080, type: WidthType.DXA },
                shading: { fill: "E8F5E9", type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ 
                  children: [new TextRun({ text: "78%", bold: true })] 
                })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders,
                width: { size: 3120, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("Treatment Relevance")] })]
              }),
              new TableCell({
                borders,
                width: { size: 2080, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("52%")] })]
              }),
              new TableCell({
                borders,
                width: { size: 2080, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("71%")] })]
              }),
              new TableCell({
                borders,
                width: { size: 2080, type: WidthType.DXA },
                shading: { fill: "E8F5E9", type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ 
                  children: [new TextRun({ text: "81%", bold: true })] 
                })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders,
                width: { size: 3120, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("Hallucination Rate")] })]
              }),
              new TableCell({
                borders,
                width: { size: 2080, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("38%")] })]
              }),
              new TableCell({
                borders,
                width: { size: 2080, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("8%")] })]
              }),
              new TableCell({
                borders,
                width: { size: 2080, type: WidthType.DXA },
                shading: { fill: "E8F5E9", type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ 
                  children: [new TextRun({ text: "<3%", bold: true })] 
                })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders,
                width: { size: 3120, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("Expert Agreement")] })]
              }),
              new TableCell({
                borders,
                width: { size: 2080, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("41%")] })]
              }),
              new TableCell({
                borders,
                width: { size: 2080, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun("64%")] })]
              }),
              new TableCell({
                borders,
                width: { size: 2080, type: WidthType.DXA },
                shading: { fill: "E8F5E9", type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ 
                  children: [new TextRun({ text: "73%", bold: true })] 
                })]
              })
            ]
          })
        ]
      }),

      new Paragraph({ text: "", spacing: { after: 480 } }),

      // Novel Contributions
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("7. Novel Contributions")]
      }),

      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [
          new TextRun({
            text: "First Multi-Agent Architecture for Ayurveda: ",
            bold: true
          }),
          new TextRun("Pioneering specialized agent decomposition for traditional medical diagnosis")
        ]
      }),

      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [
          new TextRun({
            text: "Open Ayurvedic Knowledge Base: ",
            bold: true
          }),
          new TextRun("Digitized, structured, and semantically indexed classical texts available to research community")
        ]
      }),

      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [
          new TextRun({
            text: "Validation Framework: ",
            bold: true
          }),
          new TextRun("Novel methodology for evaluating AI systems against traditional medical expertise")
        ]
      }),

      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [
          new TextRun({
            text: "IKS-AI Integration Blueprint: ",
            bold: true
          }),
          new TextRun("Replicable approach for applying modern AI to preserve and democratize ancient wisdom systems")
        ]
      }),

      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        spacing: { after: 480 },
        children: [
          new TextRun({
            text: "Bilingual Capability: ",
            bold: true
          }),
          new TextRun("Bridges language barriers between Sanskrit scholarship and contemporary Hindi/English speakers")
        ]
      }),

      // Timeline
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("8. Implementation Timeline")]
      }),

      // Timeline Table
      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [1560, 7800],
        rows: [
          new TableRow({
            children: [
              new TableCell({
                borders,
                width: { size: 1560, type: WidthType.DXA },
                shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ 
                  children: [new TextRun({ text: "Phase", bold: true })] 
                })]
              }),
              new TableCell({
                borders,
                width: { size: 7800, type: WidthType.DXA },
                shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ 
                  children: [new TextRun({ text: "Tasks", bold: true })] 
                })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders,
                width: { size: 1560, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ 
                  children: [new TextRun({ text: "Week 1-2", bold: true })] 
                })]
              }),
              new TableCell({
                borders,
                width: { size: 7800, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ 
                  children: [new TextRun("Data Collection & RAG Setup: Download Ayurvedic texts, process into chunks, create embeddings, build ChromaDB vector store, test basic retrieval")] 
                })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders,
                width: { size: 1560, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ 
                  children: [new TextRun({ text: "Week 3-4", bold: true })] 
                })]
              }),
              new TableCell({
                borders,
                width: { size: 7800, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ 
                  children: [new TextRun("Multi-Agent Development: Implement 4 agents using LangGraph/CrewAI, design prompts for specialized reasoning, build orchestrator coordination logic, create Gradio interface")] 
                })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders,
                width: { size: 1560, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ 
                  children: [new TextRun({ text: "Week 5", bold: true })] 
                })]
              }),
              new TableCell({
                borders,
                width: { size: 7800, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ 
                  children: [new TextRun("Expert Validation: Develop 30 test cases, consult Ayurvedic practitioners for ground truth, implement baseline systems (vanilla LLM, single-agent RAG)")] 
                })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders,
                width: { size: 1560, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ 
                  children: [new TextRun({ text: "Week 6-7", bold: true })] 
                })]
              }),
              new TableCell({
                borders,
                width: { size: 7800, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ 
                  children: [new TextRun("Experiments & Analysis: Run comparative evaluation across 3 conditions, compute metrics, perform ablation studies (effect of each agent, retrieval strategies), analyze failure cases")] 
                })]
              })
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders,
                width: { size: 1560, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ 
                  children: [new TextRun({ text: "Week 8", bold: true })] 
                })]
              }),
              new TableCell({
                borders,
                width: { size: 7800, type: WidthType.DXA },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ 
                  children: [new TextRun("Paper Writing: Draft manuscript, create visualizations (agent workflow diagram, result charts), prepare demo video, finalize submission")] 
                })]
              })
            ]
          })
        ]
      }),

      new Paragraph({ text: "", spacing: { after: 480 } }),

      // Conference Alignment
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("9. MBCC 2026 Conference Alignment")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [
          new TextRun({
            text: "This research perfectly aligns with MBCC 2026's mission to integrate Indian Knowledge Systems with cutting-edge technology:",
            italics: true
          })
        ]
      }),

      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [
          new TextRun({
            text: "Primary Track - Ayurveda: ",
            bold: true
          }),
          new TextRun("Core focus on digitizing and operationalizing Ayurvedic diagnostic principles")
        ]
      }),

      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [
          new TextRun({
            text: "Secondary Track - NLP for Indian Languages: ",
            bold: true
          }),
          new TextRun("Bilingual system supporting English and Hindi with Sanskrit terminology preservation")
        ]
      }),

      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [
          new TextRun({
            text: "Tertiary Track - Cognitive Science and AI: ",
            bold: true
          }),
          new TextRun("Novel multi-agent reasoning architecture for medical diagnosis")
        ]
      }),

      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        spacing: { after: 240 },
        children: [
          new TextRun({
            text: "Holistic Integration: ",
            bold: true
          }),
          new TextRun("Bridges empirical AI research with timeless IKS wisdom, fostering dialogue between disciplines")
        ]
      }),

      new Paragraph({
        spacing: { after: 480 },
        children: [
          new TextRun("The interdisciplinary nature of this work—combining computer science, traditional medicine, and knowledge preservation—exemplifies MBCC's vision of redefining consciousness and cognitive science studies through IKS integration.")
        ]
      }),

      // Impact & Future Work
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("10. Impact and Future Work")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("10.1 Immediate Impact")]
      }),

      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [
          new TextRun({
            text: "Healthcare Access: ",
            bold: true
          }),
          new TextRun("Democratizes Ayurvedic consultation for underserved populations")
        ]
      }),

      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [
          new TextRun({
            text: "Knowledge Preservation: ",
            bold: true
          }),
          new TextRun("Creates digital infrastructure preventing loss of traditional wisdom")
        ]
      }),

      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        spacing: { after: 240 },
        children: [
          new TextRun({
            text: "Research Tool: ",
            bold: true
          }),
          new TextRun("Enables systematic study of Ayurvedic principles through computational methods")
        ]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("10.2 Future Extensions")]
      }),

      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [
          new TextRun({
            text: "Fine-Tuning Layer: ",
            bold: true
          }),
          new TextRun("Add domain-specific fine-tuning on Ayurvedic clinical case studies for improved accuracy")
        ]
      }),

      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [
          new TextRun({
            text: "Additional Languages: ",
            bold: true
          }),
          new TextRun("Expand to Tamil, Bengali, Marathi, Telugu for pan-India accessibility")
        ]
      }),

      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [
          new TextRun({
            text: "Integration with Modern Medicine: ",
            bold: true
          }),
          new TextRun("Hybrid system combining Ayurvedic and allopathic recommendations with drug interaction checks")
        ]
      }),

      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        children: [
          new TextRun({
            text: "Clinical Trials: ",
            bold: true
          }),
          new TextRun("Partner with Ayurvedic hospitals to validate system recommendations through patient outcomes")
        ]
      }),

      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        spacing: { after: 480 },
        children: [
          new TextRun({
            text: "Generalization to Other IKS: ",
            bold: true
          }),
          new TextRun("Apply framework to Yoga therapy, Unani medicine, Traditional Chinese Medicine")
        ]
      }),

      // Conclusion
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("11. Conclusion")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [
          new TextRun("AyurMind represents a paradigm shift in how artificial intelligence can serve to preserve, democratize, and advance traditional knowledge systems. By combining the retrieval precision of RAG with the collaborative reasoning of multi-agent architectures, we address the critical dual challenge of hallucination prevention and specialized medical reasoning.")
        ]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [
          new TextRun("This work is not merely a technical contribution but a bridge between ancient wisdom and modern innovation—exactly the interdisciplinary vision that MBCC 2026 champions. The proposed system has immediate practical applications while opening new research directions in AI-augmented traditional medicine.")
        ]
      }),

      new Paragraph({
        spacing: { after: 480 },
        children: [
          new TextRun("We are confident that AyurMind will generate significant interest at MBCC 2026, spark meaningful discussions between IKS scholars and AI researchers, and inspire future work at the intersection of computational intelligence and timeless human knowledge.")
        ]
      }),

      // Appendix
      new Paragraph({
        heading: HeadingLevel.HEADING_1,
        children: [new TextRun("Appendix: Technical Details")]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("A. Sample Agent Prompts")]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [
          new TextRun({
            text: "Prakriti Assessor Agent:",
            bold: true
          })
        ]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [
          new TextRun({
            text: "\"You are an expert Ayurvedic practitioner specializing in Prakriti assessment. Based on the user's responses about physical characteristics (body frame, skin type, hair texture), mental tendencies (stress response, decision-making style), and behavioral patterns (appetite, sleep, energy levels), determine their constitutional type. Use the retrieved classical texts to support your assessment. Ask clarifying questions when needed. Provide assessment only after gathering sufficient information.\"",
            italics: true
          })
        ]
      }),

      new Paragraph({
        spacing: { after: 120 },
        children: [
          new TextRun({
            text: "Dosha Imbalance Detector Agent:",
            bold: true
          })
        ]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [
          new TextRun({
            text: "\"You are an Ayurvedic diagnostician identifying current health imbalances (Vikriti). Analyze the user's reported symptoms and correlate them with Dosha aggravation patterns from classical texts. Consider: digestive issues → Agni status, skin problems → Pitta/Kapha imbalance, anxiety/insomnia → Vata aggravation. Use retrieved text passages to justify your diagnosis. Indicate confidence level (definite/probable/possible).\"",
            italics: true
          })
        ]
      }),

      new Paragraph({
        heading: HeadingLevel.HEADING_2,
        children: [new TextRun("B. Code Repository Structure")]
      }),

      new Paragraph({
        spacing: { after: 240 },
        children: [
          new TextRun("Complete code will be released as open-source upon publication:")
        ]
      }),

      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("data/ - Processed Ayurvedic texts and embeddings")]
      }),

      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("src/rag/ - RAG pipeline (chunking, embedding, retrieval)")]
      }),

      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("src/agents/ - Multi-agent implementation (4 specialist agents + orchestrator)")]
      }),

      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("src/evaluation/ - Evaluation scripts and test cases")]
      }),

      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("app.py - Gradio web interface")]
      }),

      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        children: [new TextRun("requirements.txt - Python dependencies (all open-source)")]
      }),

      new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        spacing: { after: 480 },
        children: [new TextRun("README.md - Setup instructions and usage guide")]
      }),

      // Contact
      new Paragraph({
        spacing: { before: 360, after: 240 },
        alignment: AlignmentType.CENTER,
        children: [
          new TextRun({
            text: "For questions or collaboration inquiries, please contact:",
            size: 24
          })
        ]
      }),

      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [
          new TextRun({
            text: "[Your Name]",
            bold: true,
            size: 24
          })
        ]
      }),

      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [
          new TextRun({
            text: "[Your Email]",
            size: 24
          })
        ]
      }),

      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [
          new TextRun({
            text: "[Your Institution]",
            size: 24
          })
        ]
      })
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("/mnt/user-data/outputs/AyurMind_Research_Proposal_MBCC2026.docx", buffer);
  console.log("Document created successfully!");
});
