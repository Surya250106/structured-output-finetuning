import json
import os
import re
import csv

# Paths
EVAL_SET_PATH = "data/evaluation_set.jsonl"
BASELINE_RESP_PATH = "eval/baseline_responses.md"
FINETUNED_RESP_PATH = "eval/finetuned_responses.md"

BASELINE_CSV_PATH = "eval/baseline_scores.csv"
FINETUNED_CSV_PATH = "eval/finetuned_scores.csv"
SUMMARY_PATH = "eval/summary.md"
BEFORE_AFTER_PATH = "eval/before_vs_after.md"

def normalize_val(v):
    """Normalize values for robust evaluation (string stripping, lowcase, float rounding)."""
    if isinstance(v, str):
        return re.sub(r'\s+', ' ', v).strip().lower()
    if isinstance(v, (int, float)):
        return round(float(v), 2)
    if isinstance(v, list):
        # List of items/line_items: normalize each nested object
        norm_list = []
        for item in v:
            if isinstance(item, dict):
                norm_list.append({k: normalize_val(val) for k, val in item.items()})
            else:
                norm_list.append(normalize_val(item))
        # Sort list by its serialized representation to ignore ordering differences
        return sorted(norm_list, key=lambda x: json.dumps(x, sort_keys=True))
    if isinstance(v, dict):
        return {k: normalize_val(val) for k, val in v.items()}
    return v

def extract_nested_json(text):
    """Helper to try to extract a JSON block from prose for scoring, even if raw is invalid."""
    # Look for code block ```json ... ``` or plain ``` ... ``` or just first { ... }
    match = re.search(r'```(?:json)?\s*(\{[\s\S]+?\})\s*```', text)
    if match:
        return match.group(1)
    match = re.search(r'(\{[\s\S]+\})', text)
    if match:
        return match.group(1)
    return None

def parse_responses_md(filepath):
    """Parse the raw response file and extract raw text for each document ID."""
    if not os.path.exists(filepath):
        return None
        
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Split content by document header
    # Header format: ## Document: EVAL_XXX
    # Raw Output format: ### Raw Output:\n```[text]\n[Verbatim raw output]\n```
    sections = re.split(r'## Document:\s*(EVAL_\d+)', content)
    
    responses = {}
    if len(sections) < 2:
        return responses
        
    for i in range(1, len(sections), 2):
        eval_id = sections[i]
        sec_body = sections[i+1]
        
        # Extract text in raw output block
        # We look for: ### Raw Output:\n```[optional language]\n[RAW_CONTENT]\n```
        raw_match = re.search(r'### Raw Output:\s*\n```[a-zA-Z0-9]*\n([\s\S]*?)\n```', sec_body)
        if raw_match:
            responses[eval_id] = raw_match.group(1)
        else:
            # Fallback if no block found
            responses[eval_id] = ""
            
    return responses

