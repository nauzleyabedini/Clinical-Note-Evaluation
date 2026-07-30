# AI-Powered Clinical Documentation Evaluation Framework
*Works-in-progress - Last update: July 30, 2026*

This project presents a robust framework for the comprehensive evaluation of AI-generated clinical notes against established quality, accuracy, and compliance standards. Leveraging advanced Large Language Models (LLMs) and quantitative metrics, this system addresses critical challenges in healthcare AI, such as hallucination detection, clinical accuracy, and impact on clinician workflow.

## Project Overview

The framework is designed to meticulously audit AI-generated clinical documentation through a two-phased evaluation process. It integrates multiple state-of-the-art LLMs (OpenAI, Anthropic, Google Gemini) to simulate real-world auditing scenarios and measure the efficiency gains and potential burdens introduced by AI in clinical settings. This project showcases expertise in:

*   **Multi-LLM Integration & Orchestration:** Seamlessly working with and evaluating outputs from diverse LLM providers.
*   **Custom Prompt Engineering:** Developing structured and domain-specific prompts for highly accurate and consistent evaluations.
*   **Robust API Handling:** Implementing retry logic with exponential backoff to ensure resilience and reliability in API interactions.
*   **Quantitative Performance Metrics:** Defining and applying measurable metrics for clinical accuracy, compliance (HCC capture), safety, and clinician editing burden.
*   **Healthcare AI Application:** Addressing a critical need in clinical AI development for rigorous validation and continuous improvement of documentation systems.

## Methodology

### Phase 1: Pre-Vetting Evaluation (AI Note vs. Original Transcript)

This phase assesses the initial quality of AI-generated draft notes by comparing them directly against the original doctor-patient transcripts. It simulates an expert Clinical Documentation Integrity (CDI) audit using two distinct LLMs (OpenAI `gpt-4o-mini` and Anthropic `claude-sonnet-5`) acting as independent auditors.

**Evaluation Domains:**

1.  **Clinical Accuracy:** Identifying omissions, fabrications, or hallucinations.
2.  **HCC / Risk Adjustment Capture:** Assessing the specificity and completeness of chronic condition documentation (MEAT criteria).
3.  **Patient Safety:** Detecting internal medical contradictions or unsafe information.

**Output:** Structured JSON containing quantifiable scores (0-100) for each domain and key findings.

### Phase 2: Post-Vetting Evaluation (Pre-Signed AI Note vs. Final Revised/Signed Note)

This phase quantifies the human clinician's effort required to finalize an AI-generated draft note. Since real-world revised notes were unavailable, Google Gemini acts as a "master clinician" to generate a "gold-standard" note, which is then compared against the original AI draft.

**Metrics for Clinician Burden:**

*   **Normalized Levenshtein Edit Distance:** Measures character-level editing effort.
*   **Word Edit Ratio:** Quantifies word-level changes, providing insights into the extent of structural and content revisions.

## Key Features & Technical Highlights

*   **Domain-Specific Data Handling:** Utilizes the ACI-BENCH dataset, demonstrating experience with specialized healthcare datasets.
*   **Flexible LLM Integration:** Designed to easily incorporate and compare performance across various generative AI models.
*   **Structured Output Parsing:** Ensures reliable extraction of evaluation metrics from LLM responses via JSON schema enforcement.
*   **Error Tolerance:** Implements robust error handling and API retry mechanisms to ensure high availability and stability during large-scale evaluations.
*   **Quantitative Analysis:** Focuses on generating measurable data points to inform AI model improvements and assess clinical impact.

## Technologies Used

*   **Python:** Core programming language.
*   **Pandas:** Data manipulation and analysis.
*   **OpenAI API:** For AI model evaluation.
*   **Anthropic API:** For AI model evaluation.
*   **Google Gemini API:** For generating "gold-standard" clinical notes.
*   **Levenshtein:** For calculating edit distances.
*   **Matplotlib & Seaborn:** (Implicit for future visualization of evaluation results).
*   **Google Colaboratory:** Development environment, utilizing cloud resources.

## Conclusion

This project demonstrates a rigorous, quantitative approach to evaluating AI models in sensitive domains like clinical documentation. It highlights capabilities in advanced NLP, LLM orchestration, data-driven evaluation methodologies, and a deep understanding of domain-specific challenges in healthcare AI.
