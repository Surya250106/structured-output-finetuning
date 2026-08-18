# Purchase Order (PO) Schema Definition

This document defines the strict target schema for extracting structured purchase order information from raw documents. All training examples and model evaluations must conform precisely to this specification.

---

## Fields and Specifications

| Field Name | Data Type | Semantic Meaning | Status | Format / Constraints | Missing-Value Behavior |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`buyer`** | `string` | The company or entity issuing the purchase order (purchaser). | **Required** | Non-empty string. | Reject record. |
| **`supplier`** | `string` | The vendor or seller supplying the goods/services. | **Required** | Non-empty string. | Reject record. |
| **`po_number`** | `string` | The unique identifier assigned by the buyer for tracking. | **Required** | Non-empty string. | Reject record. |
| **`date`** | `string` | The issue date of the purchase order. | **Required** | Strict ISO format: `YYYY-MM-DD`. | Reject record. |
| **`delivery_date`** | `string` or `null` | The requested or expected date for delivery. | *Optional* | Strict ISO format: `YYYY-MM-DD`, or `null`. | Map to `null`. |
| **`currency`** | `string` | The currency used for pricing and totals. | **Required** | Standard currency code or string (e.g. `USD`, `EUR`, `INR`, `GBP`). | Reject record. |
| **`total`** | `float` | The total authorized amount for this purchase order. | **Required** | Numeric float. Must match the sum of items. | Reject record. |
| **`items`** | `array` | The list of items being ordered. | **Required** | Array of objects matching the item schema below. | Reject record (or empty array if none). |

### Nested PO Item Fields (`items[*]`)

| Field Name | Data Type | Semantic Meaning | Status | Constraints | Missing-Value Behavior |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`item_name`** | `string` | The name or catalog description of the item ordered. | **Required** | Non-empty string. | Map to `""`. |
| **`quantity`** | `integer` | The number of units ordered. | **Required** | Integer greater than 0. | Reject record. |
| **`unit_price`** | `float` | The price per unit of the item. | **Required** | Numeric float. | Reject record. |

---

## Missing-Value Policy

To maintain schema consistency and robust model extraction:
1. **Required Fields**: If the raw document is ambiguous or lacks a required field (e.g., missing buyer, supplier, PO number, or total), the document **must be rejected** during data curation. We do not fabricate required values.
2. **Optional Date Fields**: If the delivery date is absent, it must be represented as `null`.
3. **Missing Item Name**: If an item entry has quantity and price but lacks an item name, it defaults to `""`.
4. **No Placeholders**: Do not use placeholders like `"N/A"`, `"None"`, or `0.0` for missing fields; map them to `null` or empty string `""` exactly as described.

---

## Valid JSON Examples

### Example 1: Full Fields (GBP)

```json
{
  "buyer": "Global Logistics UK Ltd",
  "supplier": "EuroPackaging Supplies Ltd",
  "po_number": "PO-88712-2026",
  "date": "2026-08-10",
  "delivery_date": "2026-09-01",
  "currency": "GBP",
  "total": 350.00,
  "items": [
    {
      "item_name": "Standard Cardboard Box Medium",
      "quantity": 500,
      "unit_price": 0.50
    },
    {
      "item_name": "Heavy Duty Packaging Tape (Clear)",
      "quantity": 100,
      "unit_price": 1.00
    }
  ]
}
```

### Example 2: Missing Optional Fields (INR)

```json
{
  "buyer": "Apex Retail India Pvt Ltd",
  "supplier": "Shree Textiles Group",
  "po_number": "PO/TX/26/089",
  "date": "2026-08-18",
  "delivery_date": null,
  "currency": "INR",
  "total": 75000.00,
  "items": [
    {
      "item_name": "Premium Cotton Yarn Grade-A",
      "quantity": 250,
      "unit_price": 300.00
    }
  ]
}
```
