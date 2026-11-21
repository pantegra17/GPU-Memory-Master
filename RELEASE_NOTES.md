# GPU Memory Master v11.0 Release

Welcome to **GPU Memory Master v11.0**! This major milestone release brings significant architectural refinements, dynamic hardware filtering, productivity enhancements, critical calculation fixes, and a modernized user interface.

---

### 🏛️ Clean Microarchitecture Naming & Hierarchy
* **Model-Agnostic Architecture Dropdown:** Stripped all consumer GPU model prefixes and series identifiers from the **Select Architecture** menu across all manufacturers.
* **Intel Refinement:**
  * Cleaned `Arc B-Series (Battlemage) (2024+)` → **`Battlemage (2024+)`**.
  * Cleaned `Arc A-Series (Alchemist) (2022-2024)` → **`Alchemist (2022-2024)`**.
* **AMD Refinement:**
  * Cleaned `GCN 1 / 2 / 3 (HD 7000 to R9) (2012-2016)` → **`GCN 1 / 2 / 3 (2012-2016)`** (removed `HD 7000 to R9` model range).
  * Preserved official architectural codenames for **`GCN 4 / 5 (Polaris/Vega) (2016-2019)`**.
  * Maintained distinct per-generation AI/tensor specifications for **`RDNA 4 (2025+)`**, **`RDNA 3 (2022-2024)`**, and **`RDNA 1 / 2 (2019-2022)`**.
* **NVIDIA Lineup:**
  * Verified complete microarchitecture hierarchy: **`Blackwell (2024-2026)`**, **`Ada Lovelace (2022-2024)`**, **`Ampere (2020-2022)`**, **`Turing (2018-2020)`**, **`Pascal (2016-2018)`**, and **`Maxwell (2014-2016)`**.

---

### 🔍 Dynamic Architecture-Based Model Filtering
* **Instant Model Pruning:** Selecting a specific architecture in the dropdown now automatically filters both the model search autocomplete and the dropdown popup (**▼**).
* **Targeted Selection:** When *Battlemage* is selected, only B-Series cards (e.g., Arc B580, Arc B570) are shown; selecting *RDNA 4* shows only RX 9000-series models.
* **Seamless Reset:** Leaving the architecture on *Select Architecture...* or switching brands displays the complete database for that brand.
* **Two-Way Synchronization:** Selecting a GPU model from the list automatically sets and locks its corresponding architecture.

---

### 📋 One-Click Hardware Specs Sharing (`[📋 Share]`)
* **Dedicated Header Action:** Added a sleek **`[📋 Share]`** button in the top navigation bar next to the About button.
* **Formatted Summary Export:** Instantly compiles the selected GPU's entire hardware profile into a beautifully formatted text snippet:
  * Brand and Model Name
  * Microarchitecture
  * Memory Bus Width, Effective Clock Speed, and Theoretical Bandwidth
  * Shading Units (CUDA / Stream Processors / ALUs), Boost Clock, and FP32 Compute Power (TFLOPS)
  * INT8 AI TOPS (accounting for hardware 2:4 Structural Sparsity)
  * Repository Attribution
* **Interactive Visual Feedback:** The button temporarily turns green with a **`✓ Copied!`** state for 1.5 seconds upon successful clipboard copy.

---

### ⚡ Instant Keyboard Calculation (`<Enter>` Key Support)
* **Productivity Workflow:** Users can now trigger immediate calculations simply by pressing `Enter` (`<Return>`) inside any text box:
  * **Memory Analysis Tab:** Memory Bus, Effective Speed, Bandwidth
  * **Compute Power Tab:** Shading Units, Boost Clock, Compute Power
  * **AI Performance Tab:** AI Core Count, Boost Clock, AI Performance
* Eliminates the need to switch between keyboard and mouse during rapid overclocking, hardware exploration, or custom benchmarking.

---

### 🛠️ Critical Calculation & UI/UX Bugfixes
* **Memory Bandwidth Result Label Fix:** Fixed an issue in `calc_memory()` where the result label was hardcoded to display `Result: {speed} Gbps`. It now dynamically and accurately reflects whichever metric was computed with the proper unit (`GB/s`, `Gbps`, or `Bit`).
* **Clean Preset Loading:** When an existing GPU model preset is loaded, all calculated parameter entries (Bandwidth, TFLOPS, TOPS) populate immediately, but **the bottom result summary labels remain completely empty (`""`)** to keep the workspace clean and distraction-free.
* **Manual Intervention Indicator:** Bottom result labels only display when the user explicitly triggers a calculation via the `CALCULATE` button or by pressing `Enter`.
* **Standardized Typography:** Unified the font size for all bottom summary labels across all three tabs to `Arial 20 bold` (resolving previous size discrepancies between 16pt and 22pt).
* **Pixel-Perfect Button Placement:** Aligned the vertical margins (`pady=14, padx=15`) of the `CALCULATE` button across all tabs, eliminating any vertical jump or shift when toggling between Memory, Compute, and AI tabs.

---

### 🌐 Cloud & Offline Database Compatibility Bridge
* **`ARCH_ALIASES` Normalization Engine:** Integrated an automatic translation dictionary into `_normalize_database()`.
* **Zero Disruption:** Ensures 100% interoperability between online GitHub database pulls (`gpus.json`) and local presets, automatically mapping legacy names on-the-fly without throwing errors or unlinking architectures.
* **Synchronized Local Database:** Updated all 112 GPU configurations in `gpus.json` to the new architecture hierarchy.

---

### ℹ️ Modernized About Dialog
* **Interactive Hyperlinks:** Integrated standard web and email protocols using Python's `webbrowser` module:
  * `🌐 GitHub Repository` button opens the project repository directly in the system's default browser.
  * `✉️ pantegra@gmail.com` button opens the system's default mail client with `mailto:`.
  * Buttons feature hover states and pointer (`hand2`) cursors.
* **Window Polish:**
  * The dialog is now centered relative to the main application window.
  * The application icon (`ikon.ico`) is explicitly attached to the dialog to prevent generic Tkinter feather icons.
  * Added `<Escape>` key binding to instantly close the dialog.

---

### 📦 Updated Files:
* `main.py` — Core application logic, UI enhancements, event bindings, and v11.0 metadata.
* `gpus.json` — Database of 112 GPUs synchronized to clean architecture specifications.
* `README.md` — Cleaned and streamlined documentation focusing on core features and setup.
* `.github/workflows/release.yml` — Automated CI/CD release workflow enhanced to publish full release notes.
