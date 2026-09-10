# 🎓 Scriptorium : AI-Multi-Agent Academic Research Platform

 **Scriptorium AI** is a production-ready, multi-agent academic research platform built to automate rigorous literature reviews and stress-test academic claims. Powered by a custom Retrieval-Augmented Generation (RAG) pipeline and Google Gemini, it utilizes specialized AI sub-agents to execute deterministic research, compare methodologies, and simulate citation integrity. 

--- 
The platform features an ultra-premium spatial glassmorphism UI, a live Adversarial Agent Debate terminal, and hardware Biometric Authentication for a state-of-the-art user experience. Engineered under strict server constraints, it seamlessly integrates a FastAPI backend with a dynamic React frontend environment.

---

## 🌟 Showstopper Features

*   **🎙️ Adversarial Agent Debates (Live Terminal):** 
    Watch two specialized AI agents (*The Empirical Skeptic* vs. *The Theoretical Optimist*) engage in a live, timed debate to stress-test research claims before presenting a final synthesis.
*   **🕸️ Retraction Domino Effect Map:** 
    An interactive knowledge graph simulation. Trigger a "Retraction," and watch the visual system automatically track compromised citations cascading through downstream academic papers.
*   **👁️ Biometric Authentication HUD:** 
    A fully functional facial recognition login flow utilizing active hardware camera integration, a live scanning reticle, and secure environment state management.
*   **⌨️ Global Command Palette:** 
    Press `Ctrl + K` anywhere in the app to instantly access system commands, voice synthesis, and workspace navigation for professional-grade accessibility.
*   **🎨 Premium Editorial UI Design:** 
    Built entirely from scratch utilizing tailored Cream & Burgundy color palettes, dynamic liquid gradient backgrounds, and micro-animated spatial glassmorphism.

---

## 🏗️ System Architecture

### 1. Frontend (React + Vite)
### 2. Backend (FastAPI + Python)

---

## 🧠 Deep-Dive: AI & Multi-Agent Architecture

Unlike standard chatbots, **Scriptorium AI** is built on a complex *Multi-Agent Orchestration* framework. Instead of a single AI model trying to do everything, the backend dynamically delegates tasks to specialized, independent AI modules.

### The Agentic Ecosystem
1. **The Orchestrator Agent (The Brain):** 
   Intercepts the user's natural language query and uses deterministic logic algorithms to classify the intent (e.g., "Compare X and Y" vs. "Summarize X"). It then dynamically routes the workload to the correct sub-agent.
2. **The Research Agent (The Librarian):** 
   Executes standard academic queries. It builds context string structures from the database and forcefully grounds the LLM in source material to prevent AI hallucinations.
3. **The Comparison Agent (The Analyst):** 
   Designed explicitly to juxtapose multiple research papers. It automatically isolates methodologies, datasets, and limitations between papers to find research gaps.
4. **The Citation Agent (The Auditor):** 
   Formats and traces claims strictly to their DOI origins, ensuring flawless academic integrity.

### Advanced RAG (Retrieval-Augmented Generation) Pipeline
Scriptorium implements a production-grade RAG pipeline to ensure the AI only speaks absolute truth based on real academic data:
* **The Context Injection:** When a user asks a question, the backend searches the MongoDB catalog of clean academic datasets (originally sourced from the OpenAlex API).
* **Semantic Prompting:** The retrieved documents are forcefully injected into the Gemini Prompt via temporary memory. 
* **Hallucination Prevention:** The System Instructions strictly mandate the AI to cite its claims using bracketed citations `[Paper N]` pointing directly back to the grounded context array.

---

## 🎨 UI/UX: The Psychology of the Dashboard

The frontend was meticulously engineered to combat "AI Fatigue." Standard AI interfaces (like ChatGPT) are often visually sterile. Scriptorium introduces a high-end, editorial aesthetic aimed at making prolonged academic research visually stimulating.

* **Spatial Depth Mapping:** Using layered `backdrop-filter: blur()`, the application creates a sense of spatial hierarchy. Important modals (like the Biometric Scanner and Agent Debates) physically "float" above the background data.
* **Liquid Gradients:** The custom CSS keyframe animations slowly map a shifting `#FDFBF7` (Cream) and `#800020` (Burgundy) color profile behind the application, offering a premium, breathing interface.
* **Non-Blocking Architecture:** Despite heavy CSS computation, all animations are hardware-accelerated or isolated via `z-index` stacking contexts to ensure the user's cursor and typing inputs never lag or lock up.

---

## 📊 Dataset & Data Engineering

Scriptorium operates on rigorous academic datasets:
* **Source:** Originally pulled and aggregated via the `OpenAlex API`.
* **Sanitization pipeline:** A custom Python script (`clean_dataset.py`) parses raw TSV/CSV data, standardizes messy author arrays, purges null abstracts, and normalizes publication years.
* **Storage:** Cleaned metadata is dynamically loaded into a remote `MongoDB` Cluster, allowing the API to run lighting-fast `$regex` search algorithms under severe hardware memory limitations (sub-512MB RAM constraints).

