<p align="center">
  <img src="ikon.png" alt="GPU Memory Master Logo" width="100">
</p>

# GPU Memory Master v11.0

A modern desktop application built with Python and CustomTkinter designed for analyzing GPU hardware specifications and calculating memory bandwidth, compute throughput (TFLOPS), and AI performance (TOPS).

## What's New in v11.0
- **Clean Architecture Hierarchy:** Architecture options under "Select Architecture" now exclusively display clean microarchitecture names and release periods (e.g., `Battlemage (2024+)`, `Alchemist (2022-2024)`, `GCN 1 / 2 / 3 (2012-2016)`) completely freed from GPU model series prefixes like `Arc B-Series`, `Arc A-Series`, or `HD 7000 to R9`.
- **Architecture-Based Model Filtering:** When an architecture is selected, the model search and dropdown (▼) dynamically filter to show only GPU models belonging to that specific architecture.
- **One-Click Specs Sharing (Clipboard Export):** Added a `📋 Share` button in the header that formats all current GPU specifications (Model, Architecture, Memory Bandwidth, FP32 TFLOPS, INT8 TOPS) into a clean text summary ready for Discord, Reddit, and forums with instant visual feedback (`✓ Copied!`).
- **Seamless Cloud Backward-Compatibility Bridge:** Integrated an automatic architecture normalization mapper (`ARCH_ALIASES`) ensuring 100% interoperability between online GitHub database updates and local presets.
- **Instant Keyboard Calculation (`<Enter>` Key):** Pressing `Enter` inside any parameter input across Memory Analysis, Compute Power, and AI Performance tabs immediately triggers calculation.
- **Pixel-Perfect CALCULATE Button Alignment:** Standardized vertical padding and heights across all three tabs so the action button remains perfectly locked in place without shifting during tab switches.
- **Polished Result Label Typography & Logic:** All bottom result labels share a uniform font size (`Arial 20 bold`). When a GPU preset is selected, fields populate cleanly while bottom labels remain clear until manual calculation or editing occurs, displaying exact units (`GB/s`, `Gbps`, `Bit`, `TFLOPS`, `TOPS`).
- **Modernized About Dialog:** Centered About window with application icon, clickable GitHub repository link, direct `mailto:` link with hover pointer cues, and `Esc` key dismissal.

## What's New in v10.1
- **Accurate INT8 AI TOPS:** Recalibrated AI performance calculation multipliers to match official manufacturer specifications for NVIDIA, AMD, and Intel.
- **Hardware 2:4 Structural Sparsity:** Properly accounted for hardware sparsity on supported architectures (NVIDIA Ada Lovelace, Ampere, Blackwell, and AMD RDNA 4).
- **Separated Architectures:** Split NVIDIA Ada Lovelace / Ampere and AMD RDNA 4 / RDNA 3 into distinct architectures with dedicated per-generation tensor/AI multipliers.
- **AMD Radeon RX 9000 Series (RDNA 4):** Added Radeon RX 9070 XT, RX 9070, RX 9070 GRE, RX 9060 XT, and RX 9060 to the cloud preset database.
- **Massive Workstation & Classic GPU Expansion:** Added 40+ professional, enterprise, and popular GPUs including NVIDIA RTX Pro Blackwell, RTX Ada Generation, RTX Ampere (A-Series), Quadro RTX, Titan RTX, and AMD Radeon AI Pro R9700, Radeon Pro (W7800 48GB, W6800, W6600, WX 5100), Radeon VII, Vega 64/56, and RX 6000/5000/Polaris lineups with VRAM-specific bandwidth distinctions.

<img width="542" height="692" alt="image" src="https://github.com/user-attachments/assets/f7c777be-2da2-41b6-9276-626d559f17c3" />
<img width="542" height="692" alt="image" src="https://github.com/user-attachments/assets/9e134fb0-2103-44ef-9b35-9c60b6182b93" />
<img width="542" height="692" alt="image" src="https://github.com/user-attachments/assets/64a09101-3014-43fe-b2f0-947380c5d439" />

## Features

- **Cloud Preset Database:** Dynamically retrieves up-to-date specifications for modern GPUs directly from GitHub on launch.
- **Live Autocomplete Search:** Type any model number (such as `5090`, `4080`, or `7900`) to instantly filter and auto-fill hardware parameters.
- **Memory Analysis:** Automatically calculates bandwidth (GB/s), effective speed (Gbps), and memory bus width (Bit).
- **Compute Power:** Computes FP32 TFLOPS based on architecture multipliers, shading units, and boost clock frequencies.
- **AI Performance:** Calculates INT8 AI TOPS (including hardware 2:4 Structural Sparsity on supported architectures) for modern GPUs (Blackwell, Ada Lovelace, Ampere, Turing, RDNA 4, RDNA 3, Intel Battlemage/Alchemist).
- **Interactive & Editable:** All pre-filled fields remain fully editable for custom overclocking and simulation scenarios.

## Supported Architectures

- **NVIDIA:** Blackwell, Ada Lovelace, Ampere, Turing, Pascal, Maxwell
- **AMD:** RDNA 4, RDNA 3, RDNA 1 / 2, GCN 4 / 5 (Polaris/Vega), GCN 1 / 2 / 3
- **Intel:** Battlemage, Alchemist

## Requirements

- Python 3.10 or higher
- `customtkinter` 5.2.0 or higher

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/pantegra17/GPU-Memory-Master.git
   cd GPU-Memory-Master
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## Author

- **Developer:** Gökhan Can
- **Contact:** pantegra@gmail.com
- **GitHub:** [@pantegra17](https://github.com/pantegra17)

## License

This project is open source and available under the MIT License.
