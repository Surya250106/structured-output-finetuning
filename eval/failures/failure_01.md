# Failure Analysis 01

This document registers a detailed failure analysis for the fine-tuned model (Llama 3.2 3B Instruct + LoRA adapter) on a specific evaluation document.

> [!IMPORTANT]
> **Pending Actual Fine-Tuned Evaluation**:
> This report must be completed by inspecting actual model outputs in `eval/finetuned_responses.md` that fail to parse, have key/value accuracy errors, or violate formatting constraints.
> The proposed fix must focus on **training data adjustments** (e.g. adding specific layout types, correcting target value representations in `curated_train.jsonl`), not merely prompt modifications.

---

## 1. Source Document

```text
[Pending: Paste raw document text here]
```

## 2. Expected JSON (Ground Truth)

```json
{
  "Pending": "Paste expected JSON here matching schema"
}
```

## 3. Actual Model Response

```text
[Pending: Paste verbatim model response here]
```

## 4. What Went Wrong
- [Pending: Identify key mismatch, parsing error, or formatting failure]

## 5. Failure Diagnosis & Why it Failed
- [Pending: Analyze why the model failed on this specific structure or value. Was it a layout issue? Noise in OCR?]

## 6. Proposed Training Data Fix
- **Dataset Modification**: [Pending: Specify the exact training data change needed. Example: Add 5 more examples of invoice headers that use "Payable to:" instead of "Vendor:"]
- **Rationale**: [Pending: Explain how this dataset change will guide the LoRA adapter to resolve this specific class of errors]
