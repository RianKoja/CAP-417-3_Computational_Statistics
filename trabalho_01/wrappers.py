import random
import numpy as np


class PythonRNG:
    def __init__(self, seed=None):
        self.rng = random.Random(seed)

    def random(self):
        return self.rng.random()


class NumPyRNG:
    def __init__(self, seed=None):
        self.rng = np.random.default_rng(seed)

    def random(self):
        return self.rng.random()


class JuliaRNG:
    def __init__(self, seed=None):
        self.seed = seed
        self.buffer = []
        self.batch_size = 1000

    def random(self):
        if not self.buffer:
            import subprocess

            seed_code = f"Random.seed!({self.seed});" if self.seed is not None else ""
            cmd = f'julia -e "using Random; {seed_code} for i in 1:{self.batch_size} println(rand()) end"'
            out = subprocess.check_output(cmd, shell=True).decode()
            self.buffer = [float(x) for x in out.splitlines() if x.strip()]
            self.seed = None  # Avoid re-seeding if we generate more batches
        return self.buffer.pop(0)


class RRNG:
    def __init__(self, seed=None):
        self.seed = seed
        self.buffer = []
        self.batch_size = 1000

    def random(self):
        if not self.buffer:
            import subprocess

            seed_code = f"set.seed({self.seed});" if self.seed is not None else ""
            cmd = f"Rscript -e 'RNGkind(\"Marsaglia-Multicarry\"); {seed_code} cat(runif({self.batch_size}))'"
            out = subprocess.check_output(cmd, shell=True).decode()
            self.buffer = [float(x) for x in out.split()]
            self.seed = None
        return self.buffer.pop(0)


class RustRNGWrapper:
    def __init__(self, seed=None):
        import rust_rng

        self.rng = rust_rng.RustRNG(seed)

    def random(self):
        return self.rng.random()