def evaluate_single_response(raw_output, gt_json):
    """Evaluate raw response against ground truth JSON, returning scores and notes."""
    is_valid_json = False
    has_all_required_keys = False
    key_accuracy = 0.0
    value_accuracy = 0.0
    notes_list = []
    
    # 1. Determine RAW validity (must be directly loadable as JSON)
    try:
        parsed_json = json.loads(raw_output.strip())
        is_valid_json = True
    except json.JSONDecodeError:
        is_valid_json = False
        notes_list.append("Raw output is not valid JSON (contains prose or code fences)")
        
    # 2. Try to extract JSON for scoring keys/values even if raw is invalid
    json_to_score = None
    if is_valid_json:
        json_to_score = parsed_json
    else:
        extracted = extract_nested_json(raw_output)
        if extracted:
            try:
                json_to_score = json.loads(extracted)
                notes_list.append("Underlying JSON was successfully extracted and parsed")
            except json.JSONDecodeError:
                notes_list.append("Failed to parse extracted JSON block")
                
    if not json_to_score:
        notes_list.append("No parseable JSON structure found")
        return is_valid_json, has_all_required_keys, 0.0, 0.0, "; ".join(notes_list)
        
    # 3. Assess Schema Keys
    doc_type = "Invoice" if "line_items" in gt_json else "Purchase Order"
    if doc_type == "Invoice":
        required_keys = ["vendor", "invoice_number", "date", "currency", "subtotal", "total", "line_items"]
        all_keys = required_keys + ["due_date", "tax"]
    else:
        required_keys = ["buyer", "supplier", "po_number", "date", "currency", "total", "items"]
        all_keys = required_keys + ["delivery_date"]
        
    # Count present keys
    present_keys = [k for k in all_keys if k in json_to_score]
    required_present = [k for k in required_keys if k in json_to_score]
    
    has_all_required_keys = len(required_present) == len(required_keys)
    if not has_all_required_keys:
        missing_req = set(required_keys) - set(required_present)
        notes_list.append(f"Missing required keys: {', '.join(missing_req)}")
        
    key_accuracy = len(present_keys) / len(all_keys)
    
    # 4. Assess Value Accuracy (on keys that are present)
    matches = 0
    total_compared = 0
    
    for key in present_keys:
        val_pred = json_to_score[key]
        val_gt = gt_json.get(key)
        
        # Omitted optional field match
        if val_pred is None and val_gt is None:
            matches += 1
            total_compared += 1
            continue
            
        # Field comparison
        if key in ["line_items", "items"]:
            # Evaluate nested list
            if not isinstance(val_pred, list):
                total_compared += 1
                notes_list.append(f"Key '{key}' is not an array")
                continue
                
            # Compare nested items
            item_key = "description" if key == "line_items" else "item_name"
            # Normalize list items
            norm_pred_list = []
            for item in val_pred:
                if isinstance(item, dict):
                    norm_pred_list.append({k: normalize_val(val) for k, val in item.items()})
                    
            norm_gt_list = [{k: normalize_val(val) for k, val in item.items()} for item in val_gt]
            
            # Match item by item
            matched_items = 0
            for gt_item in norm_gt_list:
                # Find matching item in prediction
                found_match = False
                for i, pred_item in enumerate(norm_pred_list):
                    # Compare description/item_name, quantity, unit_price
                    desc_match = pred_item.get(item_key) == gt_item.get(item_key)
                    qty_match = pred_item.get("quantity") == gt_item.get("quantity")
                    price_match = pred_item.get("unit_price") == gt_item.get("unit_price")
                    
                    if desc_match and qty_match and price_match:
                        matched_items += 1
                        norm_pred_list.pop(i) # remove to prevent duplicate matching
                        found_match = True
                        break
                        
                total_compared += 1 # compare each item
                if found_match:
                    matches += 1
                else:
                    notes_list.append(f"Unmatched item: {gt_item.get(item_key)}")
                    
        else:
            # Scalar comparison
            total_compared += 1
            norm_pred = normalize_val(val_pred)
            norm_gt = normalize_val(val_gt)
            if norm_pred == norm_gt:
                matches += 1
            else:
                notes_list.append(f"Value mismatch for '{key}': expected '{val_gt}', got '{val_pred}'")
                
    value_accuracy = matches / total_compared if total_compared > 0 else 0.0
    
    return is_valid_json, has_all_required_keys, round(key_accuracy, 3), round(value_accuracy, 3), "; ".join(notes_list) if notes_list else "Pass"

def write_scores_csv(filepath, scores):
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["filename", "raw_output_first_50_chars", "is_valid_json", "has_all_required_keys", "key_accuracy", "value_accuracy", "notes"])
        for row in scores:
            writer.writerow(row)

