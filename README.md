# ESTCP-PFAS-LEACH-Numerical-1D (Tier 2) - Example Packages

This README provides a combined overview of the binary example packages provided with this software:

- `Examples_Windows`
- `Examples_Linux`
- `Examples_MacOS_arm64`
- `Examples_MacOS_x86_64`

All packages are binary-only (no source code).

## 1) Choose the correct package

| OS | Package folder | Executable |
|---|---|---|
| Windows | `Examples_Windows` | `bin/ESTCP-PFAS-LEACH-Numerical-1D.exe` |
| Linux x86_64 | `Examples_Linux` | `bin/ESTCP-PFAS-LEACH-Numerical-1D` |
| macOS Apple Silicon | `Examples_MacOS_arm64` | `bin/ESTCP-PFAS-LEACH-Numerical-1D` |
| macOS Intel | `Examples_MacOS_x86_64` | `bin/ESTCP-PFAS-LEACH-Numerical-1D` |

For macOS, check architecture first:

```bash
uname -m
```

- `arm64` -> use `Examples_MacOS_arm64`
- `x86_64` -> use `Examples_MacOS_x86_64`

## 2) Standard folder layout

Each package has:

- `bin/` (model executable)
- `Exp1/`, `Exp2/`, `Exp3/` (example cases)
- `LICENSE`
- `README.md`

Each example case (`Exp*`) has:

- `INPUT/` (required model inputs)
- `OUTPUT/` (model outputs)
- `Run.bat` (Windows) or `Run.sh` (Linux/macOS)
- `plot_outputs.py` (visualization script)

## 3) Quick start

### Windows

1. Open `Examples_Windows/Exp1/`.
2. Double-click `Run.bat`.
3. Run plotting script:
   ```bat
   python plot_outputs.py
   ```

### Linux

```bash
cd Examples_Linux/Exp1
bash Run.sh
python3 plot_outputs.py
```

### macOS (arm64 or x86_64 package)

```bash
cd Examples_MacOS_arm64/Exp1
# or: cd Examples_MacOS_x86_64/Exp1
bash Run.sh
python3 plot_outputs.py
```

Outputs:

- `OUTPUT/` -> CSV results
- `FIGURES/` -> generated PDF figures

## 4) Create your own case

Use `Exp3` as a template:

- Windows:
  1. Copy `Exp3` to `MyCase`.
  2. Edit `MyCase/INPUT/*.csv`.
  3. Run `MyCase/Run.bat`.
  4. Run `python plot_outputs.py` in `MyCase`.

- Linux/macOS:
  ```bash
  cp -r Exp3 MyCase
  cd MyCase
  # edit INPUT/*.csv
  bash Run.sh
  python3 plot_outputs.py
  ```

## 5) Input and output files

Main input files in `INPUT/`:

- `System_ctrl.csv`
- `Soil_profile.csv`
- `PFAS_properties.csv`
- `Boundary_conditions.csv`
- `Output_ctrl.csv`
- optional: `Root_uptake.csv`, `Groundwater_pollution.csv`

Main output files in `OUTPUT/`:

- `1.Profile-Time-*.csv`
- `2.Time series.csv`
- `3.Observations.csv`
- `4.Summary.csv`

## 6) Python dependencies for plotting

Install if needed:

```bash
python3 -m pip install pandas matplotlib
```

On Windows (if needed):

```bat
pip install pandas matplotlib
```

## 7) Troubleshooting

- `Permission denied` (Linux/macOS):
  ```bash
  chmod +x ../bin/ESTCP-PFAS-LEACH-Numerical-1D
  ```
- `bad CPU type in executable` (macOS):
  - switch to the other macOS package (`arm64` vs `x86_64`).
- Missing Python packages:
  - install `pandas` and `matplotlib`.

## 8) Notes

- Official software name: `ESTCP-PFAS-LEACH-Numerical-1D`.
- The same three example cases are provided for all supported operating systems.
- The main platform-specific differences are the executable file and launcher script.

## 9) License and contact

- License: `LICENSE` (CC BY-ND 4.0)
- Contact: `boguo@arizona.edu`
