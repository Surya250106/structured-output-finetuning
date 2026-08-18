import json
import os
import re

# Paths
TRAIN_PATH = "data/curated_train.jsonl"
EVAL_PATH = "data/evaluation_set.jsonl"

def normalize_text(text):
    """Normalize text by stripping whitespace and converting to lowercase for duplicate detection."""
    return re.sub(r'\s+', '', text).lower()

def validate_invoice(obj, label):
    required = ["vendor", "invoice_number", "date", "due_date", "currency", "subtotal", "tax", "total", "line_items"]
    for r in required:
        if r not in obj:
            return False, f"[{label}] Missing required invoice field: {r}"
    if not isinstance(obj["vendor"], str) or not obj["vendor"]:
        return False, f"[{label}] vendor must be a non-empty string"
    if not isinstance(obj["invoice_number"], str) or not obj["invoice_number"]:
        return False, f"[{label}] invoice_number must be a non-empty string"
    if not isinstance(obj["date"], str) or not re.match(r'^\d{4}-\d{2}-\d{2}$', obj["date"]):
        return False, f"[{label}] date must be YYYY-MM-DD string, got: {obj['date']}"
    if obj["due_date"] is not None:
        if not isinstance(obj["due_date"], str) or not re.match(r'^\d{4}-\d{2}-\d{2}$', obj["due_date"]):
            return False, f"[{label}] due_date must be YYYY-MM-DD or null, got: {obj['due_date']}"
    if not isinstance(obj["currency"], str) or not re.match(r'^[A-Z]{3}$', obj["currency"]):
        return False, f"[{label}] currency must be 3-letter ISO code, got: {obj['currency']}"
    if not isinstance(obj["subtotal"], (int, float)):
        return False, f"[{label}] subtotal must be float"
    if obj["tax"] is not None and not isinstance(obj["tax"], (int, float)):
        return False, f"[{label}] tax must be float or null"
    if not isinstance(obj["total"], (int, float)):
        return False, f"[{label}] total must be float"
    if not isinstance(obj["line_items"], list) or len(obj["line_items"]) == 0:
        return False, f"[{label}] line_items must be a non-empty array"
    
    for i, item in enumerate(obj["line_items"]):
        for key in ["description", "quantity", "unit_price"]:
            if key not in item:
                return False, f"[{label}] Line item {i} missing key: {key}"
        if not isinstance(item["description"], str):
            return False, f"[{label}] Line item {i} description must be string"
        if not isinstance(item["quantity"], int) or item["quantity"] <= 0:
            return False, f"[{label}] Line item {i} quantity must be positive integer"
        if not isinstance(item["unit_price"], (int, float)):
            return False, f"[{label}] Line item {i} unit_price must be float"
            
    return True, ""

def validate_po(obj, label):
    required = ["buyer", "supplier", "po_number", "date", "delivery_date", "currency", "total", "items"]
    for r in required:
        if r not in obj:
            return False, f"[{label}] Missing required PO field: {r}"
    if not isinstance(obj["buyer"], str) or not obj["buyer"]:
        return False, f"[{label}] buyer must be a non-empty string"
    if not isinstance(obj["supplier"], str) or not obj["supplier"]:
        return False, f"[{label}] supplier must be a non-empty string"
    if not isinstance(obj["po_number"], str) or not obj["po_number"]:
        return False, f"[{label}] po_number must be a non-empty string"
    if not isinstance(obj["date"], str) or not re.match(r'^\d{4}-\d{2}-\d{2}$', obj["date"]):
        return False, f"[{label}] date must be YYYY-MM-DD string, got: {obj['date']}"
    if obj["delivery_date"] is not None:
        if not isinstance(obj["delivery_date"], str) or not re.match(r'^\d{4}-\d{2}-\d{2}$', obj["delivery_date"]):
            return False, f"[{label}] delivery_date must be YYYY-MM-DD or null, got: {obj['delivery_date']}"
    if not isinstance(obj["currency"], str) or not obj["currency"]:
        return False, f"[{label}] currency must be non-empty string, got: {obj['currency']}"
    if not isinstance(obj["total"], (int, float)):
        return False, f"[{label}] total must be float"
    if not isinstance(obj["items"], list) or len(obj["items"]) == 0:
        return False, f"[{label}] items must be a non-empty array"
        
    for i, item in enumerate(obj["items"]):
        for key in ["item_name", "quantity", "unit_price"]:
            if key not in item:
                return False, f"[{label}] PO item {i} missing key: {key}"
        if not isinstance(item["item_name"], str):
            return False, f"[{label}] PO item {i} item_name must be string"
        if not isinstance(item["quantity"], int) or item["quantity"] <= 0:
            return False, f"[{label}] PO item {i} quantity must be positive integer"
        if not isinstance(item["unit_price"], (int, float)):
            return False, f"[{label}] PO item {i} unit_price must be float"
            
    return True, ""

