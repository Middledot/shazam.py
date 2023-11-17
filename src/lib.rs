mod algorithm;
mod signature_format;
mod utils;
use pyo3::prelude::{
    pymodule,
    Python,
    PyModule,
    PyResult,
    wrap_pyfunction
};

#[pymodule]
fn shazam(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<signature_format::DecodedSignature>()?;
    m.add_function(wrap_pyfunction!(algorithm::make_signature_from_buffer, m)?)?;
    Ok(())
}
