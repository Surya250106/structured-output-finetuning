# Structured Output Fine-Tuning: Train Llama 3.2 for Reliable JSON Extraction

This repository contains the complete dataset, validation utilities, evaluation scaffolding, prompt engineering iterations, and training documentation for fine-tuning **Llama 3.2 3B Instruct** to perform strict, structured data extraction of Invoices and Purchase Orders.

---

## Project Objective & Problem Statement
Extracting structured data from unstructured text is a key requirement in data engineering pipelines. General LLMs, while capable of understanding documents, frequently fail at formatting reliability:
1. They output conversational preambles (e.g. *"Here is the requested JSON..."*).
2. They wrap data in markdown code blocks (e.g. ` ```json `).
3. They fail to preserve data types or key schemas under novel layouts.

This project addresses these challenges by comparing **Prompt Engineering** with **Parameter-Efficient LoRA Fine-Tuning** to achieve 100% compliant JSON structures directly parseable by downstream code without regex cleaning.

---

## Repository Structure

```
structured-output-finetuning/
├── README.md                          # Master documentation & handoff guide
├── training_config.md                 # LlamaFactory setups & hyperparameter guides
├── report.md                          # Prompting vs Fine-Tuning comparative report
├── .gitignore                         # Exclude cache, checkpoints, and local evaluation set
├── validate_data.py                   # Automated script to audit dataset constraints
├── evaluate_inference.py              # Automated evaluator to compute metrics and compile CSVs
│
├── schema/
│   ├── invoice_schema.md              # Invoice schema definitions and JSON examples
│   └── po_schema.md                   # Purchase order schema definitions and JSON examples
│
├── data/
│   ├── curated_train.jsonl            # Exactly 80 curated training examples (50 Invoices, 30 POs)
│   ├── evaluation_set.jsonl           # 20 held-out evaluation examples (10 Invoices, 10 POs)
│   └── curation_log.md                # Data provenance details & curation decisions
│
├── screenshots/
│   ├── training_config.png            # LlamaFactory WebUI parameters (Capture manually)
│   └── loss_curve.png                 # LlamaFactory training loss chart (Capture manually)
│
├── eval/
│   ├── baseline_responses.md          # Verbatim baseline model raw outputs (Paste manually)
│   ├── baseline_scores.csv            # Auto-generated baseline score sheet
│   ├── summary.md                     # Parse success rates & scoring definitions
│   ├── finetuned_responses.md         # Verbatim fine-tuned model raw outputs (Paste manually)
│   ├── finetuned_scores.csv           # Auto-generated fine-tuned score sheet
│   ├── before_vs_after.md             # Auto-generated metrics comparison table
│   └── failures/                      # Deep-dives for 5 model failures (Fill manually)
│       ├── failure_01.md
│       ├── failure_02.md
│       ├── failure_03.md
│       ├── failure_04.md
│       └── failure_05.md
│
└── prompts/
    ├── prompt_iterations.md           # Three prompt variants for evaluation
    └── prompt_eval.md                 # Evaluation scaffolding for worst documents
```

---

## Completed Automatically

The following assets are fully initialized and verified:
1. **Schemas (`schema/`)**: Detailed targets with ISO formatting rules and missing-field definitions.
2. **Curated Train Data (`data/curated_train.jsonl`)**: Exactly 80 examples (50 invoices, 30 purchase orders) with data provenance, optional field omissions (tax, due_date, delivery_date as null), multi-item lines, non-USD currencies (INR, EUR, GBP, JPY), and diverse raw text layouts.
3. **Curation Log (`data/curation_log.md`)**: Complete provenance list mapping examples to SROIE/CORD IDs or synthetic labels, with kept/rejected audits.
4. **Evaluation Set (`data/evaluation_set.jsonl`)**: 20 held-out documents completely disjoint from training (checked for exact or normalized input overlap).
5. **Scaffolding Files**: Verbatim response headers, failure templates, prompt iteration logs, and summary templates.
6. **Automation Code**:
   - `validate_data.py`: Audits training split, counts, duplicate records, overlap, and schema compliance.
   - `evaluate_inference.py`: Grade raw response logs strictly, generates score CSVs, before-vs-after comparison, and identifies worst documents.

---

## Requires Manual Experiment Data (Your Handoff Workflow)

To complete the ML experiment, you must execute the following workflow:

### Step 1: Run Baseline Inference
1. Query the base `Llama-3.2-3B-Instruct` model with the 20 documents in `data/evaluation_set.jsonl` using the target prompt:
   *"Extract all fields and return ONLY a valid JSON object. No explanation, no markdown, no code fences."*
2. Paste the verbatim raw responses into `eval/baseline_responses.md` under the corresponding document headers.
3. Run `python evaluate_inference.py`. This will generate `eval/baseline_scores.csv` and report the worst-performing documents in console.

### Step 2: Run Prompt Engineering Experiment
1. Note the three worst-performing baseline documents reported.
2. Query the base model on these three documents using Prompt 2 and Prompt 3 (from `prompts/prompt_iterations.md`).
3. Record raw outputs and observations in `prompts/prompt_eval.md`.

### Step 3: Run LlamaFactory Fine-Tuning
1. Set up LlamaFactory on your GPU environment (see detailed commands in `training_config.md`).
2. Copy `data/curated_train.jsonl` to LlamaFactory, register it in `dataset_info.json`, and open the WebUI (`llamafactory-cli webui`).
3. Set parameters: LoRA, target modules all, learning rate 2e-4, epochs 3, rank 16, alpha 32.
4. Capture a screenshot of this setup and save to `screenshots/training_config.png`.
5. Execute training. Once completed, copy the generated loss curve and save to `screenshots/loss_curve.png`.

### Step 4: Run Fine-Tuned Inference & Scoring
1. Load the fine-tuned model (with LoRA adapter).
2. Query the model on the same 20 evaluation documents using the target prompt.
3. Paste the verbatim raw responses into `eval/finetuned_responses.md`.
4. Run `python evaluate_inference.py`. This will automatically score the fine-tuned outputs, write `eval/finetuned_scores.csv`, and generate the metrics comparison table in `eval/before_vs_after.md`.

### Step 5: Failure Analysis & Final Report
1. Select 5 actual failures (e.g. from baseline or fine-tuned outputs) and document them in `eval/failures/failure_01.md` through `failure_05.md`.
2. Open `report.md` and complete the final findings and executive summary sections using the metrics generated by `evaluate_inference.py`.

---

## Reproduction and Validation Commands

To check repository integrity at any time, run:

1. **Verify Training/Evaluation Dataset Integrity**:
   ```bash
   python validate_data.py
   ```
2. **Execute Metric Calculations**:
   ```bash
   python evaluate_inference.py
   ```

---

## Submission Checklist
- [ ] `schema/invoice_schema.md` and `schema/po_schema.md` are present.
- [ ] `data/curated_train.jsonl` has exactly 80 valid JSON lines (50 invoices, 30 POs).
- [ ] `data/curation_log.md` documents SROIE/CORD provenance and rejection entries.
- [ ] `validate_data.py` passes with zero errors.
- [ ] `eval/baseline_responses.md` contains 20 actual verbatim raw responses.
- [ ] `eval/finetuned_responses.md` contains 20 actual verbatim raw responses.
- [ ] `eval/baseline_scores.csv` and `eval/finetuned_scores.csv` contain scores.
- [ ] `eval/before_vs_after.md` is populated with actual model comparisons.
- [ ] `eval/failures/` contains 5 real failure analyses.
- [ ] `prompts/prompt_eval.md` has the prompt variant experiment documented.
- [ ] `screenshots/training_config.png` shows LlamaFactory parameter inputs.
- [ ] `screenshots/loss_curve.png` shows training loss descent.
- [ ] `report.md` contains completed executive summary and conclusions.
- [ ] No `.safetensors`, `.bin`, `.gguf`, or checkpoint files are committed.
