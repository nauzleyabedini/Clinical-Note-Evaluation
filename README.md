# AI-Powered Clinical Documentation Evaluation Harness

## Executive Summary ##

This project aims to build a comprehensive LLM-as-a-Judge pipeline for evaluating AI-generated clinical notes, comparing two frontier models (OpenAI `GPT-4o-mini` and Anthropic `Claude-3.5-Sonnet`) against human expert evaluations. 

## 🚀 Quick Start & Datasets
All resources to replicate this study are in our [GitHub Repository](https://github.com/nauzleyabedini/Clinical-Note-Evaluation/).
* **Note Data:** [ACI-BENCH Transcripts](https://raw.githubusercontent.com/microsoft/clinical_visit_note_summarization_corpus/refs/heads/main/data/aci-bench/challenge_data/train.csv) | [AI Notes Full (67)](https://raw.githubusercontent.com/nauzleyabedini/Clinical-Note-Evaluation/main/Data/full_dataset_with_ai_notes.csv) | [AI Notes Pilot (10)](https://raw.githubusercontent.com/nauzleyabedini/Clinical-Note-Evaluation/main/Data/experimental_dataset_with_ai_notes.csv)
* **Evaluation Data:** [Human Benchmark (10)](https://raw.githubusercontent.com/nauzleyabedini/Clinical-Note-Evaluation/main/Data/human_evaluation.csv) | [Aggregated Pilot Results](https://raw.githubusercontent.com/nauzleyabedini/Clinical-Note-Evaluation/main/Data/aggregated_experimental_evaluation_results_v2_4_modules.csv)
* **Code & Prompts:** [GitHub Prompts & Utils](https://github.com/nauzleyabedini/Clinical-Note-Evaluation/tree/main)
* **Rubric & Scoring System:** [Note Audit Rubric v2](https://github.com/nauzleyabedini/Clinical-Note-Evaluation/blob/main/Rubrics/Note_Audit_Rubric_v2.md)

## Methods ##

### 1. Dataset and AI-generated note corpus
I utilized the **ACI-BENCH dataset**, a corpus of ground-truth, simulated patient-clinician transcripts and corresponding, gold-standard clinical notes. 
- **Full Dataset (N=67):** Used to establish baseline performance metrics and failure rates for the LLM judges.
- **Experimental/Pilot Dataset (N=10):** A subset of encounters used for initial human-expert validation, prompt debugging, and pipeline alignment.
AI-generated draft notes were synthesized for each encounter using a baseline generative model (e.g., Gemini) to serve as the evaluation targets.

### 2. LLM Evaluation Pipeline (LLM-as-a-Judge)
I implemented an automated, 4-module evaluation pipeline to assess the quality of the AI-generated notes against the original transcripts and gold-standard notes. The evaluation was conducted using two frontier models: **OpenAI GPT-4o-mini** (optimizing for cost/efficiency) and **Anthropic Claude-3.5-Sonnet** (optimizing for rigor). 
The four modules evaluated:
1.  **Fact Grounding & Clinical Safety:** Detecting critical omissions and hallucinations.
2.  **Clinical Reasoning:** Identifying contradictions and logical misattributions.
3.  **Coding, Billing & Compliance:** Validating ICD-10 specificity, unsubstantiated diagnoses, and HCC/MEAT criteria.
4.  **Structure & Usability:** Subjective scoring of note organization and overall pass/fail judgment.
 
### 3. Human Expert Baseline
To assess baseline performance of the LLM judges, a **Human Expert** evaluated the experimental subset (N=10) using the same rubric. This established a baseline for clinical safety heuristics, compliance strictness, and qualitative formatting preferences to inform future LLM judge prompt fine-tuning.

### 4. Analysis Techniques
-   **Quantitative Analysis:** We calculated **Cohen's Kappa** to measure Inter-Rater Reliability (IRR) between each LLM judge and the human expert across binary and ordinal metrics (e.g., Critical Safety Error presence, Overall Note Pass).

## 📊 Results

### 1. Initial LLM Baseline (Full Dataset, N=67)
* **Anthropic (Claude-Sonnet-5):** Extremely strict (70.1% fail rate). Excellent at catching compliance/billing errors (HCC/MEAT) but overly sensitive.
* **OpenAI (GPT-4o-mini):** Lenient (46.3% fail rate). Missed the vast majority of unsubstantiated diagnoses and compliance risks.

### 2. Human Validation Pilot (Experimental Dataset, N=10)
*I ran this comparison on a smaller sample size (N=10) to conduct prompt debugging, qualitative alignment, and pipeline validation before scaling up. In the next iteration, I will use the full dataset with fine-tuned prompts.*

**Key Findings:**
* **OpenAI** aligns better with humans on **Safety** (Kappa=0.40) and overall pass rate but completely fails on **Compliance** (Kappa=-0.11).
* **Anthropic** aligns better on **Compliance** (Kappa=0.41) but misses human nuance on **Safety** (Kappa=0.00).

![Average Scores](https://raw.githubusercontent.com/nauzleyabedini/Clinical-Note-Evaluation/main/Results/human_vs_llm_averages.png) 
![Kappa Heatmap](https://raw.githubusercontent.com/nauzleyabedini/Clinical-Note-Evaluation/main/Results/human_agreement_heatmap.png)

### 3. Summary of Key Failure Modes:
**OpenAI (GPT-4o-mini):**
* **Compliance Blind Spot:** Frequently misses unsubstantiated diagnoses. It assumes any condition listed in the AI draft has valid clinical justification even without explicit transcript evidence or documented Assessment & Plan (MEAT).
* **False Negatives in Safety:** Its holistic leniency occasionally causes it to miss subtle but real clinical safety issues.

**Anthropic (Claude-3.5-Sonnet):**
* **Over-Sensitivity (False Positives):** Frequently flags minor conversational details or non-clinical pleasantries omitted from the note as "Critical Safety Omissions".
* **Hallucination Rigidity:** Heavily penalizes slight rephrasings or natural clinical summarization as "Critical Omissions."

**Detailed results are summarized [here.](https://github.com/nauzleyabedini/Clinical-Note-Evaluation/blob/main/Results/p0_eval_result_summary.md)**

## 🔍 Strengths & Limitations
* **Strengths:** Fully automated, modular 4-stage clinical evaluation pipeline with strict JSON schema outputs. Provides both quantitative (Kappa) and qualitative side-by-side behavioral alignment.
* **Limitations:** The N=10 human baseline is useful for pipeline validation and vibe-checks, but statistically underpowered for definitive claims about model performance.

## 🚀 Next Steps
The primary objective of the next iteration is to bridge OpenAI's cost and basic safety heuristics with Anthropic's strict compliance - the core challenge in developing a scalable, reliable AI clinical note auditor.

1. **Manual Prompt Tuning (N=10 Pilot) (*In Progress*):** Refine Anthropic's prompt to be less sensitive to harmless omissions and manually add strict HCC/MEAT validation rules to OpenAI's prompt. A small sample will be used to conserve token costs.
2. **Scale Human Evaluation (*In Progress*):** Expand the manual human grading to the full 67-note dataset to establish a statistically robust Gold Standard.
3. **Automatic Prompt Optimization (APO) (*Future*):** Leverage an APO framework on the full dataset to aggressively optimize OpenAI (`gpt-4o-mini`). The objective is to refine the cheaper model achieve comparable safety and compliance profiles as the human judge, as indicated by improvement in Cohen's kappa. notably, APO will be introduced once a manually fine-tuned model is produced to focus on edge-case performance.

---

## 📚 Resources
* [ACI-BENCH dataset](https://arxiv.org/abs/2306.02022)
* [NOHARM2 Study](https://arxiv.org/abs/2512.01241)

## 💻 Technologies Used
* **Python** (Pandas, Matplotlib, Seaborn)
* **OpenAI API** (`gpt-4o-mini`)
* **Anthropic API** (`claude-sonnet-5`)
* **Google Gemini API** (`gemini-1.5-flash`)



