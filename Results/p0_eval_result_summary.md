# Evaluation Summary & Strategic Next Steps: LLM Clinical Note Auditing

## 1. Executive Summary
This document summarizes the findings from evaluating AI-generated clinical notes using an LLM-as-a-Judge pipeline. We compared a highly capable model (**Anthropic Claude-3.5-Sonnet**) against a smaller, cost-effective model (**OpenAI GPT-4o-mini**) and benchmarked both against a **Human Expert** (N=10 pilot).

The primary objective of the next iteration is to bridge the identified capability gap: retaining OpenAI's lower operational costs while improving human-aligned safety heuristics, and adopting/improving Anthropic's rigorous billing and compliance standards. Balancing OpenAI's cost and basic safety heuristics against Anthropic's strict compliance checking is the core challenge in developing a scalable, reliable AI auditor.

---

## 2. Quantitative Findings & Misalignments
### Baseline Strictness (Full Dataset, N=67)
* **Anthropic (Claude-Sonnet-5):** 70.1% Failure Rate. Acts as an extremely conservative auditor.
* **OpenAI (GPT-4o-mini):** 46.3% Failure Rate. Highly lenient, passing many notes with underlying compliance risks.

### Inter-Rater Reliability (Cohen's Kappa vs. Human, N=10 Pilot)
* **Critical Safety Errors:** OpenAI aligns *Fairly* (Kappa = 0.40), while Anthropic shows *No Agreement* (Kappa = 0.00). This indicates Anthropic is misaligned with human judgment on what constitutes a true safety risk.
* **Critical Compliance Errors:** Anthropic aligns *Moderately* (Kappa = 0.41), while OpenAI performs worse than random chance (Kappa = -0.11). OpenAI severely fails to detect compliance issues.
* **ICD-10 Specificity:** Both models show slight agreement (OpenAI: 0.22, Anthropic: 0.17).
* **Structure & Usability:** Both models fail to align with human subjective scoring (Kappa = 0.00).
* **Overall Note Pass Rate:** OpenAI (Kappa = 0.40) aligns closer to the human expert's holistic judgment than Anthropic (Kappa = 0.20), primarily because Anthropic's over-strictness fails too many notes.

---

## 3. Qualitative Insights (Behavioral Analysis)
Based on side-by-side extraction reviews, the models exhibit distinct behavioral phenotypes and misalignments:

* **The Strict Compliance Auditor (Anthropic):** Excels at catching unsubstantiated diagnoses and missing HCC/MEAT criteria. However, it suffers from severe over-sensitivity, frequently flagging minor conversational omissions (e.g., patient pleasantries, minor demographic details) as "Critical Hallucinations" or "Safety Omissions." It lacks the clinical heuristic to distinguish between trivial conversational filler and clinically relevant data.
* **The Lenient Clinician (OpenAI):** Understands the heuristic of what makes a note clinically "safe" and appropriately ignores conversational fluff, aligning better with human safety judgments. However, it has a blind spot for billing compliance, assuming that any diagnosis listed in the AI draft is inherently justified, even without explicit transcript evidence or MEAT documentation.
* **Shared Weakness (Structure):** Both models struggle to evaluate the subjective "Structure & Usability" of a note. Human preference for SOAP flow, brevity, and clinical narrative is highly nuanced and difficult to encapsulate in the current prompt rubric.

---

## 4. Next Steps: Forking & Fine-Tuning Strategy (Next Iteration)
To optimize the pipeline for production, we will fork the current prompt architecture and execute a 3-phase fine-tuning/optimization strategy.

### Phase 1: Manual Prompt Tuning (The N=10 Pilot)
Before using automated frameworks, we must manually inject our qualitative and quantitative learnings into the system prompts. Beginning with manual fine-tuning allows us to improve general evaluation capabilities, reserving high-compute/high-cost APO capabilities for refining the model around edge cases. 
**Examples:**
* **Tuning OpenAI (Target: Compliance):** Explicitly update the OpenAI prompt rubric to mandate HCC/MEAT validation. *Instruction to add: "You MUST verify that every diagnosis listed in the note has explicit transcript evidence and a documented Assessment & Plan. Do not assume diagnoses are valid by default."*
* **Tuning Anthropic (Target: Safety/Leniency):** Update Anthropic to serve as our "Silver Standard." *Instruction to add: "Do not penalize the omission of small talk, non-clinical pleasantries, or minor demographic details unless clinically relevant."*

### Phase 2: Establish the Gold Standard (Scale to N=67)
To statistically validate our tuning, N=10 is insufficient.
* **Action:** Complete human expert evaluation for the remaining 57 notes.
* **Outcome:** This creates a robust, 67-note "Gold Standard" dataset required for the automated optimization phase.

### Phase 3: Automatic Prompt Optimization (APO) for OpenAI 
With the N=67 Gold Standard established, we will introduce an APO framework (e.g., DSPy or Promptbreeder) exclusively targeting the cheaper `gpt-4o-mini` model.
* **Action:** Feed the 67 human-graded notes into the APO framework. The system will iteratively generate, test, and score hundreds of prompt variations for OpenAI.
* **Objective Function:** Maximize the Cohen's Kappa score on the **Compliance** metric without dropping the **Safety** metric below 0.8.
* **Final Goal:** Achieve maximum rigor across all evaluated domains at OpenAI-mini API costs.
