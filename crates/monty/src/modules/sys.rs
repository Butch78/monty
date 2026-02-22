//! Implementation of the `sys` module.
//!
//! Provides a minimal implementation of Python's `sys` module with:
//! - `version`: Python version string (e.g., "3.14.0 (Monty)")
//! - `version_info`: Named tuple (3, 14, 0, 'final', 0)
//! - `platform`: Platform identifier ("monty")
//! - `stdout`: Marker for standard output (no real functionality)
//! - `stderr`: Marker for standard error (no real functionality)
//!
//! The version values are derived from the [`PythonVersion`](crate::python_version::PythonVersion)
//! stored in `Interns`, which defaults to Python 3.14 but can be configured
//! when creating a [`MontyRun`](crate::run::MontyRun).

use crate::{
    heap::{Heap, HeapData, HeapId},
    intern::{Interns, StaticStrings},
    resource::{ResourceError, ResourceTracker},
    types::{Module, NamedTuple, Str},
    value::{Marker, Value},
};

/// Creates the `sys` module and allocates it on the heap.
///
/// The version information (`sys.version`, `sys.version_info`) is derived from
/// the Python version configured in `interns`.
///
/// Returns a HeapId pointing to the newly allocated module.
///
/// # Panics
///
/// Panics if the required strings have not been pre-interned during prepare phase.
pub fn create_module(heap: &mut Heap<impl ResourceTracker>, interns: &Interns) -> Result<HeapId, ResourceError> {
    let mut module = Module::new(StaticStrings::Sys);

    // sys.platform
    module.set_attr(StaticStrings::Platform, StaticStrings::Monty.into(), heap, interns);

    // sys.stdout / sys.stderr - markers for standard output/error
    module.set_attr(
        StaticStrings::Stdout,
        Value::Marker(Marker(StaticStrings::Stdout)),
        heap,
        interns,
    );
    module.set_attr(
        StaticStrings::Stderr,
        Value::Marker(Marker(StaticStrings::Stderr)),
        heap,
        interns,
    );

    let py_version = interns.python_version();

    // sys.version - heap-allocated string like "3.14.0 (Monty)"
    let version_str = Str::new(py_version.version_string());
    let version_id = heap.allocate(HeapData::Str(version_str))?;
    module.set_attr(StaticStrings::Version, Value::Ref(version_id), heap, interns);

    // sys.version_info - named tuple (major, minor, micro, releaselevel, serial)
    let version_info = NamedTuple::new(
        StaticStrings::SysVersionInfo,
        vec![
            StaticStrings::Major.into(),
            StaticStrings::Minor.into(),
            StaticStrings::Micro.into(),
            StaticStrings::Releaselevel.into(),
            StaticStrings::Serial.into(),
        ],
        vec![
            Value::Int(i64::from(py_version.major())),
            Value::Int(i64::from(py_version.minor())),
            Value::Int(0),
            Value::InternString(StaticStrings::Final.into()),
            Value::Int(0),
        ],
    );
    let version_info_id = heap.allocate(HeapData::NamedTuple(version_info))?;
    module.set_attr(StaticStrings::VersionInfo, Value::Ref(version_info_id), heap, interns);

    heap.allocate(HeapData::Module(module))
}
