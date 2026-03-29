use pyo3::prelude::*;
use rand::prelude::*;
use rand_chacha::ChaCha12Rng;

#[pyclass]
pub struct RustRNG {
    rng: ChaCha12Rng,
}

#[pymethods]
impl RustRNG {
    #[new]
    pub fn new(seed: Option<u64>) -> Self {
        let rng = match seed {
            Some(s) => ChaCha12Rng::seed_from_u64(s),
            None => ChaCha12Rng::from_entropy(),
        };
        Self { rng }
    }

    pub fn random(&mut self) -> f64 {
        self.rng.gen()
    }
}

#[pymodule]
fn rust_rng(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<RustRNG>()?;
    Ok(())
}
