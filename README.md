# AI-Powered Clinical Documentation Evaluation Harness

This project presents a robust harness for the comprehensive evaluation of AI-generated clinical notes against established quality, accuracy, and compliance standards. Leveraging advanced Large Language Models (LLMs) and quantitative metrics, this system addresses critical challenges in healthcare AI, such as hallucination detection, clinical accuracy, and billing compliance.

## 🚀 Quick Start & Resources

To run this pipeline or adapt it for your own use, all necessary scripts and datasets are hosted in the [Clinical-Note-Evaluation GitHub Repository](https://github.com/nauzleyabedini/Clinical-Note-Evaluation/).

**Data Files:**
* [ACI-BENCH Raw Dataset (Train)](https://raw.githubusercontent.com/microsoft/clinical_visit_note_summarization_corpus/refs/heads/main/data/aci-bench/challenge_data/train.csv)
* [Pre-generated Experimental AI Notes (10 samples)](https://raw.githubusercontent.com/nauzleyabedini/Clinical-Note-Evaluation/main/Data/experimental_dataset_with_ai_notes.csv)
* [Pre-generated Full AI Notes (67 samples)](https://raw.githubusercontent.com/nauzleyabedini/Clinical-Note-Evaluation/main/Data/full_dataset_with_ai_notes.csv)

**Prompts & Utilities:**
* `clinical_utils.py`: [Setup and API Handling](https://github.com/nauzleyabedini/Clinical-Note-Evaluation/blob/main/Setup/clinical_utils.py)
* `note_gen_prompts.py`: [Gemini Note Draft Generation Prompts](https://github.com/nauzleyabedini/Clinical-Note-Evaluation/blob/main/Prompts/note_gen_prompts.py)
* `eval_prompt_current.py`: [LLM-as-a-Judge Rubrics](https://github.com/nauzleyabedini/Clinical-Note-Evaluation/blob/main/Prompts/eval_prompt_current.py)


---

## 💡 Project Overview

The harness is designed to meticulously audit AI-generated clinical documentation. It integrates multiple frontier LLMs to simulate real-world auditing scenarios and measure the efficiency gains and potential burdens introduced by AI in clinical settings.

### Why Claude vs. GPT-4o-mini?
We explicitly chose to compare a highly capable, larger model (Anthropic's Claude) against a smaller, highly cost-effective model (OpenAI's GPT-4o-mini). This architectural contrast serves two purposes:
1. **Clear Discernment:** To clearly discern and quantify the differences in clinical reasoning, safety netting, and strictness between different tiers of AI models.
2. **Cost-Optimization Pipeline:** To establish a baseline capability gap, with the ultimate goal of determining if techniques like Automatic Prompt Optimization (APO) can enhance the smaller, cheaper model to operate at the same clinical accuracy level as the more expensive Anthropic model.

## 🔬 Methodology

### AI Note Generation
The Gemini API and a rigorously refined system prompt are leveraged to generate AI clinical notes from outpatient patient-clinician transcripts derived from the [ACI-BENCH dataset](https://arxiv.org/abs/2306.02022).

### AI Note Evaluation (LLM-as-a-Judge)
The quality of AI-generated draft notes is compared against the original transcripts and a "Gold Standard Note," simulating an expert Clinical Documentation Integrity (CDI) audit. The evaluation is broken into four strict modules:
1. **Fact Grounding & Clinical Safety:** Transcript fidelity, hallucination extraction, and critical omissions.
2. **Clinical Reasoning & Contextual Attribution:** Contextual accuracy and timeline integrity.
3. **Coding, Billing & Compliance Integrity:** HCC/MEAT criteria validation, ICD-10 specificity, and upcoding risk assessment.
4. **Structure, Usability & Master Gate Evaluation:** Adherence to standard outpatient note formats (SOAP) and an overall Pass/Fail gate.
The modules and rating scales are described in more detail in `Note_Audit_Rubric_v2.md`: [Initial Evaluation Rubric](https://github.com/nauzleyabedini/Clinical-Note-Evaluation/blob/main/Rubrics/Note_Audit_Rubric_v2.md) 

## 📊 Results

### Initial LLM-as-a-Judge Evaluation (Full Dataset - 67 encounters)
Our baseline evaluation highlights significant differences in strictness and clinical auditing capabilities between the two judge models:

* **Anthropic (Claude-Sonnet-5) - The Strict Auditor:** Exhibited a highly conservative profile with a **70.1% failure rate** (47/67 notes failed). It heavily penalized notes for `Critical Compliance Errors` (32 occurrences) and `Unsubstantiated Diagnoses` (26 occurrences), catching fine-grained nuances in the transcript.
* **OpenAI (GPT-4o-mini) - The Lenient Judge:** Evaluated notes much more loosely, yielding a **46.3% failure rate** (31/67 notes failed). While it still caught major `Critical Compliance Errors` (21 occurrences), it missed the vast majority of `Unsubstantiated Diagnoses` (only 7 occurrences flagged) compared to Anthropic.

These findings mathematically demonstrate that relying solely on a smaller, unoptimized model for clinical auditing risks letting clinically significant and compliance-related errors slip into the final medical record. This establishes the baseline capability gap needed for the next phase of prompt optimization.

## 🚀 Next Steps

The next phase of this project focuses on directly bridging the gap between LLM evaluation and human clinical expertise, and optimizing the cost-efficiency of the pipeline:

1. **Complete Human-in-the-Loop Evaluation:** Finalize the manual human expert evaluation on the 10-note experimental subset using the generated CSV rubrics.
2. **Human vs. LLM Benchmarking:** Statistically compare the human expert scores against both Anthropic and OpenAI. This will identify exactly where the LLM judges fail to capture true clinical nuance and which model better aligns with actual physician standards.
3. **Automatic Prompt Optimization (APO):** Introduce APO to iteratively refine and self-improve the LLM-as-a-judge prompts. The primary objective is to determine if APO can enhance the performance, strictness, and accuracy of the smaller, cheaper model (GPT-4o-mini) to match the baseline performance of the more expensive Anthropic model.


---

## 📚 Resources
* [ACI-BENCH dataset](https://arxiv.org/abs/2306.02022)
* [NOHARM2 Study](https://arxiv.org/abs/2512.01241)

## 💻 Technologies Used
* **Python** (Pandas, Matplotlib, Seaborn)
* **OpenAI API** (`gpt-4o-mini`)
* **Anthropic API** (`claude-sonnet-5`)
* **Google Gemini API** (`gemini-1.5-flash`)



