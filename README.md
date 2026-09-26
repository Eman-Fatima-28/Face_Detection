# Module 5: Image Generation — Stable Diffusion + ControlNet

## AI Room Scan & Interior Styling System

A CPU-compatible image generation module for redesigning room images while preserving the original room structure using Stable Diffusion and ControlNet.

**Author:** Eman Fatima

---

## 📌 Overview

Module 5 is the image generation stage of the AI Room Scan & Interior Styling System.

The module takes a processed room image together with structural information such as:

- Original/processed room frame
- Depth map
- Segmentation masks
- Interior-design prompt

It then generates a redesigned version of the room using Stable Diffusion with ControlNet-based structural guidance.

The module provides two workflows:

1. **Dummy Workflow** — Fast testing without running a diffusion model
2. **Real Workflow** — Actual AI-based room redesign using Stable Diffusion + ControlNet

The dummy workflow allows the complete project pipeline to be tested without waiting for CPU-based diffusion generation.

---

## 🎯 Module Objective

The objective of Module 5 is to transform an existing room image into a redesigned interior while attempting to preserve:

- Room geometry
- Furniture placement
- Major structural elements
- Overall scene layout

The generation process uses textual design instructions together with structural conditioning.

### Basic Pipeline

```text
Processed Room Frame
        +
    Depth Map
        +
 Segmentation Masks
        +
     Text Prompt
        │
        ▼
┌───────────────────────┐
│   Module 5 Entry      │
│   Image Generation    │
└───────────┬───────────┘
            │
       ┌────┴────┐
       ▼         ▼
    Dummy      Real
    Mode       Mode
       │         │
       ▼         ▼
 Copy +       Stable
 Overlay      Diffusion
       │         │
       │      ControlNet
       │         │
       └────┬────┘
            ▼
     Redesigned Image
            │
            ▼
      data/generated/
```

---

## ✨ Key Features

### 1. Dummy Generation Mode

The dummy workflow is designed for:

- Pipeline testing
- Integration testing
- Development
- Demonstrations
- Testing downstream modules

Instead of running Stable Diffusion, the workflow copies the input image and adds a visual label indicating that the selected style was applied.

**Example**

```text
Input Room
    ↓
Copy Image
    ↓
Add "Modern Style Applied"
    ↓
Save Generated Image
```

This makes it possible for the rest of the project to be developed without waiting for CPU-based diffusion generation.

### 2. Real AI Generation Mode

The real workflow uses:

- Stable Diffusion
- ControlNet
- Depth conditioning
- Segmentation conditioning
- Text prompts

The intended process is:

```text
Input Image
    +
Depth Map
    +
Segmentation
    +
Design Prompt
        ↓
Stable Diffusion + ControlNet
        ↓
Redesigned Room Image
```

### 3. Structural Guidance

ControlNet is used to provide additional structural information to the generation process.

**Depth Guidance**

The depth map provides information about the approximate spatial structure of the room.

```text
Room Image
     ↓
 Depth Map
     ↓
ControlNet
     ↓
Stable Diffusion
```

**Segmentation Guidance**

Segmentation masks provide information about detected objects and regions.

For example:

```text
Sofa Mask
Table Mask
Chair Mask
Bed Mask
Window Mask
Door Mask
```

These masks can be used as additional structural information during generation.

---

## 🏗️ System Architecture

### High-Level Architecture

```text
             Previous Modules
                    │
                    ▼
        ┌─────────────────────┐
        │ Processed Room      │
        │ Frames              │
        └──────────┬──────────┘
                   │
                   ├───────────────┐
                   │               │
                   ▼               ▼
              Depth Maps      Segmentation
                                Masks
                   │               │
                   └───────┬───────┘
                           │
                           ▼
                     Module 5
                 Image Generation
                           │
                  ┌────────┴────────┐
                  │                 │
                  ▼                 ▼
             Dummy Mode        Real Mode
                  │                 │
                  │          Stable Diffusion
                  │                 +
                  │             ControlNet
                  │                 │
                  └────────┬────────┘
                           ▼
                  Redesigned Images
                           │
                           ▼
                    data/generated/
```

---

## 📂 Project Structure

```text
image_generation/
│
├── main.py
├── dummy.py
├── run.py
├── utils.py
├── __init__.py
├── module5_config.yaml
├── requirements.txt
├── README.md
│
├── data/
│   ├── processed_frames/
│   ├── depth_maps/
│   ├── masks/
│   ├── prompts/
│   ├── generated/
│   └── temp/
│
└── logs/
    └── module5/
```

### File Responsibilities

| File | Purpose |
|---|---|
| `main.py` | Main entry point and workflow orchestration |
| `dummy.py` | Dummy image-generation workflow |
| `run.py` | Real Stable Diffusion + ControlNet workflow |
| `utils.py` | Shared helper functions |
| `__init__.py` | Python package initialization |
| `module5_config.yaml` | Module configuration |
| `requirements.txt` | Python dependencies |
| `README.md` | Module documentation |

