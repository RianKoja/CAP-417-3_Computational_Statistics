# Assignment 04 — Soybean Sprout Growth Analysis

Graduate course "Estatística Computacional" at INPE/CAP. Author: Rian Koja.

## Dataset

**CongNaMul** soybean sprout dataset (Kaggle: `byunghyunban/congnamul`).  
Download with `make download` — lands in `~/.cache/kagglehub/datasets/byunghyunban/congnamul/versions/1`.

Five physical measurements per sprout: head length, body length, body thickness, tail length (mm), weight (mg).  
Each sprout appears 3× (different backgrounds); the script deduplicates by sample ID.  
Weight is missing (coded −1) for ~45 of 203 sprouts after outlier removal.

## Build

```
make download   # one-time data fetch
make run        # run analysis.py then compile report.typ → report.pdf
make clean      # delete generated SVGs
```

Requires `uv` (Python env) and `typst` on PATH.

## Constraints

- Report must be **≤ 4 pages** (A4, current margins).
- No hardcoded values in `report.typ` — all numbers come from `outputs/`.
- Only feature data is used; image/segmentation data is ignored.
