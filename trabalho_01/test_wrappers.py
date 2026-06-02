from wrappers import PythonRNG, NumPyRNG, JuliaRNG, RRNG, RustRNGWrapper


def test_rng(name, rng_class, seed=42):
    print(f"Testing {name}...")
    try:
        rng = rng_class(seed=seed)
        nums = [rng.random() for _ in range(5)]
        print(f"  {name} numbers (seed={seed}): {nums}")

        rng2 = rng_class(seed=seed)
        nums2 = [rng2.random() for _ in range(5)]
        assert nums == nums2, f"{name} sequence mismatch with same seed"
        print(f"  {name} seed test passed.")

        for n in nums:
            assert 0 <= n <= 1, f"{name} number out of range: {n}"
        print(f"  {name} range test passed.")
    except Exception as e:
        print(f"  {name} FAILED: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_rng("Python", PythonRNG)
    test_rng("NumPy", NumPyRNG)
    test_rng("Julia", JuliaRNG)
    test_rng("R", RRNG)
    test_rng("Rust", RustRNGWrapper)
