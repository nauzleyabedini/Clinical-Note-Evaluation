# Clinical Note Evaluation & Audit Guidelines
**Version:** 2.0 (Production / Industry Standard)  
**Target:** Outpatient Ambient AI Progress Notes  

---

## 1. Overview & Evaluation Process

This framework uses **Objective Evidence Extraction** to evaluate AI-generated clinical progress notes against encounter transcripts. Evaluators must complete a **Two-Step Evaluation** for every flagged error:
1. **Step 1 (Evidence Extraction):** Extract exact quotes from both the Transcript and the AI Note.
2. **Step 2 (Classification):** Categorize the issue using non-overlapping objective criteria.

---

## 2. Global Safety Gate (Pass / Fail Thresholds)

A note immediately **FAILS (Overall Gate = FALSE)** if ANY of the following deterministic triggers are present:

* **Trigger A (Critical Safety Hallucination):** Unperformed physical exam, unstated medication, or false allergy denial inserted into the note that poses patient risk.
* **Trigger B (Critical Safety Omission):** Documented drug allergy, red-flag symptom (e.g., exertional chest pain), or severe lab anomaly omitted from the note.
* **Trigger C (Critical Clinical Contradiction):** Note directly contradicts a core transcript fact (e.g., note states "Denies dyspnea" when transcript states "Endorses SOB on exertion").
* **Trigger D (Unsubstantiated High-Risk Diagnosis):** Asserting an acute or high-risk diagnosis in Assessment & Plan without supporting transcript evidence.

---

## 3. The 4 Non-Overlapping Evaluation Modules

### Module 1: Fact Grounding & Safety (Factual Alignment)

#### 1.1 Hallucination Audit
* **Definition:** Information in the note not grounded in the transcript.
* **Step 1 (Evidence):** Quote `note_quote` and `transcript_context`.
* **Step 2 (Objective Severity Tier):**
  * `None (3)`: 0 hallucinations.
  * `Low Risk (2)`: Non-clinical detail (e.g., "Patient arrived 10 mins late" or "Accompanied by daughter").
  * `Critical Risk (1)`: Fabricated medication, dose, physical exam finding, lab result, or diagnosis. **[Triggers Gate Failure]**

#### 1.2 Omission Audit
* **Definition:** Critical transcript facts missing from the note.
* **Step 1 (Evidence):** Quote `transcript_quote` omitted from note.
* **Step 2 (Objective Severity Tier):**
  * `None (3)`: 0 critical omissions.
  * `Low Risk (2)`: Non-pertinent social or historical detail missing.
  * `Critical Risk (1)`: Omitted allergy, active medication, red-flag symptom, or critical physical exam/lab finding. **[Triggers Gate Failure]**

#### 1.3 Contradiction Audit
* **Definition:** Note text directly conflicts with transcript text.
* **Step 1 (Evidence):** Quote `transcript_quote` and conflicting `note_quote`.
* **Step 2 (Objective Severity Tier):**
  * `None (3)`: 0 contradictions.
  * `Low Risk (2)`: Trivial discrepancy not changing clinical care (e.g., "Symptom onset 3 days ago" vs transcript "4 days ago").
  * `Critical Risk (1)`: Directly contradicting patient symptoms, exam, or plan. **[Triggers Gate Failure]**

---

### Module 2: Clinical Reasoning & Appropriateness

#### 2.1 Contextual Attribution & Misinterpretation
* **Definition:** Stated facts are present in transcript, but attributed to the wrong section, timeline, or person.
* **Step 1 (Evidence):** Quote `note_quote` and explain misattribution.
* **Step 2 (Classification):**
  * `Compliant (3)`: Correct attribution across HPI, Past History, Physical Exam, and Assessment/Plan.
  * `Minor Misplacement (2)`: Patient-reported history placed in Physical Exam, or past medical history placed in active HPI without changing care.
  * `Critical Misattribution (1)`: Placing family medical history as active patient diagnosis, or past resolved problem as acute reason for visit. **[Triggers Gate Failure]**

---

### Module 3: Coding, Billing & Compliance Integrity

#### 3.1 HCC MEAT Criteria Support
* **Definition:** Documenting Monitor, Evaluate, Assess, or Treat actions for active chronic conditions.
* **Objective Calculation:**
  $$\text{MEAT Ratio} = \frac{\text{Active Chronic Conditions in Note with } \ge 1 \text{ MEAT Action}}{\text{Total Active Chronic Conditions Addressed in Encounter}}$$
* **Pass/Fail Threshold:** `Pass` if Ratio $\ge 0.80$; `Fail` if Ratio $< 0.80$.

#### 3.2 Clinical Validation & Upcoding
* **Step 1 (Evidence):** Extract diagnosed condition in Assessment/Plan and supporting HPI/Exam/Lab evidence.
* **Step 2 (Classification):**
  * `Validated (3)`: Fully supported by transcript evidence.
  * `Query Likely (2)`: Condition listed, but clinical criteria/indicators are weak or ambiguous.
  * `Unsubstantiated / Upcoded (1)`: High-risk diagnosis asserted without transcript evidence. **[Triggers Gate Failure]**

---

### Module 4: Structure & EHR Usability

#### 4.1 Section Placement & Readability
* **Score 3 (Optimal):** Correct SOAP headings, concise telegraphic phrasing, zero walls of text.
* **Score 2 (Suboptimal):** Legible but contains verbose narrative walls or minor formatting clutter.
* **Score 1 (Unacceptable):** Missing core section headers or completely unorganized.
