# AI-Powered Clinical Documentation Evaluation Harness:

This project presents a robust harness for the comprehensive evaluation of AI-generated clinical notes against established quality, accuracy, and compliance standards. Leveraging advanced Large Language Models (LLMs) and quantitative metrics, this system addresses critical challenges in healthcare AI, such as hallucination detection, clinical accurac, and billing compliance.

## Project Overview

The harness is designed to meticulously audit AI-generated clinical documentation. It integrates multiple frontier LLMs to simulate real-world auditing scenarios and measure the efficiency gains and potential burdens introduced by AI in clinical settings. This project showcases expertise in:

*   **Multi-LLM Integration & Orchestration:** Seamlessly working with and evaluating outputs from diverse LLM providers, including managing model-specific API nuances.
*   **Custom Prompt Engineering for Clinical Integrity:** Developing structured, domain-specific, and rigorously tested prompts for highly accurate and consistent evaluations, with **explicit JSON schema enforcement** tailored to clinical criteria.
*   **Robust API Handling:** Implementing advanced retry logic with exponential backoff and fine-tuning model parameters (e.g., `max_tokens`, `temperature`) to ensure resilience, reliability, and deterministic output from various APIs.
*   **Quantitative Performance Metrics with Clinical Domain Expertise:** Defining and applying measurable metrics for clinical accuracy, compliance (HCC capture, ICD-10 specificity), and safety, informed by deep clinical understanding.
*   **Healthcare AI Application:** Addressing a critical need in clinical AI development for rigorous validation and continuous improvement of documentation systems, directly contributing to safe and effective AI deployment in healthcare.

## Methodology

### AI Note Generation