---

## 📥 Input Specification

Module 5 expects processed data from the previous stages of the system.

### 1. Processed Room Frames

Directory:

```text
data/processed_frames/
```

Supported formats:

```text
PNG
JPG/JPEG
```

Expected naming:

```text
frame_001.png
frame_002.png
frame_003.png
```

The images should be resized/preprocessed according to the project's configured generation resolution.

### 2. Depth Maps

Directory:

```text
data/depth_maps/
```

Format:

```text
PNG/JPG
```

Expected naming:

```text
frame_001_depth.png
frame_002_depth.png
```

Depth maps are generated by the depth-estimation stage of the overall project.

### 3. Segmentation Masks

Directory:

```text
data/masks/
```

Example:

```text
frame_001_sofa.png
frame_001_table.png
frame_001_chair.png
frame_001_bed.png
```

The masks represent objects detected and segmented by earlier pipeline stages.

### 4. Design Prompts

Directory:

```text
data/prompts/
```

Example:

```text
frame_001.txt
```

Example content:

```text
Design this room in a modern minimalist style with neutral colors,
natural lighting, clean furniture, and a spacious appearance.
```

---

## 📤 Output Specification

Generated images are saved in:

```text
data/generated/
```

Example:

```text
data/generated/
├── frame_001.png
├── frame_002.png
├── frame_003.png
```

The output represents the redesigned version of the corresponding input frame.

---

## 🎨 Styling Modes

The complete AI Room Scan & Interior Styling System supports three styling modes.

### Mode 1 — Generic Style

The user selects a predefined style.

Examples:

```text
Modern
Minimal
Luxury
```

A predefined prompt is then passed to the image-generation module.

Example:

```text
Redesign this room in a modern interior style.
```

### Mode 2 — Prompt-Based Style

The user provides a custom design description.

Example:

```text
Design this room in a modern minimalist style with
neutral colors, warm lighting, wooden furniture,
and clean lines.
```

The user-provided prompt is passed to the generation pipeline.

### Mode 3 — AI Auto-Design

In this mode, the user does not provide a design style.

The system can analyze information obtained from the room-processing stages, such as:

- Room appearance
- Brightness
- Approximate room size
- Detected furniture
- Existing scene characteristics

The system then generates an internal design prompt.

Example:

```text
Design a clean, well-lit modern living room with
neutral tones, simple furniture, and an uncluttered layout.
```

That generated prompt is then used by Module 5.

---

## 🤖 Real Generation Pipeline

The real workflow follows these steps:

**Step 1 — Load Input**

```text
Original Frame
Depth Map
Segmentation Information
Design Prompt
```

**Step 2 — Load Stable Diffusion**

The configured Stable Diffusion model is loaded using Hugging Face Diffusers.

**Step 3 — Load ControlNet**

ControlNet provides structural conditioning for the generation process.

Possible conditioning sources include:

```text
Depth
Segmentation
```

**Step 4 — Prepare Conditioning**

The input depth map and segmentation information are prepared for the generation pipeline.

**Step 5 — Generate Image**

Stable Diffusion generates a redesigned room according to the supplied prompt and structural conditions.

**Step 6 — Save Output**

The generated image is saved in:

```text
data/generated/
```

---

## 🧪 Dummy Workflow

The dummy workflow is intentionally simple.

### Process

```text
Read Input Frame
       ↓
Read Prompt
       ↓
Copy Original Image
       ↓
Add "Style Applied" Label
       ↓
Save Output
```

This workflow does not run Stable Diffusion.

It is useful for verifying that:

- Input files are correctly located
- Prompts are correctly loaded
- Output directories work
- Frame processing works
- The complete pipeline can run before enabling expensive AI generation

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Eman-Fatima-28/YOUR-REPOSITORY.git
cd YOUR-REPOSITORY
```

Replace `YOUR-REPOSITORY` with the actual GitHub repository name.

### 2. Create a Virtual Environment

**Windows**

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

**Linux / WSL**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If your environment requires it, install packages using the appropriate Python environment/package configuration.

---

## 📦 Model Requirements

The real workflow requires compatible Stable Diffusion and ControlNet models.

The project is designed around open-source models available through Hugging Face Diffusers.

Typical components include:

```text
Stable Diffusion v1.5
        +
ControlNet Depth
        +
ControlNet Segmentation
```

Models can require several gigabytes of storage.

The first model load/download may therefore take significantly longer than subsequent runs.

> **Important:** Do not commit downloaded model weights (`.safetensors`, `.ckpt`, `.bin`, etc.) to GitHub. They should be downloaded separately or managed through the model-loading mechanism.

---

## 🚀 Usage

### Dummy Mode

For fast testing:

```bash
python main.py --mode dummy
```

This does not perform actual diffusion generation.

### Real Mode

For actual AI image generation:

```bash
python main.py --mode real
```

CPU inference can be considerably slower than GPU inference.

### Custom Configuration

```bash
python main.py --config custom_config.yaml --mode dummy
```

For real generation:

```bash
python main.py --config custom_config.yaml --mode real
```

---

## 🐍 Python Usage

The module can also be used from Python.

### Dummy Workflow

```python
from dummy import DummyGenerator

