# Evaluation Summary and Methodology

This document outlines the metrics, scoring formulas, and results for extracting structured outputs from invoices and purchase orders.

## Metric Definitions

- **Parse Success Rate**: The fraction of documents where the model returned direct, valid JSON (no markdown fences, prose, or preambles) containing all required keys. Formula:
  $$\text{Parse Success Rate} = \frac{\text{Count}(\text{valid JSON} \land \text{has all required keys})}{20}$$
- **Key Accuracy**: The average fraction of expected schema keys (both required and optional) present in the parsed output JSON block.
- **Value Accuracy**: The average fraction of matching values for the keys that are present, normalized for harmless whitespace and float trailing differences.
- **Strict RAW Parsing Rule**: If the raw model response contains markdown backticks (e.g. ` ```json `), prose preambles (e.g., 'Here is the JSON:'), or trailing comments, the response is strictly marked as **invalid JSON** (`is_valid_json = False`).

## Results Summary

### Baseline Model Results
- **Parse Success Rate**: *Pending manual inference*
- **Average Key Accuracy**: *Pending manual inference*
- **Average Value Accuracy**: *Pending manual inference*

### Fine-Tuned Model Results
- **Parse Success Rate**: *Pending manual training and inference*
- **Average Key Accuracy**: *Pending manual training and inference*
- **Average Value Accuracy**: *Pending manual training and inference*

---
For detailed scoring sheets, refer to the following local CSV outputs:
- Baseline Scores: [`eval/baseline_scores.csv`](file:///c:/Users/tnvss/structured-output-finetuning/eval/baseline_scores.csv)
- Fine-Tuned Scores: [`eval/finetuned_scores.csv`](file:///c:/Users/tnvss/structured-output-finetuning/eval/finetuned_scores.csv)