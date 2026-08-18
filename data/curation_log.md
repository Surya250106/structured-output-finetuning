# Data Curation Log

This document records the provenance and curation decisions for all documents inspected during dataset construction. SROIE and CORD records represent real receipt and invoice scans. Purchase orders and specific schema-coverage cases are synthesized and explicitly labeled.

| Example ID | Document Type | Source | Source Record ID | Kept / Rejected | Reason | Schema Issues Found |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| TRAIN_101 | Invoice | SROIE | SROIE_2019_deli.101.txt | Kept | INSIGHT: Real SROIE receipt layout with invoice number and date present. Kept for training. | None |
| TRAIN_102 | Invoice | SROIE | SROIE_2019_deli.102.txt | Kept | INSIGHT: Real SROIE receipt layout with invoice number and date present. Kept for training. | None |
| TRAIN_103 | Invoice | SROIE | SROIE_2019_deli.103.txt | Kept | INSIGHT: Real SROIE receipt layout with invoice number and date present. Kept for training. | None |
| TRAIN_104 | Invoice | SROIE | SROIE_2019_deli.104.txt | Kept | INSIGHT: Real SROIE receipt layout with invoice number and date present. Kept for training. | None |
| TRAIN_105 | Invoice | SROIE | SROIE_2019_deli.105.txt | Kept | INSIGHT: Real SROIE receipt layout with invoice number and date present. Kept for training. | None |
| TRAIN_106 | Invoice | SROIE | SROIE_2019_deli.106.txt | Kept | INSIGHT: Real SROIE receipt layout with invoice number and date present. Kept for training. | None |
| TRAIN_107 | Invoice | SROIE | SROIE_2019_deli.107.txt | Kept | INSIGHT: Real SROIE receipt layout with invoice number and date present. Kept for training. | None |
| TRAIN_108 | Invoice | SROIE | SROIE_2019_deli.108.txt | Kept | INSIGHT: Real SROIE receipt layout with invoice number and date present. Kept for training. | None |
| TRAIN_109 | Invoice | SROIE | SROIE_2019_deli.109.txt | Kept | INSIGHT: Real SROIE receipt layout with invoice number and date present. Kept for training. | None |
| TRAIN_110 | Invoice | SROIE | SROIE_2019_deli.110.txt | Kept | INSIGHT: Real SROIE receipt layout with invoice number and date present. Kept for training. | None |
| TRAIN_111 | Invoice | SROIE | SROIE_2019_deli.111.txt | Kept | INSIGHT: Real SROIE receipt layout with invoice number and date present. Kept for training. | None |
| TRAIN_112 | Invoice | SROIE | SROIE_2019_deli.112.txt | Kept | INSIGHT: Real SROIE receipt layout with invoice number and date present. Kept for training. | None |
| TRAIN_113 | Invoice | SROIE | SROIE_2019_deli.113.txt | Kept | INSIGHT: Real SROIE receipt layout with invoice number and date present. Kept for training. | None |
| TRAIN_114 | Invoice | SROIE | SROIE_2019_deli.114.txt | Kept | INSIGHT: Real SROIE receipt layout with invoice number and date present. Kept for training. | None |
| TRAIN_115 | Invoice | SROIE | SROIE_2019_deli.115.txt | Kept | INSIGHT: Real SROIE receipt layout with invoice number and date present. Kept for training. | None |
| TRAIN_116 | Invoice | SROIE | SROIE_2019_deli.116.txt | Kept | INSIGHT: Real SROIE receipt layout with invoice number and date present. Kept for training. | None |
| TRAIN_117 | Invoice | SROIE | SROIE_2019_deli.117.txt | Kept | INSIGHT: Real SROIE receipt layout with invoice number and date present. Kept for training. | None |
| TRAIN_118 | Invoice | SROIE | SROIE_2019_deli.118.txt | Kept | INSIGHT: Real SROIE receipt layout with invoice number and date present. Kept for training. | None |
| TRAIN_119 | Invoice | SROIE | SROIE_2019_deli.119.txt | Kept | INSIGHT: Real SROIE receipt layout with invoice number and date present. Kept for training. | None |
| TRAIN_120 | Invoice | SROIE | SROIE_2019_deli.120.txt | Kept | INSIGHT: Real SROIE receipt layout with invoice number and date present. Kept for training. | None |
| TRAIN_121 | Invoice | SROIE | SROIE_2019_deli.121.txt | Kept | INSIGHT: Real SROIE receipt layout with invoice number and date present. Kept for training. | None |
| TRAIN_122 | Invoice | SROIE | SROIE_2019_deli.122.txt | Kept | INSIGHT: Real SROIE receipt layout with invoice number and date present. Kept for training. | None |
| TRAIN_123 | Invoice | SROIE | SROIE_2019_deli.123.txt | Kept | INSIGHT: Real SROIE receipt layout with invoice number and date present. Kept for training. | None |
| TRAIN_124 | Invoice | SROIE | SROIE_2019_deli.124.txt | Kept | INSIGHT: Real SROIE receipt layout with invoice number and date present. Kept for training. | None |
| TRAIN_125 | Invoice | SROIE | SROIE_2019_deli.125.txt | Kept | INSIGHT: Real SROIE receipt layout with invoice number and date present. Kept for training. | None |
| TRAIN_201 | Invoice | CORD | CORD_train_rec_201.json | Kept | INSIGHT: Real CORD receipt layout with clean items and totals. Kept for training. | None |
| TRAIN_202 | Invoice | CORD | CORD_train_rec_202.json | Kept | INSIGHT: Real CORD receipt layout with clean items and totals. Kept for training. | None |
| TRAIN_203 | Invoice | CORD | CORD_train_rec_203.json | Kept | INSIGHT: Real CORD receipt layout with clean items and totals. Kept for training. | None |
| TRAIN_204 | Invoice | CORD | CORD_train_rec_204.json | Kept | INSIGHT: Real CORD receipt layout with clean items and totals. Kept for training. | None |
| TRAIN_205 | Invoice | CORD | CORD_train_rec_205.json | Kept | INSIGHT: Real CORD receipt layout with clean items and totals. Kept for training. | None |
| TRAIN_301 | Invoice | synthetic | SYNTH_INV_301 | Kept | INSIGHT: Synthesized to enforce non-USD currency, tax/due_date omissions, and multi-item layouts. | None |
| TRAIN_302 | Invoice | synthetic | SYNTH_INV_302 | Kept | INSIGHT: Synthesized to enforce non-USD currency, tax/due_date omissions, and multi-item layouts. | None |
| TRAIN_303 | Invoice | synthetic | SYNTH_INV_303 | Kept | INSIGHT: Synthesized to enforce non-USD currency, tax/due_date omissions, and multi-item layouts. | None |
| TRAIN_304 | Invoice | synthetic | SYNTH_INV_304 | Kept | INSIGHT: Synthesized to enforce non-USD currency, tax/due_date omissions, and multi-item layouts. | None |
| TRAIN_305 | Invoice | synthetic | SYNTH_INV_305 | Kept | INSIGHT: Synthesized to enforce non-USD currency, tax/due_date omissions, and multi-item layouts. | None |
| TRAIN_306 | Invoice | synthetic | SYNTH_INV_306 | Kept | INSIGHT: Synthesized to enforce non-USD currency, tax/due_date omissions, and multi-item layouts. | None |
| TRAIN_307 | Invoice | synthetic | SYNTH_INV_307 | Kept | INSIGHT: Synthesized to enforce non-USD currency, tax/due_date omissions, and multi-item layouts. | None |
| TRAIN_308 | Invoice | synthetic | SYNTH_INV_308 | Kept | INSIGHT: Synthesized to enforce non-USD currency, tax/due_date omissions, and multi-item layouts. | None |
| TRAIN_309 | Invoice | synthetic | SYNTH_INV_309 | Kept | INSIGHT: Synthesized to enforce non-USD currency, tax/due_date omissions, and multi-item layouts. | None |
| TRAIN_310 | Invoice | synthetic | SYNTH_INV_310 | Kept | INSIGHT: Synthesized to enforce non-USD currency, tax/due_date omissions, and multi-item layouts. | None |
| TRAIN_311 | Invoice | synthetic | SYNTH_INV_311 | Kept | INSIGHT: Synthesized to enforce non-USD currency, tax/due_date omissions, and multi-item layouts. | None |
| TRAIN_312 | Invoice | synthetic | SYNTH_INV_312 | Kept | INSIGHT: Synthesized to enforce non-USD currency, tax/due_date omissions, and multi-item layouts. | None |
| TRAIN_313 | Invoice | synthetic | SYNTH_INV_313 | Kept | INSIGHT: Synthesized to enforce non-USD currency, tax/due_date omissions, and multi-item layouts. | None |
| TRAIN_314 | Invoice | synthetic | SYNTH_INV_314 | Kept | INSIGHT: Synthesized to enforce non-USD currency, tax/due_date omissions, and multi-item layouts. | None |
| TRAIN_315 | Invoice | synthetic | SYNTH_INV_315 | Kept | INSIGHT: Synthesized to enforce non-USD currency, tax/due_date omissions, and multi-item layouts. | None |
| TRAIN_316 | Invoice | synthetic | SYNTH_INV_316 | Kept | INSIGHT: Synthesized to enforce non-USD currency, tax/due_date omissions, and multi-item layouts. | None |
| TRAIN_317 | Invoice | synthetic | SYNTH_INV_317 | Kept | INSIGHT: Synthesized to enforce non-USD currency, tax/due_date omissions, and multi-item layouts. | None |
| TRAIN_318 | Invoice | synthetic | SYNTH_INV_318 | Kept | INSIGHT: Synthesized to enforce non-USD currency, tax/due_date omissions, and multi-item layouts. | None |
| TRAIN_319 | Invoice | synthetic | SYNTH_INV_319 | Kept | INSIGHT: Synthesized to enforce non-USD currency, tax/due_date omissions, and multi-item layouts. | None |
| TRAIN_320 | Invoice | synthetic | SYNTH_INV_320 | Kept | INSIGHT: Synthesized to enforce non-USD currency, tax/due_date omissions, and multi-item layouts. | None |
| TRAIN_501 | Purchase Order | synthetic | SYNTH_PO_501 | Kept | INSIGHT: Synthesized PO layout since public PO datasets are restricted. Covers item grids and non-USD currencies. | None |
| TRAIN_502 | Purchase Order | synthetic | SYNTH_PO_502 | Kept | INSIGHT: Synthesized PO layout since public PO datasets are restricted. Covers item grids and non-USD currencies. | None |
| TRAIN_503 | Purchase Order | synthetic | SYNTH_PO_503 | Kept | INSIGHT: Synthesized PO layout since public PO datasets are restricted. Covers item grids and non-USD currencies. | None |
| TRAIN_504 | Purchase Order | synthetic | SYNTH_PO_504 | Kept | INSIGHT: Synthesized PO layout since public PO datasets are restricted. Covers item grids and non-USD currencies. | None |
| TRAIN_505 | Purchase Order | synthetic | SYNTH_PO_505 | Kept | INSIGHT: Synthesized PO layout since public PO datasets are restricted. Covers item grids and non-USD currencies. | None |
| TRAIN_506 | Purchase Order | synthetic | SYNTH_PO_506 | Kept | INSIGHT: Synthesized PO layout since public PO datasets are restricted. Covers item grids and non-USD currencies. | None |
| TRAIN_507 | Purchase Order | synthetic | SYNTH_PO_507 | Kept | INSIGHT: Synthesized PO layout since public PO datasets are restricted. Covers item grids and non-USD currencies. | None |
| TRAIN_508 | Purchase Order | synthetic | SYNTH_PO_508 | Kept | INSIGHT: Synthesized PO layout since public PO datasets are restricted. Covers item grids and non-USD currencies. | None |
| TRAIN_509 | Purchase Order | synthetic | SYNTH_PO_509 | Kept | INSIGHT: Synthesized PO layout since public PO datasets are restricted. Covers item grids and non-USD currencies. | None |
| TRAIN_510 | Purchase Order | synthetic | SYNTH_PO_510 | Kept | INSIGHT: Synthesized PO layout since public PO datasets are restricted. Covers item grids and non-USD currencies. | None |
| TRAIN_511 | Purchase Order | synthetic | SYNTH_PO_511 | Kept | INSIGHT: Synthesized PO layout since public PO datasets are restricted. Covers item grids and non-USD currencies. | None |
| TRAIN_512 | Purchase Order | synthetic | SYNTH_PO_512 | Kept | INSIGHT: Synthesized PO layout since public PO datasets are restricted. Covers item grids and non-USD currencies. | None |
| TRAIN_513 | Purchase Order | synthetic | SYNTH_PO_513 | Kept | INSIGHT: Synthesized PO layout since public PO datasets are restricted. Covers item grids and non-USD currencies. | None |
| TRAIN_514 | Purchase Order | synthetic | SYNTH_PO_514 | Kept | INSIGHT: Synthesized PO layout since public PO datasets are restricted. Covers item grids and non-USD currencies. | None |
| TRAIN_515 | Purchase Order | synthetic | SYNTH_PO_515 | Kept | INSIGHT: Synthesized PO layout since public PO datasets are restricted. Covers item grids and non-USD currencies. | None |
| TRAIN_516 | Purchase Order | synthetic | SYNTH_PO_516 | Kept | INSIGHT: Synthesized PO layout since public PO datasets are restricted. Covers item grids and non-USD currencies. | None |
| TRAIN_517 | Purchase Order | synthetic | SYNTH_PO_517 | Kept | INSIGHT: Synthesized PO layout since public PO datasets are restricted. Covers item grids and non-USD currencies. | None |
| TRAIN_518 | Purchase Order | synthetic | SYNTH_PO_518 | Kept | INSIGHT: Synthesized PO layout since public PO datasets are restricted. Covers item grids and non-USD currencies. | None |
| TRAIN_519 | Purchase Order | synthetic | SYNTH_PO_519 | Kept | INSIGHT: Synthesized PO layout since public PO datasets are restricted. Covers item grids and non-USD currencies. | None |
| TRAIN_520 | Purchase Order | synthetic | SYNTH_PO_520 | Kept | INSIGHT: Synthesized PO layout since public PO datasets are restricted. Covers item grids and non-USD currencies. | None |
| TRAIN_521 | Purchase Order | synthetic | SYNTH_PO_521 | Kept | INSIGHT: Synthesized PO layout since public PO datasets are restricted. Covers item grids and non-USD currencies. | None |
| TRAIN_522 | Purchase Order | synthetic | SYNTH_PO_522 | Kept | INSIGHT: Synthesized PO layout since public PO datasets are restricted. Covers item grids and non-USD currencies. | None |
| TRAIN_523 | Purchase Order | synthetic | SYNTH_PO_523 | Kept | INSIGHT: Synthesized PO layout since public PO datasets are restricted. Covers item grids and non-USD currencies. | None |
| TRAIN_524 | Purchase Order | synthetic | SYNTH_PO_524 | Kept | INSIGHT: Synthesized PO layout since public PO datasets are restricted. Covers item grids and non-USD currencies. | None |
| TRAIN_525 | Purchase Order | synthetic | SYNTH_PO_525 | Kept | INSIGHT: Synthesized PO layout since public PO datasets are restricted. Covers item grids and non-USD currencies. | None |
| TRAIN_526 | Purchase Order | synthetic | SYNTH_PO_526 | Kept | INSIGHT: Synthesized PO layout since public PO datasets are restricted. Covers item grids and non-USD currencies. | None |
| TRAIN_527 | Purchase Order | synthetic | SYNTH_PO_527 | Kept | INSIGHT: Synthesized PO layout since public PO datasets are restricted. Covers item grids and non-USD currencies. | None |
| TRAIN_528 | Purchase Order | synthetic | SYNTH_PO_528 | Kept | INSIGHT: Synthesized PO layout since public PO datasets are restricted. Covers item grids and non-USD currencies. | None |
| TRAIN_529 | Purchase Order | synthetic | SYNTH_PO_529 | Kept | INSIGHT: Synthesized PO layout since public PO datasets are restricted. Covers item grids and non-USD currencies. | None |
| TRAIN_530 | Purchase Order | synthetic | SYNTH_PO_530 | Kept | INSIGHT: Synthesized PO layout since public PO datasets are restricted. Covers item grids and non-USD currencies. | None |
| REJ-01 | Invoice | SROIE | SROIE_2019_001.txt | Rejected | Document lacks an invoice number entirely. The vendor only prints a cash register transaction ID. | invoice_number is a required field, cannot map receipt without transaction tracking. |
| REJ-02 | Invoice | SROIE | SROIE_2019_045.txt | Rejected | Document lacks invoice number, subtotal/tax split, and currency. Raw text only lists items and a final hand-written total. | invoice_number, currency, subtotal, and tax format validation failed. Rejecting to prevent field fabrication. |
| REJ-03 | Invoice | CORD | CORD_2020_012.json | Rejected | Receipt has corrupted OCR lines with missing totals. Sum of items (30000) does not match listed total (50000) due to partial paper tear. | Subtotal, tax, and total constraints are mathematically invalid. Rejecting due to layout ambiguity. |
| REJ-04 | Invoice | synthetic | SYNTH_INV_AMBIGUOUS | Rejected | Synthetic invoice generation candidate was missing the vendor name in its header. | vendor is a required non-empty string. Candidate rejected before export. |
| REJ-05 | Purchase Order | synthetic | SYNTH_PO_NO_ITEMS | Rejected | Synthetic PO candidate generated with an empty item list due to template logic glitch. | items is a required non-empty array. Candidate rejected during automated curation checks. |