def main():
    errors = []
    
    # 1. Check training file exists
    if not os.path.exists(TRAIN_PATH):
        print(f"ERROR: Training file not found at {TRAIN_PATH}")
        return False
        
    # Read training examples
    train_lines = []
    with open(TRAIN_PATH, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            try:
                train_lines.append(json.loads(line))
            except json.JSONDecodeError as e:
                errors.append(f"Training line {i} is not valid JSON: {str(e)}")
                
    # Read evaluation examples
    eval_lines = []
    if os.path.exists(EVAL_PATH):
        with open(EVAL_PATH, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                try:
                    eval_lines.append(json.loads(line))
                except json.JSONDecodeError as e:
                    errors.append(f"Evaluation line {i} is not valid JSON: {str(e)}")
    else:
        print(f"WARNING: Evaluation set not found at {EVAL_PATH}")

    # If syntax errors already found, abort further check
    if errors:
        print("Dataset Syntax Validation FAILED:")
        for err in errors:
            print(" -", err)
        return False
        
    # 2. Count training examples
    total_train = len(train_lines)
    if total_train != 80:
        errors.append(f"Training set must have exactly 80 examples, got {total_train}")
        
    # Verify JSON structure and count document splits
    invoice_count = 0
    po_count = 0
    optional_omitted_count = 0
    multi_item_count = 0
    non_usd_count = 0
    
    train_inputs_normalized = {}
    
    for idx, obj in enumerate(train_lines, 1):
        # Verify required keys for JSONL format
        for key in ["instruction", "input", "output"]:
            if key not in obj:
                errors.append(f"Training record {idx} missing JSONL key: {key}")
                continue
        if "instruction" not in obj or "input" not in obj or "output" not in obj:
            continue
            
        raw_input = obj["input"]
        output_str = obj["output"]
        
        # Check duplicate inputs in training
        norm_in = normalize_text(raw_input)
        if norm_in in train_inputs_normalized:
            errors.append(f"Training record {idx} is a duplicate of record {train_inputs_normalized[norm_in]} (normalized raw text match)")
        else:
            train_inputs_normalized[norm_in] = idx
            
        # Parse output JSON to validate schema
        try:
            output_json = json.loads(output_str)
        except json.JSONDecodeError as e:
            errors.append(f"Training record {idx} output field is not valid JSON string: {str(e)}")
            continue
            
        # Check document type based on schema keys
        if "line_items" in output_json:
            invoice_count += 1
            is_valid, msg = validate_invoice(output_json, f"Train Rec {idx} (Invoice)")
            if not is_valid:
                errors.append(msg)
            else:
                # Count optional omissions
                omitted = False
                if output_json["due_date"] is None:
                    omitted = True
                if output_json["tax"] is None:
                    omitted = True
                if omitted:
                    optional_omitted_count += 1
                
                # Count multi-items
                if len(output_json["line_items"]) >= 3:
                    multi_item_count += 1
                    
                # Count non-USD currencies
                if output_json["currency"] != "USD":
                    non_usd_count += 1
                    
        elif "items" in output_json:
            po_count += 1
            is_valid, msg = validate_po(output_json, f"Train Rec {idx} (PO)")
            if not is_valid:
                errors.append(msg)
            else:
                # Count optional omissions
                if output_json["delivery_date"] is None:
                    optional_omitted_count += 1
                
                # Count multi-items
                if len(output_json["items"]) >= 3:
                    multi_item_count += 1
                    
                # Count non-USD currencies
                if output_json["currency"] != "USD":
                    non_usd_count += 1
        else:
            errors.append(f"Training record {idx} output schema unrecognized (lacks both line_items and items keys)")

    # 3. Check splits
    if invoice_count != 50:
        errors.append(f"Expected exactly 50 invoices, got {invoice_count}")
    if po_count != 30:
        errors.append(f"Expected exactly 30 purchase orders, got {po_count}")
        
    # 4. Check specific constraints
    if optional_omitted_count < 15:
        errors.append(f"Expected at least 15 examples with missing optional fields, got {optional_omitted_count}")
    if multi_item_count < 10:
        errors.append(f"Expected at least 10 examples with 3+ items, got {multi_item_count}")
    if non_usd_count < 5:
        errors.append(f"Expected at least 5 non-USD examples, got {non_usd_count}")

    # 5. Validate Evaluation set and look for overlap
    eval_count = 0
    eval_invoice_count = 0
    eval_po_count = 0
    overlap_count = 0
    
    eval_inputs_normalized = {}
    
    for idx, obj in enumerate(eval_lines, 1):
        for key in ["eval_id", "document_type", "raw_document", "ground_truth"]:
            if key not in obj:
                errors.append(f"Evaluation record {idx} missing key: {key}")
                continue
        if "eval_id" not in obj or "raw_document" not in obj or "ground_truth" not in obj:
            continue
            
        eval_count += 1
        raw_input = obj["raw_document"]
        gt_str = obj["ground_truth"]
        
        # Check duplicate inputs in evaluation
        norm_in = normalize_text(raw_input)
        if norm_in in eval_inputs_normalized:
            errors.append(f"Evaluation record {idx} ({obj['eval_id']}) is a duplicate of evaluation record {eval_inputs_normalized[norm_in]} (normalized raw text match)")
        else:
            eval_inputs_normalized[norm_in] = obj['eval_id']
            
        # Check overlap with training set
        if norm_in in train_inputs_normalized:
            overlap_count += 1
            errors.append(f"CRITICAL OVERLAP: Evaluation record {idx} ({obj['eval_id']}) input matches training record {train_inputs_normalized[norm_in]}")
            
        # Validate schema of evaluation ground truth
        try:
            gt_json = json.loads(gt_str)
        except json.JSONDecodeError as e:
            errors.append(f"Evaluation record {idx} ground_truth is not valid JSON string: {str(e)}")
            continue
            
        if obj["document_type"] == "Invoice":
            eval_invoice_count += 1
            is_valid, msg = validate_invoice(gt_json, f"Eval Rec {idx} ({obj['eval_id']})")
            if not is_valid:
                errors.append(msg)
        elif obj["document_type"] == "Purchase Order":
            eval_po_count += 1
            is_valid, msg = validate_po(gt_json, f"Eval Rec {idx} ({obj['eval_id']})")
            if not is_valid:
                errors.append(msg)
        else:
            errors.append(f"Evaluation record {idx} ({obj['eval_id']}) has unrecognized document_type: {obj['document_type']}")
            
    # Check evaluation set count and split
    if eval_count > 0:
        if eval_count != 20:
            errors.append(f"Expected exactly 20 evaluation documents, got {eval_count}")
        if eval_invoice_count != 10:
            errors.append(f"Expected exactly 10 evaluation invoices, got {eval_invoice_count}")
        if eval_po_count != 10:
            errors.append(f"Expected exactly 10 evaluation purchase orders, got {eval_po_count}")

    # Output results
    print("----------------------------------------")
    print("DATASET VALIDATION SUMMARY STATUS:")
    print("----------------------------------------")
    print(f"Total training examples:       {total_train} (Target: 80)")
    print(f" - Invoices:                   {invoice_count} (Target: 50)")
    print(f" - Purchase Orders:            {po_count} (Target: 30)")
    print(f" - Optional field omissions:   {optional_omitted_count} (Target: >=15)")
    print(f" - Multi-item records (>=3):   {multi_item_count} (Target: >=10)")
    print(f" - Non-USD currency records:   {non_usd_count} (Target: >=5)")
    print(f"Total evaluation examples:     {eval_count} (Target: 20)")
    print(f" - Eval Invoices:              {eval_invoice_count} (Target: 10)")
    print(f" - Eval Purchase Orders:       {eval_po_count} (Target: 10)")
    print(f"Training/Eval overlap count:   {overlap_count} (Target: 0)")
    
    if errors:
        print("\nDataset Verification FAILED with the following errors:")
        for err in errors:
            print(" [ERROR]", err)
        return False
    else:
        print("\nSUCCESS: All dataset validations and schema constraints are strictly satisfied!")
        return True

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
