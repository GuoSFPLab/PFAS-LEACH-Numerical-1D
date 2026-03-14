# ESTCP-PFAS-LEACH-Numerical-1D

## macOS arm64 Binary Example Package

This package contains the macOS Apple Silicon binary version of `ESTCP-PFAS-LEACH-Numerical-1D` together with three example cases.

The same three example cases are provided for all supported operating systems.
The main platform-specific differences are the executable file and launcher
script.

### Package contents

- `bin/ESTCP-PFAS-LEACH-Numerical-1D`
- `Exp1/`, `Exp2/`, `Exp3/`
- `LICENSE`
- `README.md`

### Quick start

```bash
cd Exp1
bash Run.sh
python3 plot_outputs.py
```

### Notes

- The plotting script requires `pandas` and `matplotlib`.
- Figures will be written to `FIGURES/`.
- Main model outputs will be written to `OUTPUT/`.
- macOS uses `Run.sh`; Windows uses `Run.bat`.

### License

See `LICENSE`.
