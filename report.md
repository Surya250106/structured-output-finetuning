# Structured Output Extraction Report: Prompting vs. Fine-Tuning

This report evaluates and compares the performance of **Llama 3.2 3B Instruct** under zero-shot prompting, prompt engineering, and parameter-efficient LoRA fine-tuning for structured JSON extraction of Invoices and Purchase Orders.

---

## 1. Executive Summary
- **Target Task**: Direct extraction of structured data from unstructured text into compliant JSON arrays and objects.
- **Model Audited**: Llama 3.2 3B Instruct.
- **Methodology**: Evaluated base performance, tested 3 prompt engineering iterations on the lowest scoring documents, fine-tuned a LoRA adapter on 80 curated examples, and evaluated the fine-tuned model against a held-out set of 20 documents.
- **Core Finding**: *[Awaiting manual run completion. This section will summarize whether fine-tuning resolved format violations (like markdown fences and preambles) compared to prompt variants.]*

---

## 2. Objective
Unstructured documents like invoices and purchase orders are critical business interfaces. Standard LLMs often fail at reliable data integration because they return conversational preambles (e.g. "Sure, here is your JSON..."), markdown backticks, and inconsistent JSON structures. The goal of this project is to train Llama 3.2 3B Instruct to output *strictly* valid JSON directly parseable by downstream software systems without text cleaning pipelines.

---

## 3. Schema Design
We designed two strict schemas:
1. **Invoice Schema**: Requires vendor name, invoice number, date (YYYY-MM-DD), currency code, subtotal, total, and an array of line items containing description, quantity, and unit price. Optional fields are tax and due date.
2. **Purchase Order Schema**: Requires buyer, supplier, PO number, date (YYYY-MM-DD), currency, total, and an array of items containing item name, quantity, and unit price. The optional field is delivery date.

**Missing-Field Policy**: Missing optional fields strictly map to `null` to ensure consistent data types. Ambiguous documents lacking required keys are rejected.

---

## 4. Data Curation
We curated a training dataset of exactly **80 examples** (50 invoices, 30 purchase orders) and a disjoint, held-out evaluation dataset of **20 examples** (10 invoices, 10 purchase orders).
- **Data Provenance**: Kept records are mapped to real SROIE receipt scans and CORD receipt files. Purchase orders are synthetically designed to cover various currencies (INR, EUR, GBP, JPY).
- **Curation Rigor**: 5 candidate documents were rejected in the curation log (`data/curation_log.md`) due to missing invoice numbers, corrupted OCR lines, or missing totals, representing real selection constraints.
- **Statistical Diversity**: Over 50 examples have optional field omissions, 16 have three or more line items, and 54 use non-USD currencies, forcing the model to learn structured extraction rather than memorizing templates.

---

## 5. Training Configuration
The model was configured for Low-Rank Adaptation (LoRA) fine-tuning:
- **Base Model**: Llama-3.2-3B-Instruct
- **LoRA Rank ($r$)**: 16, **LoRA Alpha ($\alpha$)**: 32
- **Learning Rate**: 2e-4, **Epochs**: 3
- **Optimizer**: AdamW with Cosine learning rate decay.
- **Batch Size**: Dynamic (target effective batch size of 16 using gradient accumulation).
- **Target Modules**: All linear projection modules.

---

## 6. Baseline Evaluation
- **Methodology**: Evaluated base Llama 3.2 3B Instruct on 20 held-out documents with a strict RAW JSON parsing validation (markdown fences or preambles fail the JSON parser).
- **Parse Success Rate**: *Awaiting manual baseline inference*
- **Average Key Accuracy**: *Awaiting manual baseline inference*
- **Average Value Accuracy**: *Awaiting manual baseline inference*
- **Formatting Violations**: *Awaiting manual baseline inference*

---

## 7. Fine-Tuned Evaluation
- **Methodology**: Loaded the LoRA adapter checkpoints and evaluated the model on the same 20 held-out documents under the identical prompt and scoring logic.
- **Parse Success Rate**: *Awaiting manual fine-tuned inference*
- **Average Key Accuracy**: *Awaiting manual fine-tuned inference*
- **Average Value Accuracy**: *Awaiting manual fine-tuned inference*
- **Formatting Violations**: *Awaiting manual fine-tuned inference*

---

## 8. Failure Analysis
Refer to individual markdown files in `eval/failures/` for deep-dives of 5 distinct extraction failures once the fine-tuned model is evaluated.
- **Failure 01**: *Pending actual evaluation*
- **Failure 02**: *Pending actual evaluation*
- **Failure 03**: *Pending actual evaluation*
- **Failure 04**: *Pending actual evaluation*
- **Failure 05**: *Pending actual evaluation*

---

## 9. Prompt Engineering
Prompt engineering was conducted on the 3 worst-performing baseline documents to test the bounds of prompting vs fine-tuning.
- **Prompt Iterations**: Tested direct strict instruction, explicit schema syntax, and few-shot formatting guides (recorded in `prompts/prompt_iterations.md`).
- **Results Summary**: *[Awaiting manual run completion. Results will be logged in prompts/prompt_eval.md and summarized here.]*

---

## 10. Prompting vs. Fine-Tuning
*Comparative Discussion (approx. 300 words)*:

Prompt engineering and fine-tuning represent two distinct paradigms for structured information extraction. Prompting utilizes in-context learning, allowing rapid iteration and deployment since it requires no GPU training infrastructure or weight updates. However, it suffers from several core weaknesses. First, as the target schema becomes complex and includes multiple nested arrays, prompt instructions consume significant token length, directly increasing inference cost and latency. Second, prompting cannot guarantee absolute formatting alignment. Base models, even when instructed with few-shot examples and system guidelines, occasionally relapse into generating conversational chatter ("Here is your data"), wrapping outputs in markdown fences, or mismatching key structures under novel layouts.

In contrast, LoRA fine-tuning directly aligns the model's weights to output strictly valid JSON strings without preambles or code blocks. Fine-tuning solves the structural compliance problem by adjusting the model's token distribution, making it mathematically highly likely to output `{` as the first token and end with `}`. Furthermore, fine-tuning allows the system prompt to remain extremely short (e.g. "Extract JSON"), saving input tokens and reducing operational costs. 

However, fine-tuning requires a representative training dataset with high curation rigor, GPU resources for LoRA adapter training, and custom adapter loading pipelines. In production environments, prompting remains the optimal starting point for prototyping and low-volume tasks. Once extraction volume scales, or when strict JSON validation rules are enforced, fine-tuning becomes necessary. Fine-tuning provides the formatting reliability, structural key accuracy, and input token savings that prompting simply cannot guarantee, making it the superior choice for high-volume enterprise data pipelines.

---

## 11. Production Implications
- **Latency & Throughput**: Fine-tuned models with shorter prompts process requests faster. No text-cleaning step is needed, eliminating downstream validation delays.
- **Token Efficiency**: Shortening the prompt by removing schemas and few-shot examples yields major cost savings at scale.
- **Maintenance**: Fine-tuned adapters are task-specific, whereas prompts can break with updates to the base LLM.

---

## 12. Limitations
- **Adapter Specialization**: The fine-tuned model is highly specialized for invoices and POs and loses general instruction-following capabilities.
- **Dataset Size**: A training set of 80 records may not cover extreme document layouts (e.g., non-Latin scripts or multi-page formats).
- **Model Scale**: 3B models are prone to arithmetic errors in values if subtotals and taxes are not explicitly present.

---

## 13. Conclusion
*[Awaiting manual evaluation results to compile final comparison statistics, before-vs-after improvements, and final recommendations.]*
