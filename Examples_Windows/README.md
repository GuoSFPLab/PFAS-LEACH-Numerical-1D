# ESTCP-PFAS-LEACH-Numerical-1D

## Windows Binary Example Package

This package contains the Windows binary version of `ESTCP-PFAS-LEACH-Numerical-1D` together with three example cases.

The same three example cases are provided for all supported operating systems.
The main platform-specific differences are the executable file and launcher
script.

### Package contents

- `bin/ESTCP-PFAS-LEACH-Numerical-1D.exe`
- `Exp1/`, `Exp2/`, `Exp3/`
- `LICENSE`
- `README.md`

### Quick start

1. Open `Exp1`.
2. Double-click `Run.bat`.
3. Run:

```bat
python plot_outputs.py
```

### Notes

- The plotting script requires `pandas` and `matplotlib`.
- Figures will be written to `FIGURES/`.
- Main model outputs will be written to `OUTPUT/`.
- Windows uses `Run.bat`; Linux and macOS use `Run.sh`.

### License

See `LICENSE`.
