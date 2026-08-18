# Invoice Schema Definition

This document defines the strict target schema for extracting structured invoice information from raw documents. All training examples and model evaluations must conform precisely to this specification.

---

## Fields and Specifications

| Field Name | Data Type | Semantic Meaning | Status | Format / Constraints | Missing-Value Behavior |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`vendor`** | `string` | The legal name of the entity issuing the invoice (seller). | **Required** | Non-empty string. | Reject record. |
| **`invoice_number`** | `string` | The unique identifier assigned by the vendor for tracking this transaction. | **Required** | Non-empty string. | Reject record. |
| **`date`** | `string` | The date when the invoice was officially issued. | **Required** | Strict ISO format: `YYYY-MM-DD`. | Reject record. |
| **`due_date`** | `string` or `null` | The deadline date for payment of the invoice. | *Optional* | Strict ISO format: `YYYY-MM-DD`, or `null`. | Map to `null`. |
| **`currency`** | `string` | The currency used for prices and totals. | **Required** | Strict 3-letter ISO 4217 code (e.g., `USD`, `EUR`, `INR`). | Reject record. |
| **`subtotal`** | `float` | The total amount of all line items before taxes or additional fees. | **Required** | Numeric float. Must match the sum of line items. | Reject record. |
| **`tax`** | `float` or `null` | The tax amount applied (VAT, GST, sales tax, etc.). | *Optional* | Numeric float, or `null`. | Map to `null`. |
| **`total`** | `float` | The final amount payable, inclusive of taxes and fees. | **Required** | Numeric float. Must equal `subtotal + tax` (if tax is not null). | Reject record. |
| **`line_items`** | `array` | A list of individual products or services invoiced. | **Required** | Array of objects matching the item schema below. | Reject record (or empty array if none). |

### Nested Line Item Fields (`line_items[*]`)

| Field Name | Data Type | Semantic Meaning | Status | Constraints | Missing-Value Behavior |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`description`** | `string` | Description of the product, service, or work completed. | **Required** | Non-empty string. | Map to `""`. |
| **`quantity`** | `integer` | The quantity of items, hours, or units billed. | **Required** | Integer greater than 0. | Reject record. |
| **`unit_price`** | `float` | The cost per individual unit or hour. | **Required** | Numeric float. | Reject record. |

---

## Missing-Value Policy

To maintain schema consistency and robust model extraction:
1. **Required Fields**: If the raw document is ambiguous or lacks a required field (e.g., missing vendor name, total, or invoice number), the document **must be rejected** during data curation. We do not fabricate or guess required values.
2. **Optional Date Fields**: If the due date is absent, it must be represented as `null`.
3. **Optional Tax Field**: If no tax is mentioned, it must be represented as `null`.
4. **Missing Line Item Description**: If a line item has quantity and price but lacks description, it defaults to `""`.
5. **No Placeholders**: Do not use placeholders like `"N/A"`, `"None"`, or `0.0` for missing fields; map them to `null` or empty string `""` exactly as described.

---

## Valid JSON Examples

### Example 1: Full Fields (USD)

```json
{
  "vendor": "Acme Industrial Supplies Ltd",
  "invoice_number": "INV-2026-8941",
  "date": "2026-08-15",
  "due_date": "2026-09-15",
  "currency": "USD",
  "subtotal": 1250.00,
  "tax": 100.00,
  "total": 1350.00,
  "line_items": [
    {
      "description": "Heavy Duty Steel Bracket (M12)",
      "quantity": 100,
      "unit_price": 10.00
    },
    {
      "description": "Industrial Lubricant Spray 400ml",
      "quantity": 10,
      "unit_price": 25.00
    }
  ]
}
```

### Example 2: Missing Optional Fields (EUR)

```json
{
  "vendor": "TechSolutions Europe GmbH",
  "invoice_number": "TS-99824",
  "date": "2026-08-01",
  "due_date": null,
  "currency": "EUR",
  "subtotal": 4500.00,
  "tax": null,
  "total": 4500.00,
  "line_items": [
    {
      "description": "Senior Software Architect Consulting (Hours)",
      "quantity": 30,
      "unit_price": 150.00
    }
  ]
}
```