The Gemini API (`gemini-3.6-flash`) and rigorously refined system prompt are leveraged to generate AI clinical note from a subset of outpatient patient-clinician conversation transcripts derived from the [ACI-BENCH dataset](https://arxiv.org/abs/2306.02022).

**AI Note Generation Process (Google Gemini):**

*   **Few-Shot Prompting:** The Gemini API (`gemini-3.6-flash`) is used to generate the initial AI draft notes. The prompt incorporates domain-specific few-shot examples to guide the model towards the desired output format and content, emphasizing clinical integrity, compliance, and safety.
*   **Post-Processing for Structure:** A custom Python function is applied post-generation to enforce a strict, predefined clinical note structure (e.g., 'CHIEF COMPLAINT', 'HISTORY OF PRESENT ILLNESS', 'REVIEW OF SYSTEMS', 'PHYSICAL EXAM', 'RESULTS', 'ASSESSMENT AND PLAN'). This programmatic step uses regular expressions to parse and reconstruct the note, ensuring all required headings are present and content is correctly organized, even if initial LLM output deviates slightly.

### AI Note Evaluation Against Ground Truth Transcripts & Clinician-Vetted Notes

The quality of AI-generated draft notes are compared against the original doctor-patient transcripts and a "Gold Standard Note," simulating an expert Clinical Documentation Integrity (CDI) audit using two distinct LLMs (OpenAI `gpt-4o-mini` and Anthropic `claude-sonnet-5`) acting as independent auditors.

**Modular Evaluation Approach reflecting Clinical Domain Expertise:**
The evaluation of these AI-generated notes is modular, grouping evaluation criteria into three core domains, each designed to assess specific aspects of clinical documentation from an expert perspective. A modular evaluation harness was used to allow more flexibility in fine-tuning and to limit computational demands:

1.  **Clinical Fact Grounding:** This module rigorously assesses the AI note's fidelity to the original patient-doctor transcript. It measures:
    *   **Transcript Fidelity (Score 1-4):** How accurately the AI note reflects the information in the transcript.
        *   Score 4 (Fully Accurate): Every clinical assertion in the note aligns with explicit statements or necessary clinical deductions from the transcript.
        *   Score 3 (Minor Inaccuracy): Contains trivial misstatements that do not alter clinical context.
        *   Score 2 (Moderate Distortion): Misrepresents patient history, severity, or examination details.
        *   Score 1 (Major Factual Error): Directly contradicts facts established in the transcript.
    *   **Hallucinations (Count & Severity 1-3):** Identifies any information in the AI note not grounded in the transcript.
        *   `hallucinations_count`: Number of hallucinations (0, 1, 2, ...).
        *   `hallucinations_severity_score`: Score 3 (No hallucinations), Score 2 (Low severity), Score 1 (High severity).
    *   **Critical Omissions (Score 1-3):** Detects critical clinical information from the transcript omitted from the AI note.
        *   Score 3 (No Critical Omissions): No critical omissions present.
        *   Score 2 (Low severity): Low stakes omissions that do not have the potential to cause harm.
        *   Score 1 (High severity): High stakes omissions with potential for harm.

2.  **Compliance & Billing:** This module focuses on the adherence to coding and regulatory standards by comparing the AI Note against both the Gold Standard Note and the Transcript:
    *   **HCC Compliance via MEAT Criteria (Ratio & Pass/Fail):** For chronic conditions, verifies MEAT (Monitor, Evaluate, Assess, Treat) documentation.
        *   `hcc_compliance_ratio_percentage`: (float 0.0-1.0).
        *   `hcc_pass_fail`: (boolean) based on a compliance ratio threshold of >= 0.8.
    *   **ICD-10 Specificity (Scale 1-3):** Assesses the specificity of implied or explicit ICD-10 codes.
        *   Score 3 (High Specificity): Captures maximum clinical detail.
        *   Score 2 (Unspecified): Uses generic terms when specifics are available.
        *   Score 1 (Invalid): Codes unconfirmed or undocumented conditions.
    *   **Clinical Validation (Scale 1-3):** Assesses if clinical statements and diagnoses are clinically sound and supported.
        *   Score 3 (Compliant): Strong clinical indicators support all documented diagnoses.
        *   Score 2 (Query Likely): Diagnosis documented but lacking supporting clinical data.
        *   Score 1 (Upcoding / Unsubstantiated): High-risk diagnosis asserted without evidence.

3.  **Quality, Style & Safety:** This module examines the overall quality, adherence to style guidelines, and potential safety risks within the AI note, using both the Gold Standard Note and Transcript for context. It covers, incorporating **critical safety flags** and qualitative assessment skills:
    *   **Note Structure & Organization (0-5):** Evaluate adherence to outpatient note structure, readability, and clarity.
        *   Score 1 (Unacceptable) to Score 5 (Excellent), with detailed rubrics for each level.
    *   **Safety Risk Tier (Score 1-4):** Identify potential patient safety risks.
        *   Score 4 (None): Zero safety concerns.
        *   Score 3 (Low): Minor ambiguity.
        *   Score 2 (Moderate): Potential for minor clinical misunderstanding.
        *   Score 1 (Critical): Risk of patient harm.
    *   **`overall_key_findings`:** A string summary of overall errors or strengths across all modules.

**Output:** Strictly structured JSON containing quantifiable scores for each domain and `overall_key_findings`, rigorously enforced through prompt engineering and `response_format` settings.


## Key Features & Technical Highlights

*   **Domain-Specific Data Handling:** Utilizes the [ACI-BENCH dataset](https://arxiv.org/abs/2306.02022), demonstrating experience with specialized healthcare datasets and understanding of clinical data nuances.
*   **Flexible LLM Integration with Nuance Handling:** Designed to easily incorporate and compare performance across various generative AI models, including explicit handling of Anthropic's `TextBlock` responses and setting `temperature=0.0` for deterministic JSON output.
*   **Strict Structured Output Parsing:** Ensures reliable extraction of complex evaluation metrics from LLM responses via explicit JSON schema enforcement and robust post-processing.
*   **Advanced Error Tolerance & Recovery:** Implements robust error handling, including API-specific retry mechanisms with exponential backoff, and strategies to mitigate `JSONDecodeError` by optimizing `max_tokens` and `temperature` for consistent LLM output.
*   **Iterative Fine-Tuning of Evaluation Logic:** The modular design facilitates **iterative refinement and optimization** of individual evaluation criteria and prompts, allowing for continuous improvement of the harness's precision and recall in identifying documentation issues.
*   **Quantitative Analysis for Actionable Clinical Impact:** Focuses on generating measurable data points to inform AI model improvements and assess clinical impact, providing actionable insights for clinical AI development by directly linking technical metrics to **clinical outcomes and compliance standards**.

## Results

### Average Evaluation Scores by LLM Judge
![Average Evaluation Scores](llm_judge_comparison_bar.png)
*Figure 1: Average evaluation scores across 7 clinical metrics comparing Anthropic (claude-sonnet-5) and OpenAI (gpt-4o-mini) across 67 clinical encounters.*

### Score Comparison Across Samples by Metric (Heatmap)
![Score Comparison Heatmap](llm_judge_heatmap.png)
*Figure 2: Heatmap showing the distribution of scores for Transcript Fidelity, Safety Risk Tier, and Note Structure Organization across all 67 samples.*

### Distribution of Compliance & Billing Scores
![Compliance and Billing Scores](llm_judge_billing_boxplot.png)
*Figure 3: Boxplot showing the distribution of scores for HCC Compliance Ratio, ICD-10 Specificity, and Clinical Validation across all 67 samples.*

### Interpretation of LLM-as-a-Judge Results (Clinical Context - Full N=67 Dataset)

Evaluating the full ACI-Bench dataset (67 clinical encounters) reveals significant, quantifiable differences in how frontier models behave as clinical auditors. The expanded sample size highlights a stark divergence in model strictness and evaluation philosophy:

**1. Auditor Strictness and Clinical Fact Grounding:**
* **Anthropic (Claude) as a Strict Compliance Auditor:** Across the full dataset, Anthropic consistently acts as a highly conservative judge. It assigns stricter (lower) scores for **Transcript Fidelity**, **Hallucinations**, and **Critical Omissions**. In a clinical setting, Claude functions like a rigid CDI specialist, heavily penalizing any AI-generated text that deviates from or assumes details not explicitly stated in the transcript.
* **OpenAI (GPT-4o-mini) as a Lenient Summarizer:** OpenAI evaluates the notes much more leniently, frequently giving perfect scores for fidelity and safety. It appears to evaluate based on general "clinical plausibility" rather than strict transcript grounding, making it much more forgiving but potentially riskier for catching subtle hallucinations.

**2. Inter-Rater Reliability (Cohen's Kappa):**
* The calculated Cohen's Kappa scores across the 67 notes are strikingly low (near or below 0.0) for metrics like *Transcript Fidelity* and *Safety Risk Tier*. This mathematically proves that the two models have **almost no agreement** in their evaluation standards. Anthropic is consistently finding errors and safety risks that OpenAI completely ignores.

**3. Structural and Stylistic Agreement:**
* Despite disagreeing on factual fidelity, both models show high baseline scores for **Note Structure Organization**. This confirms that the generative AI successfully synthesizes the required Outpatient Note formats (CC, HPI, ROS, etc.), even if the underlying clinical facts are contested.

**4. Compliance and Billing Evaluation:**
* **ICD-10 Specificity and Clinical Validation:** In evaluating billing components, the models exhibit similar discrepancies, with Anthropic generally assigning lower scores and capturing a broader range of deficiencies compared to OpenAI's more lenient grading.
* **HCC Compliance Ratio:** Both models identified very high compliance, reflecting the AI note generator's ability to effectively document MEAT criteria. However, Anthropic proved to be slightly more strict in identifying edge cases.

**Summary:**
The full dataset evaluation strongly supports using **Anthropic** if the goal is a strict safety net to catch hallucinations, omissions, and compliance failures before a physician signs the note. The lack of agreement (low Kappa) between the models proves that relying on a lenient model like GPT-4o-mini for clinical auditing risks letting clinically significant errors slip through to the final medical record.

### Future Directions

To further validate and refine this LLM-as-a-Judge evaluation harness, the following next steps are proposed:

**1. Prompt Engineering for Inter-Rater Reliability (IRR):**
*   **Iterative Refinement via Loop Engineering:** Conduct "loop engineering" on the prompts for highly subjective metrics like *Transcript Fidelity* and *Safety Risk Tier*. By analyzing the discrepancies between Anthropic and OpenAI, we can introduce more explicit edge-case examples into the prompt rubrics to tighten agreement.
*   **Chain-of-Thought (CoT) Verification:** Require the LLM judges to output a short rationale *before* providing their final numeric score. This forces the model to ground its decision and often increases inter-model consensus.

**2. Clinician Concordance Study (Human-in-the-Loop):**
*   **Expert Baselines:** Validate the LLM-as-a-Judge outputs against a panel of human clinical documentation experts (e.g., CDI specialists, attending physicians).
*   **Benchmarking AI vs. Human:** Compare the AI judges' scores to the human experts to determine which LLM's scoring profile (OpenAI's generalized approach vs. Anthropic's conservative approach) more accurately reflects true clinical judgment.

**3. Statistical Agreement Analysis:**
*   **Cohen's Kappa:** Formalize the inter-rater reliability between the LLM judges by calculating Cohen's Kappa (or Fleiss' Kappa for >2 judges) and against human judges for categorical metrics. This provides a rigorous quantitative measure of consensus beyond simple score averaging, helping to prove the statistical validity of the automated audit.
*   **Handling Zero-Variance Edge Cases:** Address statistical artifacts (like Cohen's Kappa returning 0.0 or NaN) that occur when an AI judge exhibits zero variance (e.g., universally scoring a '4') across a highly uniform sample set.

**4. Introduce a Severity-Weighted F1 Score:**
*   Compare current fidelity (hallucination/omission) scales against other measures of precision and recall, such as those used in the [NOHARM2](https://arxiv.org/abs/2512.01241) study by Wu, *et al.* published in *Nature Science* (2026) to calculate a severity-weighted F1 score. Examples include the RAND-UCLA Appropriateness Method (severity-weighted precision or hallucinations) and WHO Harm Severity Definitions (Severity-weighted recall or omission).

### Conclusion

This project demonstrates a rigorous, quantitative, and clinically informed approach to evaluating AI models in sensitive domains like clinical documentation. It highlights capabilities in advanced natural language processing (NLP), multi-LLM orchestration, prompt engineering for clinical integrity, data-driven evaluation methodologies, and a deep understanding of domain-specific challenges in healthcare AI. These skills are directly transferable and critical for roles at the forefront of clinical AI research and development.
---

## Resources
* [ACI-BENCH dataset](https://arxiv.org/abs/2306.02022)
* [NOHARM2 Study](https://arxiv.org/abs/2512.01241)

## Technologies Used

*   **Python:** Core programming language.
*   **Pandas:** Data manipulation and analysis.
*   **OpenAI API:** For AI model evaluation (`gpt-4o-mini`).
*   **Anthropic API:** For AI model evaluation (`claude-sonnet-5`).
*   **Google Gemini API:** For generating AI clinical notes (`gemini-3.6-flash`).
*   **Matplotlib & Seaborn:** (Implicit for future visualization of evaluation results).
*   **Google Colaboratory:** Development environment, utilizing cloud resources.

