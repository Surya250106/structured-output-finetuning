# Training Configuration & LlamaFactory Instructions

This document outlines the fine-tuning setup, LoRA hyperparameters, dataset registration, and reproduction instructions for training Llama 3.2 3B Instruct on structured output extraction.

---

## 1. Setup Instructions

To perform the fine-tuning, you must install LlamaFactory on an environment with GPU acceleration (CUDA-enabled).

### A. Environment Preparation
1. Create a Python virtual environment and activate it:
   ```bash
   python -m venv venv
   venv\Scripts\activate     # On Windows
   source venv/bin/activate  # On Linux/macOS
   ```
2. Install LlamaFactory from source:
   ```bash
   git clone https://github.com/hiyouga/LLaMA-Factory.git
   cd LLaMA-Factory
   pip install -e ".[torch,metrics]"
   ```

### B. Registering the Dataset
To register our curated training dataset in LlamaFactory:
1. Copy `data/curated_train.jsonl` from this project to the `LLaMA-Factory/data/` folder.
2. Edit `LLaMA-Factory/data/dataset_info.json` and append this configuration entry:
   ```json
   "curated_train": {
     "file_name": "curated_train.jsonl",
     "columns": {
       "prompt": "instruction",
       "query": "input",
       "response": "output"
     }
   }
   ```

---

## 2. LoRA Hyperparameter Configuration

We recommend the following hyperparameters for training Llama 3.2 3B Instruct:

| Hyperparameter | Value | Rationale |
| :--- | :--- | :--- |
| **Model** | `Llama-3.2-3B-Instruct` | Target model for compact structured parsing. |
| **Method** | `LoRA` (Low-Rank Adaptation) | Parametric efficiency; prevents full-weight collapse and avoids forgetting general capabilities. |
| **LoRA Rank ($r$)** | `16` | Standard starting rank; captures task-specific structure without high compute overhead. |
| **LoRA Alpha ($\\alpha$)** | `32` | Scaling coefficient set to $2 \\times r$ for optimization stability. |
| **LoRA Target Modules** | `all` | Targets all linear projection layers (e.g. `q_proj`, `v_proj`, `k_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`) to maximize adapter capacity. |
| **Learning Rate** | `2e-4` | Standard LR for stable LoRA convergence. |
| **Epochs** | `3` | 3 full passes over the 80 examples is sufficient for the model to align to schema output keys. |
| **Batch Size** | *Hardware Dependent* | Scale to the maximum that fits in your GPU's VRAM. |
| **Gradient Accumulation** | *Adjustable* | Adjust alongside Batch Size to target an **effective batch size of 16** (e.g. `per_device_batch_size = 2` and `gradient_accumulation_steps = 8`). |
| **Optimizer** | `adamw_torch` | Decoupled weight decay optimizer for standard LLM tuning. |
| **LR Scheduler** | `cosine` | Decays learning rate smoothly as training progresses. |
| **Warmup Ratio** | `0.1` | 10% of total steps spent warming up the learning rate to prevent early gradient spikes. |

### Overfitting Risk Analysis
Because the dataset is small (exactly 80 examples), there is a moderate risk that the model will overfit to the specific values or formats (e.g., memorizing the specific vendor names or item totals). 
To mitigate this risk:
- We keep the LoRA Rank low ($r=16$) and use a Cosine learning rate scheduler.
- The training dataset is designed with extreme layout diversity (Markdown, OCR, key-value, memos) and varying labels so that the adapter learns the extraction structure rather than memorizing a single text template.

---

## 3. Launching and Monitoring

### A. Launch LlamaFactory WebUI
To run via a graphical browser dashboard, launch the WebUI from your virtual environment inside the `LLaMA-Factory` folder:
```bash
llamafactory-cli webui
```

### B. Launch via Command Line (CLI)
Alternatively, you can write the config to a YAML file (e.g. `train_lora.yaml`) and run it:
```bash
llamafactory-cli train train_lora.yaml
```

Example YAML config:
```yaml
### model
model_name_or_path: meta-llama/Llama-3.2-3B-Instruct

### method
stage: sft
do_train: true
finetuning_type: lora
lora_target: all
lora_rank: 16
lora_alpha: 32

### dataset
dataset: curated_train
template: llama3
cutoff_len: 2048
overwrite_cache: true
preprocessing_num_workers: 16

### output
output_dir: saves/Llama-3.2-3B/lora/sft
logging_steps: 10
save_steps: 100
plot_loss: true

### train
per_device_train_batch_size: 2
gradient_accumulation_steps: 8
learning_rate: 0.0002
num_train_epochs: 3.0
lr_scheduler_type: cosine
warmup_ratio: 0.1
fp16: true
```

---

## 4. Screenshot Capture Workflows (MANUAL ACTION REQUIRED)

To satisfy final repository criteria, you must capture two screenshots from your LlamaFactory execution and place them in the `screenshots/` directory:

### Screenshot 1: Training Configuration
- **File Path**: `screenshots/training_config.png`
- **When to Capture**: Just before launching the training run in LlamaFactory.
- **Workflow**:
  1. Open the WebUI in your browser (`http://localhost:7860`).
  2. Select the Model `Llama-3.2-3B-Instruct` and set the Fine-tuning method to `lora`.
  3. Load the dataset `curated_train`.
  4. Ensure learning rate, epochs, rank, and alpha are set to the documented values.
  5. Take a screenshot of the entire WebUI setup page, ensuring all parameters are visible.
  6. Save the PNG exactly as: `screenshots/training_config.png`.

### Screenshot 2: Loss Curve Chart
- **File Path**: `screenshots/loss_curve.png`
- **When to Capture**: Once training is fully completed.
- **Workflow**:
  1. Once training finishes, LlamaFactory generates a `training_loss.png` chart in the output folder (`saves/Llama-3.2-3B/lora/sft`).
  2. Copy that generated loss curve image.
  3. Save the image exactly as: `screenshots/loss_curve.png`.
