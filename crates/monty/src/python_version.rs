//! Python version configuration for the Monty interpreter.
//!
//! Monty can target different Python versions (3.10–3.14), which affects:
//! - `sys.version` and `sys.version_info` values reported at runtime
//! - Type checking behavior (via Ruff's `PythonVersion`)
//!
//! The default target version is Python 3.14, matching Monty's primary development target.
//! Selecting a different version changes the reported version metadata but does **not**
//! gate language features — Monty's bytecode compiler always supports the full feature set.

use std::fmt;

/// The Python version that the Monty interpreter targets.
///
/// Controls `sys.version_info`, `sys.version`, and the type-checking target.
/// Defaults to [`PythonVersion::Py3_14`].
///
/// # Supported versions
///
/// Only Python 3.10 through 3.14 are supported.  Attempting to use an
/// unsupported version will fail at construction time.
#[derive(Debug, Default, Clone, Copy, PartialEq, Eq, Hash, serde::Serialize, serde::Deserialize)]
pub enum PythonVersion {
    /// Python 3.10
    Py3_10,
    /// Python 3.11
    Py3_11,
    /// Python 3.12
    Py3_12,
    /// Python 3.13
    Py3_13,
    /// Python 3.14 (default)
    #[default]
    Py3_14,
}

impl PythonVersion {
    /// Returns the major version number (always 3).
    #[must_use]
    pub const fn major(self) -> u8 {
        3
    }

    /// Returns the minor version number (10–14).
    #[must_use]
    pub const fn minor(self) -> u8 {
        match self {
            Self::Py3_10 => 10,
            Self::Py3_11 => 11,
            Self::Py3_12 => 12,
            Self::Py3_13 => 13,
            Self::Py3_14 => 14,
        }
    }

    /// Returns the `sys.version` string, e.g. `"3.14.0 (Monty)"`.
    #[must_use]
    pub fn version_string(self) -> String {
        format!("{}.{}.0 (Monty)", self.major(), self.minor())
    }

    /// Parses a `"major.minor"` string into a `PythonVersion`.
    ///
    /// Returns `None` for unsupported versions.
    #[must_use]
    pub fn from_str_opt(s: &str) -> Option<Self> {
        match s {
            "3.10" => Some(Self::Py3_10),
            "3.11" => Some(Self::Py3_11),
            "3.12" => Some(Self::Py3_12),
            "3.13" => Some(Self::Py3_13),
            "3.14" => Some(Self::Py3_14),
            _ => None,
        }
    }

    /// Converts to Ruff's `PythonVersion` for type checking integration.
    #[must_use]
    pub fn to_ruff(self) -> ruff_python_ast::PythonVersion {
        ruff_python_ast::PythonVersion {
            major: self.major(),
            minor: self.minor(),
        }
    }
}

impl fmt::Display for PythonVersion {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}.{}", self.major(), self.minor())
    }
}
