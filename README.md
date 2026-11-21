<p align="center">
  <img src="ikon.png" alt="GPU Memory Master Logo" width="100">
</p>

# GPU Memory Master v10.1

A modern desktop application built with Python and CustomTkinter designed for analyzing GPU hardware specifications and calculating memory bandwidth, compute throughput (TFLOPS), and AI performance (TOPS).

## What's New in v10.1
- **Accurate INT8 AI TOPS:** Recalibrated AI performance calculation multipliers to match official manufacturer specifications for NVIDIA, AMD, and Intel.
- **Hardware 2:4 Structural Sparsity:** Properly accounted for hardware sparsity on supported architectures (NVIDIA Ada Lovelace, Ampere, Blackwell, and AMD RDNA 4).
- **Separated Architectures:** Split NVIDIA Ada Lovelace / Ampere and AMD RDNA 4 / RDNA 3 into distinct architectures with dedicated per-generation tensor/AI multipliers.
- **AMD Radeon RX 9000 Series (RDNA 4):** Added Radeon RX 9070 XT, RX 9070, RX 9070 GRE, RX 9060 XT, and RX 9060 to the cloud preset database.
- **Massive Workstation & Classic GPU Expansion:** Added 40+ professional, enterprise, and popular GPUs including NVIDIA RTX Pro Blackwell, RTX Ada Generation, RTX Ampere (A-Series), Quadro RTX, Titan RTX, and AMD Radeon AI Pro R9700, Radeon Pro (W7800 48GB, W6800, W6600, WX 5100), Radeon VII, Vega 64/56, and RX 6000/5000/Polaris lineups with VRAM-specific bandwidth distinctions (e.g., RX 580 8GB vs 4GB).
- **Full NVIDIA GeForce RTX 50-Series Lineup:** Added GeForce RTX 5070 Ti, RTX 5070, RTX 5060 Ti, RTX 5060, and RTX 5050 presets with reference Blackwell GDDR7 specifications, and aligned RTX 5080 boost clock to reference 2617 MHz.
- **Expanded Intel & NVIDIA Presets:** Added GeForce RTX 3080 12GB, RTX 3050 8GB/6GB, full Turing lineup (RTX 2080, 2070, 2060 12GB, 2060), and Intel Arc A310 alongside retail partner clock adjustments for Arc A580 and A380.
- **Unified Core Architecture:** Standardized input and calculations across all brands for seamless benchmarking and overclocking.

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
- **AMD:** RDNA 4, RDNA 3, RDNA 1 / 2, GCN 1-5
- **Intel:** Arc Battlemage (B-Series), Arc Alchemist (A-Series)

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
