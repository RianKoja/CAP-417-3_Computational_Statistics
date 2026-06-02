import pandas as pd
import numpy as np
from wrappers import PythonRNG, JuliaRNG, RRNG, RustRNGWrapper


def generate_data(n=10000, seed=42):
    print(f"Generating {n} samples for each language (seed={seed})...")
    data = {}

    rngs = {
        "Python": PythonRNG(seed),
        "Julia": JuliaRNG(seed),
        "R": RRNG(seed),
        "Rust": RustRNGWrapper(seed),
    }

    for name, rng in rngs.items():
        print(f"  Generating {name}...")
        data[name] = [rng.random() for _ in range(n)]

    df = pd.DataFrame(data)
    df.to_csv("rng_samples.csv", index=False)
    print("Data saved to rng_samples.csv")


if __name__ == "__main__":
    generate_data()
