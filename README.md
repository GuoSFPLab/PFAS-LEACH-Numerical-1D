# PFAS-LEACH-Numerical-1D (Tier 2: A Numerical 1D Model)

This repository contains **PFAS-LEACH-Numerical-1D**, a one-dimensional (vertical) numerical model for simulating coupled water flow and PFAS fate and transport in the subsurface. It is designed for **scenario evaluation** where 1D leaching is an appropriate approximation.

PFAS-LEACH is a tiered decision support platform for predicting PFAS leaching in source zones. PFAS-LEACH-Numerical-1D corresponds to a **Tier 2-style 1D model**, and complements other tiers/models (e.g., analytical or dilution-factor screening tools (Tier 3 and Tier 4), and more comprehensive multidimensional models (Tier 1)).

## Features (Numerical-1D)

- **1D variably saturated flow** in the vertical direction.
  - Hetergeneous subsurface (layered).
  - Surfactant-induced flow.
- **PFAS transport** with advection and dispersion.
- **Retention processes** represented through:
  - solid-phase adsorption (including kinetic sites if enabled),
  - air-water interfacial adsorption (including kinetic sites if enabled),
  - optional first-order decay (if enabled in inputs).
- **Optional modules**
  - root-water uptake / evapotranspiration,
  - groundwater dilution-factor.
- **Outputs**
  - time series of key variables and mass balance terms,
  - profile snapshots of state variables versus depth,
  - observation-style outputs for selected cells.

## Getting Started

This package is publicized on GitHub. You can obtain it either by cloning the repository or by downloading a ZIP archive.

### Option A: Clone the repository (recommended)

1. Install Git (if you do not already have it):
   - Windows: install Git for Windows.
2. Open a terminal (Git Bash or PowerShell on Windows).
3. Choose a local folder where you want to store the model package and navigate there, e.g.:
   - `cd D:\Models`
4. On the GitHub repository page, click **Code** and copy the HTTPS clone URL.
5. Clone the repository:
   - `git clone <HTTPS-CLONE-URL>`
6. Enter the downloaded folder:
   - `cd <repo-folder>`

### Option B: Download as a ZIP file

1. Open the GitHub repository page in a web browser.
2. Click the green **Code** button.
3. Click **Download ZIP**.
4. Extract the ZIP file to a local folder (avoid OneDrive/online-synced folders if you encounter permission or path issues).
5. Open the extracted folder. This is your local model package.

## Repository Layout (Expected)

The model executable is expected at:

- `bin/ESTCP-PFAS-LEACH-Tier-2.exe`

A typical **case folder** is created **parallel to** `bin/`, for example:

- `MyCase/`
  - `INPUT/`
  - `OUTPUT/` (written by the executable)
  - `FIGURES/` (written by `plot_outputs.py`)
  - `Run.bat` (user double-clicks to run the model)
  - `plot_outputs.py` (user runs to visualize results)

Three example cases are provided in `Exp1/`,  `Exp2/`, and  `Exp3/` (including example inputs/outputs).

## Quick Start (Recommended Workflow)

1. **Create a case folder** (parallel to `bin/`), e.g., `MyCase/`.
2. **Copy subfolders and files into the case folder**:
   - Copy `Exp3/Run.bat` to `MyCase/Run.bat`.
   - Copy `Exp3/INPUT/` to `MyCase/INPUT/`.
   - Copy `Exp3/OUTPUT/` to `MyCase/OUTPUT/`.
   - Copy `Exp3/plot_outputs.py` to `MyCase/plot_outputs.py`.
3. **Edit inputs** by editing the CSV files in `MyCase/INPUT/`.
4. **Run the model**:
   - Double-click `MyCase/Run.bat`
   - This runs `..\bin\ESTCP-PFAS-LEACH-Tier-2.exe` with the case folder as the working directory.
6. **Plot results**:
   - Run `plot_outputs.py`,
   - This generates PDF figures in `MyCase/FIGURES/`.

## Input Files (csv files in INPUT/)

PFAS-LEACH-Numerical-1D reads a set of CSV files from `INPUT/`. A typical case includes:

- `System_ctrl.csv` (global switches + solver/time-step settings)
- `Soil_profile.csv` (grid + soil hydraulic + transport + initial conditions)
- `PFAS_properties.csv` (compound/adsorption/interface parameters)
- `Boundary_conditions.csv` (time series for fluxes/ water pressure heads and PFAS loading at the land surface)
- `Output_ctrl.csv` (what/where/when to output)
- Optional, depending on switches in `System_ctrl.csv`:
  - `Root_uptake.csv`
  - `Groundwater_pollution.csv`

## Output Files (Written to OUTPUT/)

Common outputs include:

- `1.Profile-Time-*.csv` (profiles versus depth at requested times)
- `2.Time series.csv` (domain-integrated and boundary time series)
- `3.Observations.csv` (high-frequency output at selected cells)
- `4.Summary.csv` (run summary including CPU time and groundwater pollution metrics if enabled)

## Visualization

The provided plotting script (`plot_outputs.py`) reads the model outputs and writes PDFs to `FIGURES/`.

Python dependencies:
- `pandas`
- `matplotlib`

If needed, install dependencies (example):
- `pip install pandas matplotlib`

## Version Histroy

- **Beta version** - Initial Release for testing
  - Jan 13, 2026: Data visualization using a Python script.
  - Jan 31, 2026: Computational cost optimized.


## Acknowledgements

The PFAS-LEACH Tier 2 model (PFAS-LEACH-Numerical-1D) was developed from scratch at the University of Arizona by Jicai Zeng and Bo Guo. The development of this model was supported by the Environmental Security Technology Certification Program (ESTCP) under Project ER21-5041.

We thank Dr. Mark L. Brusseau for helpful discussions related to the parameterization of the model as well as model validation by unsaturated miscible-displacement experiments. We also acknowledge constructive feedback from the community during the course of model development. The views, opinions, and findings expressed in this document are those of the authors and do not necessarily reflect the official policies or positions of the U.S. Department of Defense or other sponsoring agencies.

## How to cite

The Tier 2 PFAS-LEACH-Numerical-1D model was developed based on the modeling framework and numerical approaches described in Guo et al. (2020) and Zeng et al. (2021). If you use the Tier 2 model, please cite the following respective references.

- Zeng, J., & Guo, B., 2026. User's Guide: the ESTCP-PFAS-LEACH Tier 2 Model (PFAS-LEACH-Numerical-1D). University of Arizona, Tucson, Arizona, United States.
- Zeng, J., Brusseau, M.L., & Guo, B., 2021. Model validation and analyses of parameter sensitivity and uncertainty for modeling long-term retention and leaching of PFAS in the vadose zone. Journal of Hydrology, 603, 127172.
- Guo, B., Zeng, J. and Brusseau, M.L., 2020. A mathematical model for the release, transport, and retention of per- and polyfluoroalkyl substances (PFAS) in the vadose zone. Water Resources Research, 56(2), e2019WR026667.

## License

This project is licensed under the [CC BY-ND 4.0 License](https://github.com/GuoSFPLab/PFAS-LEACH-Tier-3-4/blob/main/LICENSE).

## Contact

For questions, please contact the development team at boguo@arizona.edu.
