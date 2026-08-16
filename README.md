# AI-Powered Clinical Documentation Evaluation Harness

A robust pipeline to evaluate AI-generated clinical notes against quality, accuracy, and billing compliance standards, comparing frontier LLMs (GPT-4o-mini vs. Claude-3.5-Sonnet) against human clinical experts.

## 🚀 Quick Start & Datasets
All resources to replicate this study are in our [GitHub Repository](https://github.com/nauzleyabedini/Clinical-Note-Evaluation/).
* **Note Data:** [ACI-BENCH Transcripts](https://raw.githubusercontent.com/microsoft/clinical_visit_note_summarization_corpus/refs/heads/main/data/aci-bench/challenge_data/train.csv) | [AI Notes Full (67)](https://raw.githubusercontent.com/nauzleyabedini/Clinical-Note-Evaluation/main/Data/full_dataset_with_ai_notes.csv) | [AI Notes Pilot (10)](https://raw.githubusercontent.com/nauzleyabedini/Clinical-Note-Evaluation/main/Data/experimental_dataset_with_ai_notes.csv)
* **Evaluation Data:** [Human Benchmark (10)](https://raw.githubusercontent.com/nauzleyabedini/Clinical-Note-Evaluation/main/Data/human_evaluation.csv) | [Aggregated Pilot Results](https://raw.githubusercontent.com/nauzleyabedini/Clinical-Note-Evaluation/main/Data/aggregated_experimental_evaluation_results_v2_4_modules.csv)
* **Code & Prompts:** [GitHub Prompts & Utils](https://github.com/nauzleyabedini/Clinical-Note-Evaluation/tree/main)
* **Rubric & Scoring System:** [Note Audit Rubric v2](https://github.com/nauzleyabedini/Clinical-Note-Evaluation/blob/main/Rubrics/Note_Audit_Rubric_v2.md)

## 📊 Results

### 1. Initial LLM Baseline (Full Dataset, N=67)
* **Anthropic (Claude-Sonnet-5):** Extremely strict (70.1% fail rate). Excellent at catching compliance/billing errors (HCC/MEAT) but overly sensitive.
* **OpenAI (GPT-4o-mini):** Lenient (46.3% fail rate). Missed the vast majority of unsubstantiated diagnoses and compliance risks.

### 2. Human Validation Pilot (Experimental Dataset, N=10)
*We ran this comparison on a smaller sample size (N=10) to conduct prompt debugging, qualitative alignment, and pipeline validation before scaling up.*

**Key Quantitative Findings:**
* **OpenAI** aligns better with humans on **Safety** (Kappa=0.40) and overall pass rate but completely fails on **Compliance** (Kappa=-0.11).
* **Anthropic** aligns better on **Compliance** (Kappa=0.41) but misses human nuance on **Safety** (Kappa=0.00).

![Average Scores](human_vs_llm_averages.png)
![Kappa Heatmap](human_agreement_heatmap.png)

**Key Qualitative Findings and Failure Modes:**
**OpenAI (GPT-4o-mini):**
* **Compliance Blind Spot:** Frequently misses unsubstantiated diagnoses. It assumes any condition listed in the AI draft has valid clinical justification even without explicit transcript evidence or documented Assessment & Plan (MEAT).
* **False Negatives in Safety:** Its holistic leniency occasionally causes it to miss subtle but real clinical safety issues.

**Anthropic (Claude-3.5-Sonnet):**
* **Over-Sensitivity (False Positives):** Frequently flags minor conversational details or non-clinical pleasantries omitted from the note as "Critical Safety Omissions".
* **Hallucination Rigidity:** Heavily penalizes slight rephrasings or natural clinical summarization as "Critical Omissions."

Detailed results are summarized [here.](https://github.com/nauzleyabedini/Clinical-Note-Evaluation/blob/main/Results/p0_eval_result_summary.md)

## 🔍 Strengths & Limitations
* **Strengths:** Fully automated, modular 4-stage clinical evaluation pipeline. Provides both quantitative (Kappa) and qualitative side-by-side behavioral alignment.
* **Limitations:** The N=10 human baseline is useful for pipeline validation and vibe-checks, but statistically underpowered for definitive claims.

## 🚀 Next Steps
The primary objective of the next iteration is to bridge OpenAI's cost and basic safety heuristics with Anthropic's strict compliance - the core challenge in developing a scalable, reliable AI clinical note auditor.

1. **Manual Prompt Tuning (N=10 Pilot):** Refine Anthropic's prompt to be less sensitive to harmless omissions and manually add strict HCC/MEAT validation rules to OpenAI's prompt. A small sample will be used to conserve token costs.
2. **Scale Human Evaluation:** Expand the manual human grading to the full 67-note dataset to establish a statistically robust Gold Standard.
3. **Automatic Prompt Optimization (APO):** Leverage an APO framework on the full dataset to aggressively optimize OpenAI (`gpt-4o-mini`). The objective is to force the cheaper model to match Anthropic's compliance rigor and the human's safety alignment.


---

## 📚 Resources
* [ACI-BENCH dataset](https://arxiv.org/abs/2306.02022)
* [NOHARM2 Study](https://arxiv.org/abs/2512.01241)

## 💻 Technologies Used
* **Python** (Pandas, Matplotlib, Seaborn)
* **OpenAI API** (`gpt-4o-mini`)
* **Anthropic API** (`claude-sonnet-5`)
* **Google Gemini API** (`gemini-1.5-flash`)



