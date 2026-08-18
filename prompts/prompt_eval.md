# Prompt Engineering Evaluation Log

This document records the prompt engineering experiment. Once baseline inference is complete, identify the **three worst-performing documents** and test all three prompt versions (from `prompts/prompt_iterations.md`) on them. 

Record the raw outputs and calculate metrics to evaluate whether prompting alone can resolve structured parsing errors compared to the base model.

---

## Worst Baseline Documents Selected
1. **Candidate 1**: `EVAL_xxx` (Lowest Score)
2. **Candidate 2**: `EVAL_yyy`
3. **Candidate 3**: `EVAL_zzz`

---

## Experiment Matrix & Results

### Document 1: EVAL_xxx
- **Raw Document**:
  ```text
  [Pending: Paste raw document text]
  ```

#### Prompt Version 1
- **Raw Output**:
  ```text
  [Pending: Run baseline model with Prompt 1 and paste raw response verbatim]
  ```
- **valid_json**: `False` / `True` (Pending)
- **has_all_required_keys**: `False` / `True` (Pending)
- **key_accuracy**: `0.0` (Pending)
- **value_accuracy**: `0.0` (Pending)
- **Observations**: [Pending: Record formatting issue, code fences present, or prose preambles]

#### Prompt Version 2
- **Raw Output**:
  ```text
  [Pending: Run baseline model with Prompt 2 and paste raw response verbatim]
  ```
- **valid_json**: `False` / `True` (Pending)
- **has_all_required_keys**: `False` / `True` (Pending)
- **key_accuracy**: `0.0` (Pending)
- **value_accuracy**: `0.0` (Pending)
- **Observations**: [Pending: Describe if adding schema details improved keys or prevented hallucination]

#### Prompt Version 3
- **Raw Output**:
  ```text
  [Pending: Run baseline model with Prompt 3 and paste raw response verbatim]
  ```
- **valid_json**: `False` / `True` (Pending)
- **has_all_required_keys**: `False` / `True` (Pending)
- **key_accuracy**: `0.0` (Pending)
- **value_accuracy**: `0.0` (Pending)
- **Observations**: [Pending: Check if in-context examples resolved array formatting or date constraints]

---

### Document 2: EVAL_yyy
- **Raw Document**:
  ```text
  [Pending: Paste raw document text]
  ```

#### Prompt Version 1
- **Raw Output**:
  ```text
  [Pending]
  ```
- **valid_json**: `Pending`
- **has_all_required_keys**: `Pending`
- **key_accuracy**: `Pending`
- **value_accuracy**: `Pending`
- **Observations**: [Pending]

#### Prompt Version 2
- **Raw Output**:
  ```text
  [Pending]
  ```
- **valid_json**: `Pending`
- **has_all_required_keys**: `Pending`
- **key_accuracy**: `Pending`
- **value_accuracy**: `Pending`
- **Observations**: [Pending]

#### Prompt Version 3
- **Raw Output**:
  ```text
  [Pending]
  ```
- **valid_json**: `Pending`
- **has_all_required_keys**: `Pending`
- **key_accuracy**: `Pending`
- **value_accuracy**: `Pending`
- **Observations**: [Pending]

---

### Document 3: EVAL_zzz
- **Raw Document**:
  ```text
  [Pending: Paste raw document text]
  ```

#### Prompt Version 1
- **Raw Output**:
  ```text
  [Pending]
  ```
- **valid_json**: `Pending`
- **has_all_required_keys**: `Pending`
- **key_accuracy**: `Pending`
- **value_accuracy**: `Pending`
- **Observations**: [Pending]

#### Prompt Version 2
- **Raw Output**:
  ```text
  [Pending]
  ```
- **valid_json**: `Pending`
- **has_all_required_keys**: `Pending`
- **key_accuracy**: `Pending`
- **value_accuracy**: `Pending`
- **Observations**: [Pending]

#### Prompt Version 3
- **Raw Output**:
  ```text
  [Pending]
  ```
- **valid_json**: `Pending`
- **has_all_required_keys**: `Pending`
- **key_accuracy**: `Pending`
- **value_accuracy**: `Pending`
- **Observations**: [Pending]