generator = DummyGenerator("module5_config.yaml")

results = generator.run()

if results["status"] == "success":
    print(f"Processed: {results['processed']}")
    print(f"Outputs: {results['outputs']}")
```

### Real Workflow

```python
from run import RealGenerator

generator = RealGenerator("module5_config.yaml")

results = generator.run()

if results["status"] == "success":
    print(f"Processed: {results['processed']}")
    print(f"Outputs: {results['outputs']}")
```

---

## 💻 CPU Compatibility

This module is designed to support CPU-based execution.

However, diffusion models are computationally expensive, so CPU generation is expected to be significantly slower than GPU generation.

The module can use optimization techniques such as:

- Attention slicing
- VAE slicing
- Reduced inference steps
- Lower generation resolution when appropriate
- Processing frames sequentially

Actual execution time depends on:

- CPU model
- Available RAM
- Image resolution
- Number of inference steps
- ControlNet configuration
- Number of frames
- Diffusion model

Therefore, performance values should be treated as machine-dependent rather than fixed guarantees.

---

## ⚡ Performance Considerations

For CPU testing, a lower number of inference steps can be used.

Example:

```yaml
generation:
  num_inference_steps: 15
```

Increasing the number of steps may improve generation quality but generally increases processing time.

For multi-frame room videos, processing frames sequentially is recommended on CPU to avoid excessive memory consumption.

---

## 📝 Logging

Execution logs are stored under:

```text
logs/module5/
```

Example:

```text
logs/module5/
├── module5_YYYYMMDD_HHMMSS.log
└── performance_report_YYYYMMDD_HHMMSS.json
```

Logs can be used to investigate:

- Input errors
- Missing files
- Model-loading problems
- Generation failures
- Processing time
- Frame-level errors

---

## 🐛 Debug Outputs

Optional debugging information can be stored under:

```text
data/temp/module5/debug/
```

Possible debugging outputs include:

```text
frame_001_conditioning_0.png
frame_001_conditioning_1.png
frame_001_comparison.png
```

These files can help verify that the correct conditioning information is being passed to the generation pipeline.

---

## 🔒 Git & Large Files

The repository should not contain large generated or model files.

Recommended `.gitignore` entries include:

```gitignore
# Python
__pycache__/
*.py[cod]

# Virtual environment
venv/
.venv/

# Model files
*.ckpt
*.safetensors
*.bin
*.pt
*.pth

# Generated outputs
data/generated/*
data/temp/*
logs/*

# Local configuration
.env

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

If sample outputs are required for demonstration, keep only a small number of intentionally selected sample files.

---

## 🔗 Position in the Complete Project

Module 5 is part of the larger:

**AI Room Scan & Interior Styling System**

The complete pipeline is:

```text
Room Image / Video
        ↓
Input Processing
        ↓
Depth Estimation
        ↓
Object Detection
        ↓
Object Segmentation
        ↓
Scene Understanding
        ↓
Prompt Generation
        ↓
┌──────────────────────────────┐
│ Module 5: Image Generation   │
│ Stable Diffusion + ControlNet│
└──────────────┬───────────────┘
               ↓
        Redesigned Images
               ↓
        Video Generation
```

Module 5 therefore acts as the AI visual redesign component of the complete system.

---

## 🧰 Technology Stack

| Component | Technology |
|---|---|
| Language | Python |
| Image Processing | Pillow, NumPy |
| Diffusion Framework | Hugging Face Diffusers |
| Deep Learning | PyTorch |
| Image Generation | Stable Diffusion |
| Structural Guidance | ControlNet |
| Conditioning | Depth / Segmentation |
| Hardware Target | CPU |

---

## 📋 Module Deliverables

This module provides:

- Python source code
- Dummy generation workflow
- Real Stable Diffusion workflow
- ControlNet integration
- Configuration file
- Requirements file
- Input/output structure
- Logging and debugging support
- Documentation

---

## ⚠️ Limitations

CPU-based Stable Diffusion is computationally expensive and can be slow.

The generated image may not perfectly preserve every object or detail from the original room because diffusion-based generation is probabilistic.

Depth and segmentation conditioning help provide structural guidance, but they do not guarantee exact pixel-level preservation.

The quality of the final result depends on:

- Input image quality
- Depth estimation quality
- Segmentation quality
- Prompt quality
- Model configuration
- ControlNet conditioning
- Available computational resources

---

## 👩‍💻 Author

**Eman Fatima**

BS Artificial Intelligence
COMSATS University Islamabad

---

## 📄 License

This project is intended for educational and research purposes.

Individual pretrained models used by this project may have their own licenses and usage restrictions. Refer to the respective model repositories for their licensing terms.