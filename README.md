<p align="center">
  <img src="ikon.png" alt="GPU Memory Master Logo" width="100">
</p>

# GPU Memory Master v11.0

A modern desktop application built with Python and CustomTkinter designed for analyzing GPU hardware specifications and calculating memory bandwidth, compute throughput (TFLOPS), and AI performance (TOPS).

<img width="542" height="692" alt="image" src="https://github.com/user-attachments/assets/f7c777be-2da2-41b6-9276-626d559f17c3" />
<img width="542" height="692" alt="image" src="https://github.com/user-attachments/assets/9e134fb0-2103-44ef-9b35-9c60b6182b93" />
<img width="542" height="692" alt="image" src="https://github.com/user-attachments/assets/64a09101-3014-43fe-b2f0-947380c5d439" />

## Features

- **Cloud Preset Database:** Dynamically retrieves up-to-date specifications for modern GPUs directly from GitHub on launch.
- **Live Autocomplete Search:** Type any model number (such as `5090`, `4080`, or `7900`) to instantly filter and auto-fill hardware parameters.
- **Architecture-Based Filtering:** Filter GPU models directly by microarchitecture.
- **Memory Analysis:** Automatically calculates bandwidth (GB/s), effective speed (Gbps), and memory bus width (Bit).
- **Compute Power:** Computes FP32 TFLOPS based on architecture multipliers, shading units, and boost clock frequencies.
- **AI Performance:** Calculates INT8 AI TOPS (including hardware 2:4 Structural Sparsity on supported architectures) for modern GPUs (Blackwell, Ada Lovelace, Ampere, Turing, RDNA 4, RDNA 3, Intel Battlemage/Alchemist).
- **One-Click Share:** Export complete hardware specifications to clipboard for benchmarks and discussions.
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