def main():
    print("Inference Evaluation script running...")
    os.makedirs("eval/failures", exist_ok=True)
    
    # 1. Load ground truth
    if not os.path.exists(EVAL_SET_PATH):
        print(f"ERROR: Ground truth set not found at {EVAL_SET_PATH}")
        return False
        
    gt_set = {}
    with open(EVAL_SET_PATH, "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            gt_set[obj["eval_id"]] = {
                "document_type": obj["document_type"],
                "ground_truth": json.loads(obj["ground_truth"])
            }
            
    # 2. Check and parse Baseline Responses
    baseline_pending = True
    baseline_scores = []
    baseline_success_count = 0
    baseline_valid_json_count = 0
    baseline_required_keys_count = 0
    baseline_fences_count = 0
    baseline_preamble_count = 0
    baseline_wrong_keys_count = 0
    baseline_key_acc_sum = 0.0
    baseline_val_acc_sum = 0.0
    
    baseline_responses = parse_responses_md(BASELINE_RESP_PATH)
    
    # Verify file matches evaluation IDs and is not containing pending placeholder
    if baseline_responses and not any("Pending" in v for v in baseline_responses.values()):
        baseline_pending = False
        print("Parsing Baseline Responses...")
        for eval_id, raw_output in baseline_responses.items():
            if eval_id not in gt_set:
                print(f"WARNING: Output ID {eval_id} not found in evaluation ground truth set.")
                continue
                
            gt_json = gt_set[eval_id]["ground_truth"]
            is_valid, has_req, key_acc, val_acc, notes = evaluate_single_response(raw_output, gt_json)
            
            # Statistics
            if is_valid:
                baseline_valid_json_count += 1
            if has_req:
                baseline_required_keys_count += 1
            if is_valid and has_req:
                baseline_success_count += 1
            
            if "```" in raw_output:
                baseline_fences_count += 1
            if any(raw_output.strip().lower().startswith(x) for x in ["here", "sure", "ok", "yes", "the json"]):
                baseline_preamble_count += 1
            if "Missing required keys" in notes:
                baseline_wrong_keys_count += 1
                
            baseline_key_acc_sum += key_acc
            baseline_val_acc_sum += val_acc
            
            first_50 = raw_output.strip()[:50].replace("\n", " ")
            baseline_scores.append([eval_id, first_50, is_valid, has_req, key_acc, val_acc, notes])
            
        write_scores_csv(BASELINE_CSV_PATH, baseline_scores)
        print(f"Completed baseline scoring. Success rate: {baseline_success_count}/20")
    else:
        print("Baseline responses are pending. Creating pending baseline CSV...")
        # Write empty template CSV
        write_scores_csv(BASELINE_CSV_PATH, [["EVAL_xxx", "Pending actual evaluation.", "False", "False", "0.0", "0.0", "Pending"]])
        
    # 3. Check and parse Fine-tuned Responses
    finetuned_pending = True
    finetuned_scores = []
    finetuned_success_count = 0
    finetuned_valid_json_count = 0
    finetuned_required_keys_count = 0
    finetuned_fences_count = 0
    finetuned_preamble_count = 0
    finetuned_wrong_keys_count = 0
    finetuned_key_acc_sum = 0.0
    finetuned_val_acc_sum = 0.0
    
    finetuned_responses = parse_responses_md(FINETUNED_RESP_PATH)
    
    if finetuned_responses and not any("Pending" in v for v in finetuned_responses.values()):
        finetuned_pending = False
        print("Parsing Fine-Tuned Responses...")
        for eval_id, raw_output in finetuned_responses.items():
            if eval_id not in gt_set:
                print(f"WARNING: Output ID {eval_id} not found in evaluation ground truth set.")
                continue
                
            gt_json = gt_set[eval_id]["ground_truth"]
            is_valid, has_req, key_acc, val_acc, notes = evaluate_single_response(raw_output, gt_json)
            
            # Statistics
            if is_valid:
                finetuned_valid_json_count += 1
            if has_req:
                finetuned_required_keys_count += 1
            if is_valid and has_req:
                finetuned_success_count += 1
            
            if "```" in raw_output:
                finetuned_fences_count += 1
            if any(raw_output.strip().lower().startswith(x) for x in ["here", "sure", "ok", "yes", "the json"]):
                finetuned_preamble_count += 1
            if "Missing required keys" in notes:
                finetuned_wrong_keys_count += 1
                
            finetuned_key_acc_sum += key_acc
            finetuned_val_acc_sum += val_acc
            
            first_50 = raw_output.strip()[:50].replace("\n", " ")
            finetuned_scores.append([eval_id, first_50, is_valid, has_req, key_acc, val_acc, notes])
            
        write_scores_csv(FINETUNED_CSV_PATH, finetuned_scores)
        print(f"Completed fine-tuned scoring. Success rate: {finetuned_success_count}/20")
    else:
        print("Fine-tuned responses are pending. Creating pending fine-tuned CSV...")
        write_scores_csv(FINETUNED_CSV_PATH, [["EVAL_xxx", "Pending actual evaluation.", "False", "False", "0.0", "0.0", "Pending"]])
        
    # 4. Generate summary.md
    summary_md = []
    summary_md.append("# Evaluation Summary and Methodology")
    summary_md.append("")
    summary_md.append("This document outlines the metrics, scoring formulas, and results for extracting structured outputs from invoices and purchase orders.")
    summary_md.append("")
    summary_md.append("## Metric Definitions")
    summary_md.append("")
    summary_md.append("- **Parse Success Rate**: The fraction of documents where the model returned direct, valid JSON (no markdown fences, prose, or preambles) containing all required keys. Formula:")
    summary_md.append("  $$\\text{Parse Success Rate} = \\frac{\\text{Count}(\\text{valid JSON} \\land \\text{has all required keys})}{20}$$")
    summary_md.append("- **Key Accuracy**: The average fraction of expected schema keys (both required and optional) present in the parsed output JSON block.")
    summary_md.append("- **Value Accuracy**: The average fraction of matching values for the keys that are present, normalized for harmless whitespace and float trailing differences.")
    summary_md.append("- **Strict RAW Parsing Rule**: If the raw model response contains markdown backticks (e.g. ` ```json `), prose preambles (e.g., 'Here is the JSON:'), or trailing comments, the response is strictly marked as **invalid JSON** (`is_valid_json = False`).")
    summary_md.append("")
    summary_md.append("## Results Summary")
    summary_md.append("")
    
    if baseline_pending:
        summary_md.append("### Baseline Model Results")
        summary_md.append("- **Parse Success Rate**: *Pending manual inference*")
        summary_md.append("- **Average Key Accuracy**: *Pending manual inference*")
        summary_md.append("- **Average Value Accuracy**: *Pending manual inference*")
    else:
        avg_key = baseline_key_acc_sum / 20
        avg_val = baseline_val_acc_sum / 20
        success_pct = (baseline_success_count / 20) * 100
        summary_md.append("### Baseline Model Results")
        summary_md.append(f"- **Parse Success Rate**: {success_pct:.1f}% ({baseline_success_count}/20)")
        summary_md.append(f"- **Average Key Accuracy**: {avg_key:.3f}")
        summary_md.append(f"- **Average Value Accuracy**: {avg_val:.3f}")
        
    summary_md.append("")
    
    if finetuned_pending:
        summary_md.append("### Fine-Tuned Model Results")
        summary_md.append("- **Parse Success Rate**: *Pending manual training and inference*")
        summary_md.append("- **Average Key Accuracy**: *Pending manual training and inference*")
        summary_md.append("- **Average Value Accuracy**: *Pending manual training and inference*")
    else:
        avg_key = finetuned_key_acc_sum / 20
        avg_val = finetuned_val_acc_sum / 20
        success_pct = (finetuned_success_count / 20) * 100
        summary_md.append("### Fine-Tuned Model Results")
        summary_md.append(f"- **Parse Success Rate**: {success_pct:.1f}% ({finetuned_success_count}/20)")
        summary_md.append(f"- **Average Key Accuracy**: {avg_key:.3f}")
        summary_md.append(f"- **Average Value Accuracy**: {avg_val:.3f}")
        
    summary_md.append("")
    summary_md.append("---")
    summary_md.append("For detailed scoring sheets, refer to the following local CSV outputs:")
    summary_md.append("- Baseline Scores: [`eval/baseline_scores.csv`](file:///c:/Users/tnvss/structured-output-finetuning/eval/baseline_scores.csv)")
    summary_md.append("- Fine-Tuned Scores: [`eval/finetuned_scores.csv`](file:///c:/Users/tnvss/structured-output-finetuning/eval/finetuned_scores.csv)")
    
    with open(SUMMARY_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(summary_md))
        
    # 5. Generate before_vs_after.md table
    before_after = []
    before_after.append("# Before-vs-After Fine-Tuning Comparison")
    before_after.append("")
    before_after.append("This table compares extraction reliability metrics of Llama 3.2 3B Instruct before and after LoRA fine-tuning on the 20 held-out evaluation documents.")
    before_after.append("")
    before_after.append("| Metric | Base Model | Fine-Tuned |")
    before_after.append("| :--- | :---: | :---: |")
    
    if baseline_pending:
        base_rate = "Pending"
        base_key = "Pending"
        base_val = "Pending"
        base_fences = "Pending"
        base_preamble = "Pending"
        base_wrong_keys = "Pending"
    else:
        base_rate = f"{(baseline_success_count / 20) * 100:.1f}%"
        base_key = f"{baseline_key_acc_sum / 20:.3f}"
        base_val = f"{baseline_val_acc_sum / 20:.3f}"
        base_fences = f"{baseline_fences_count}/20"
        base_preamble = f"{baseline_preamble_count}/20"
        base_wrong_keys = f"{baseline_wrong_keys_count}/20"
        
    if finetuned_pending:
        ft_rate = "Pending"
        ft_key = "Pending"
        ft_val = "Pending"
        ft_fences = "Pending"
        ft_preamble = "Pending"
        ft_wrong_keys = "Pending"
    else:
        ft_rate = f"{(finetuned_success_count / 20) * 100:.1f}%"
        ft_key = f"{finetuned_key_acc_sum / 20:.3f}"
        ft_val = f"{finetuned_val_acc_sum / 20:.3f}"
        ft_fences = f"{finetuned_fences_count}/20"
        ft_preamble = f"{finetuned_preamble_count}/20"
        ft_wrong_keys = f"{finetuned_wrong_keys_count}/20"
        
    before_after.append(f"| Parse success rate | {base_rate} | {ft_rate} |")
    before_after.append(f"| Avg key accuracy | {base_key} | {ft_key} |")
    before_after.append(f"| Avg value accuracy | {base_val} | {ft_val} |")
    before_after.append(f"| Responses with markdown fences | {base_fences} | {ft_fences} |")
    before_after.append(f"| Responses with prose preamble | {base_preamble} | {ft_preamble} |")
    before_after.append(f"| Responses with wrong schema keys | {base_wrong_keys} | {ft_wrong_keys} |")
    
    before_after.append("")
    before_after.append("---")
    before_after.append("### Evaluation Findings")
    before_after.append("")
    if baseline_pending and finetuned_pending:
        before_after.append("Awaiting execution of baseline and fine-tuned model inference to record findings.")
    else:
        before_after.append("Model evaluation complete. Running this script has updated all metric comparisons above.")
        
    with open(BEFORE_AFTER_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(before_after))
        
    # 6. Print helper analysis for worst baseline documents
    if not baseline_pending:
        print("\nIDENTIFIED WORST BASELINE DOCUMENTS (Candidates for Prompt Engineering):")
        # Sort baseline scores by value_accuracy then key_accuracy
        sorted_scores = sorted(baseline_scores, key=lambda x: (x[5], x[4]))
        worst_count = min(3, len(sorted_scores))
        for j in range(worst_count):
            row = sorted_scores[j]
            print(f" - {row[0]}: Key Acc={row[4]}, Val Acc={row[5]}, Note={row[6][:60]}...")
            
    return True

if __name__ == "__main__":
    main()
