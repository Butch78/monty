//! Implementation of the `math` module.
//!
//! Provides mathematical functions and constants matching Python's `math` module.
//! All functions are pure computations that don't require host involvement,
//! so they return `Value` directly rather than `AttrCallResult`.
//!
//! Implemented functions:
//! - `floor(x)`, `ceil(x)`, `trunc(x)` - rounding functions
//! - `sqrt(x)` - square root
//! - `fabs(x)` - absolute value (always returns float)
//! - `isnan(x)`, `isinf(x)`, `isfinite(x)` - float classification
//! - `log(x[, base])`, `log2(x)`, `log10(x)` - logarithms
//! - `factorial(n)` - factorial
//! - `gcd(a, b)`, `lcm(a, b)` - greatest common divisor / least common multiple
//! - `copysign(x, y)` - copy sign of y to x
//! - `isclose(a, b)` - approximate equality
//! - `degrees(x)`, `radians(x)` - angle conversions
//!
//! Constants: `pi`, `e`, `tau`, `inf`, `nan`

use crate::{
    args::ArgValues,
    defer_drop,
    exception_private::{ExcType, RunResult, SimpleException},
    heap::{Heap, HeapData, HeapId},
    intern::{Interns, StaticStrings},
    modules::ModuleFunctions,
    resource::{ResourceError, ResourceTracker},
    types::{Module, PyTrait},
    value::Value,
};

/// Math module functions.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, strum::Display, serde::Serialize, serde::Deserialize)]
#[strum(serialize_all = "lowercase")]
pub(crate) enum MathFunctions {
    Floor,
    Ceil,
    Trunc,
    Sqrt,
    Fabs,
    Isnan,
    Isinf,
    Isfinite,
    Log,
    Log2,
    Log10,
    Factorial,
    Gcd,
    Lcm,
    Copysign,
    Isclose,
    Degrees,
    Radians,
}

/// Creates the `math` module and allocates it on the heap.
///
/// The module provides mathematical functions (floor, ceil, sqrt, log, etc.)
/// and constants (pi, e, tau, inf, nan).
///
/// # Returns
/// A HeapId pointing to the newly allocated module.
///
/// # Panics
/// Panics if the required strings have not been pre-interned during prepare phase.
pub fn create_module(heap: &mut Heap<impl ResourceTracker>, interns: &Interns) -> Result<HeapId, ResourceError> {
    let mut module = Module::new(StaticStrings::Math);

    // Register all math functions
    for (name, func) in MATH_FUNCTIONS {
        module.set_attr(
            *name,
            Value::ModuleFunction(ModuleFunctions::Math(*func)),
            heap,
            interns,
        );
    }

    // Constants
    module.set_attr(StaticStrings::Pi, Value::Float(std::f64::consts::PI), heap, interns);
    module.set_attr(StaticStrings::MathE, Value::Float(std::f64::consts::E), heap, interns);
    module.set_attr(StaticStrings::Tau, Value::Float(std::f64::consts::TAU), heap, interns);
    module.set_attr(StaticStrings::MathInf, Value::Float(f64::INFINITY), heap, interns);
    module.set_attr(StaticStrings::MathNan, Value::Float(f64::NAN), heap, interns);

    heap.allocate(HeapData::Module(module))
}

/// Static mapping of attribute names to math functions for module creation.
const MATH_FUNCTIONS: &[(StaticStrings, MathFunctions)] = &[
    (StaticStrings::Floor, MathFunctions::Floor),
    (StaticStrings::Ceil, MathFunctions::Ceil),
    (StaticStrings::Trunc, MathFunctions::Trunc),
    (StaticStrings::Sqrt, MathFunctions::Sqrt),
    (StaticStrings::Fabs, MathFunctions::Fabs),
    (StaticStrings::Isnan, MathFunctions::Isnan),
    (StaticStrings::Isinf, MathFunctions::Isinf),
    (StaticStrings::Isfinite, MathFunctions::Isfinite),
    (StaticStrings::Log, MathFunctions::Log),
    (StaticStrings::Log2, MathFunctions::Log2),
    (StaticStrings::Log10, MathFunctions::Log10),
    (StaticStrings::Factorial, MathFunctions::Factorial),
    (StaticStrings::Gcd, MathFunctions::Gcd),
    (StaticStrings::Lcm, MathFunctions::Lcm),
    (StaticStrings::Copysign, MathFunctions::Copysign),
    (StaticStrings::Isclose, MathFunctions::Isclose),
    (StaticStrings::Degrees, MathFunctions::Degrees),
    (StaticStrings::Radians, MathFunctions::Radians),
];

/// Dispatches a call to a math module function.
///
/// All math functions are pure computations and return `Value` directly.
pub(super) fn call(
    heap: &mut Heap<impl ResourceTracker>,
    function: MathFunctions,
    args: ArgValues,
) -> RunResult<Value> {
    match function {
        MathFunctions::Floor => math_floor(heap, args),
        MathFunctions::Ceil => math_ceil(heap, args),
        MathFunctions::Trunc => math_trunc(heap, args),
        MathFunctions::Sqrt => math_sqrt(heap, args),
        MathFunctions::Fabs => math_fabs(heap, args),
        MathFunctions::Isnan => math_isnan(heap, args),
        MathFunctions::Isinf => math_isinf(heap, args),
        MathFunctions::Isfinite => math_isfinite(heap, args),
        MathFunctions::Log => math_log(heap, args),
        MathFunctions::Log2 => math_log2(heap, args),
        MathFunctions::Log10 => math_log10(heap, args),
        MathFunctions::Factorial => math_factorial(heap, args),
        MathFunctions::Gcd => math_gcd(heap, args),
        MathFunctions::Lcm => math_lcm(heap, args),
        MathFunctions::Copysign => math_copysign(heap, args),
        MathFunctions::Isclose => math_isclose(heap, args),
        MathFunctions::Degrees => math_degrees(heap, args),
        MathFunctions::Radians => math_radians(heap, args),
    }
}

/// `math.floor(x)` — returns the largest integer less than or equal to x.
///
/// Accepts int, float, or bool. Returns int.
/// Raises `OverflowError` for infinity, `ValueError` for NaN.
fn math_floor(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.floor", heap)?;
    defer_drop!(value, heap);

    match value {
        Value::Float(f) => float_to_int_checked(f.floor(), *f),
        Value::Int(n) => Ok(Value::Int(*n)),
        Value::Bool(b) => Ok(Value::Int(i64::from(*b))),
        _ => Err(ExcType::type_error(format!(
            "must be real number, not {}",
            value.py_type(heap)
        ))),
    }
}

/// `math.ceil(x)` — returns the smallest integer greater than or equal to x.
///
/// Accepts int, float, or bool. Returns int.
/// Raises `OverflowError` for infinity, `ValueError` for NaN.
fn math_ceil(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.ceil", heap)?;
    defer_drop!(value, heap);

    match value {
        Value::Float(f) => float_to_int_checked(f.ceil(), *f),
        Value::Int(n) => Ok(Value::Int(*n)),
        Value::Bool(b) => Ok(Value::Int(i64::from(*b))),
        _ => Err(ExcType::type_error(format!(
            "must be real number, not {}",
            value.py_type(heap)
        ))),
    }
}

/// `math.trunc(x)` — truncates x to the nearest integer toward zero.
///
/// Accepts int, float, or bool. Returns int.
fn math_trunc(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.trunc", heap)?;
    defer_drop!(value, heap);

    match value {
        Value::Float(f) => float_to_int_checked(f.trunc(), *f),
        Value::Int(n) => Ok(Value::Int(*n)),
        Value::Bool(b) => Ok(Value::Int(i64::from(*b))),
        _ => Err(ExcType::type_error(format!(
            "type {} doesn't define __trunc__ method",
            value.py_type(heap)
        ))),
    }
}

/// `math.sqrt(x)` — returns the square root of x.
///
/// Always returns a float. Raises `ValueError` for negative inputs,
/// `TypeError` for non-numeric types.
fn math_sqrt(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.sqrt", heap)?;
    defer_drop!(value, heap);

    let f = value_to_float(value, "math.sqrt", heap)?;
    if f < 0.0 {
        Err(SimpleException::new_msg(ExcType::ValueError, "math domain error").into())
    } else {
        Ok(Value::Float(f.sqrt()))
    }
}

/// `math.fabs(x)` — returns the absolute value as a float.
///
/// Unlike the builtin `abs()`, always returns a float.
fn math_fabs(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.fabs", heap)?;
    defer_drop!(value, heap);

    let f = value_to_float(value, "math.fabs", heap)?;
    Ok(Value::Float(f.abs()))
}

/// `math.isnan(x)` — returns True if x is NaN.
fn math_isnan(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.isnan", heap)?;
    defer_drop!(value, heap);

    let f = value_to_float(value, "math.isnan", heap)?;
    Ok(Value::Bool(f.is_nan()))
}

/// `math.isinf(x)` — returns True if x is positive or negative infinity.
fn math_isinf(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.isinf", heap)?;
    defer_drop!(value, heap);

    let f = value_to_float(value, "math.isinf", heap)?;
    Ok(Value::Bool(f.is_infinite()))
}

/// `math.isfinite(x)` — returns True if x is neither infinity nor NaN.
fn math_isfinite(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.isfinite", heap)?;
    defer_drop!(value, heap);

    let f = value_to_float(value, "math.isfinite", heap)?;
    Ok(Value::Bool(f.is_finite()))
}

/// `math.log(x[, base])` — returns the logarithm of x.
///
/// With one argument, returns the natural logarithm (base e).
/// With two arguments, returns `log(x) / log(base)`.
/// Raises `ValueError` for non-positive inputs.
fn math_log(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let (x_val, base_val) = args.get_one_two_args("math.log", heap)?;
    defer_drop!(x_val, heap);
    defer_drop!(base_val, heap);

    let x = value_to_float(x_val, "math.log", heap)?;
    if x <= 0.0 {
        return Err(SimpleException::new_msg(ExcType::ValueError, "math domain error").into());
    }

    match base_val {
        Some(base_v) => {
            let base = value_to_float(base_v, "math.log", heap)?;
            // base == 1.0 causes division by zero in log(x)/log(base), matching
            // CPython which raises ZeroDivisionError for this case.
            #[expect(
                clippy::float_cmp,
                reason = "exact comparison with 1.0 is intentional — log(1.0) is exactly 0.0"
            )]
            if base == 1.0 {
                return Err(SimpleException::new_msg(ExcType::ZeroDivisionError, "float division by zero").into());
            }
            if base <= 0.0 {
                return Err(SimpleException::new_msg(ExcType::ValueError, "math domain error").into());
            }
            Ok(Value::Float(x.ln() / base.ln()))
        }
        None => Ok(Value::Float(x.ln())),
    }
}

/// `math.log2(x)` — returns the base-2 logarithm of x.
///
/// Returns `inf` for positive infinity, `nan` for NaN.
/// Raises `ValueError` for non-positive finite inputs.
fn math_log2(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.log2", heap)?;
    defer_drop!(value, heap);

    let f = value_to_float(value, "math.log2", heap)?;
    if f <= 0.0 {
        Err(SimpleException::new_msg(ExcType::ValueError, "math domain error").into())
    } else {
        Ok(Value::Float(f.log2()))
    }
}

/// `math.log10(x)` — returns the base-10 logarithm of x.
///
/// Returns `inf` for positive infinity, `nan` for NaN.
/// Raises `ValueError` for non-positive finite inputs.
fn math_log10(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.log10", heap)?;
    defer_drop!(value, heap);

    let f = value_to_float(value, "math.log10", heap)?;
    if f <= 0.0 {
        Err(SimpleException::new_msg(ExcType::ValueError, "math domain error").into())
    } else {
        Ok(Value::Float(f.log10()))
    }
}

/// `math.factorial(n)` — returns n factorial.
///
/// Only accepts non-negative integers (and bools). Raises `ValueError` for
/// negative values, `TypeError` for non-integer types.
fn math_factorial(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.factorial", heap)?;
    defer_drop!(value, heap);

    let n = match value {
        Value::Int(n) => *n,
        Value::Bool(b) => i64::from(*b),
        _ => {
            return Err(ExcType::type_error(format!(
                "'{}' object cannot be interpreted as an integer",
                value.py_type(heap)
            )));
        }
    };

    if n < 0 {
        return Err(
            SimpleException::new_msg(ExcType::ValueError, "factorial() not defined for negative values").into(),
        );
    }

    // Compute factorial iteratively
    let mut result: i64 = 1;
    for i in 2..=n {
        match result.checked_mul(i) {
            Some(v) => result = v,
            None => {
                // Overflow — for simplicity, return an error for very large factorials
                // since we don't have LongInt factorial support yet
                return Err(
                    SimpleException::new_msg(ExcType::OverflowError, "int too large to convert to factorial").into(),
                );
            }
        }
    }
    Ok(Value::Int(result))
}

/// `math.gcd(a, b)` — returns the greatest common divisor of two integers.
///
/// The result is always non-negative.
fn math_gcd(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let (a_val, b_val) = args.get_two_args("math.gcd", heap)?;
    defer_drop!(a_val, heap);
    defer_drop!(b_val, heap);

    let a = value_to_int(a_val, "math.gcd", heap)?;
    let b = value_to_int(b_val, "math.gcd", heap)?;
    // GCD result is always <= max(|a|, |b|) which fits in i64 since the inputs were i64
    Ok(Value::Int(gcd(a.unsigned_abs(), b.unsigned_abs()).cast_signed()))
}

/// `math.lcm(a, b)` — returns the least common multiple of two integers.
///
/// The result is always non-negative. Returns 0 if either argument is 0.
fn math_lcm(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let (a_val, b_val) = args.get_two_args("math.lcm", heap)?;
    defer_drop!(a_val, heap);
    defer_drop!(b_val, heap);

    let a = value_to_int(a_val, "math.lcm", heap)?;
    let b = value_to_int(b_val, "math.lcm", heap)?;

    if a == 0 || b == 0 {
        return Ok(Value::Int(0));
    }

    let abs_a = a.unsigned_abs();
    let abs_b = b.unsigned_abs();
    let g = gcd(abs_a, abs_b);
    // lcm(a, b) = |a| / gcd(a,b) * |b| — dividing first avoids intermediate overflow
    Ok(Value::Int((abs_a / g * abs_b).cast_signed()))
}

/// `math.copysign(x, y)` — returns x with the sign of y.
///
/// Always returns a float.
fn math_copysign(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let (x_val, y_val) = args.get_two_args("math.copysign", heap)?;
    defer_drop!(x_val, heap);
    defer_drop!(y_val, heap);

    let x = value_to_float(x_val, "math.copysign", heap)?;
    let y = value_to_float(y_val, "math.copysign", heap)?;
    Ok(Value::Float(x.copysign(y)))
}

/// `math.isclose(a, b)` — returns True if a and b are close to each other.
///
/// Uses default tolerances: `rel_tol=1e-9`, `abs_tol=0.0`.
/// Matches CPython's default behavior without keyword argument support.
fn math_isclose(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let (a_val, b_val) = args.get_two_args("math.isclose", heap)?;
    defer_drop!(a_val, heap);
    defer_drop!(b_val, heap);

    let a = value_to_float(a_val, "math.isclose", heap)?;
    let b = value_to_float(b_val, "math.isclose", heap)?;

    // CPython defaults: rel_tol=1e-9, abs_tol=0.0
    let rel_tol: f64 = 1e-9;
    let abs_tol: f64 = 0.0;

    // Exact equality check matches CPython's isclose() behavior — two identical
    // values (including infinities) are always considered close.
    #[expect(
        clippy::float_cmp,
        reason = "exact equality check matches CPython's isclose() semantics"
    )]
    if a == b {
        return Ok(Value::Bool(true));
    }
    if a.is_infinite() || b.is_infinite() {
        return Ok(Value::Bool(false));
    }
    if a.is_nan() || b.is_nan() {
        return Ok(Value::Bool(false));
    }

    let diff = (a - b).abs();
    let result = diff <= (rel_tol * a.abs()).max(rel_tol * b.abs()).max(abs_tol);
    Ok(Value::Bool(result))
}

/// `math.degrees(x)` — converts angle x from radians to degrees.
fn math_degrees(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.degrees", heap)?;
    defer_drop!(value, heap);

    let f = value_to_float(value, "math.degrees", heap)?;
    Ok(Value::Float(f.to_degrees()))
}

/// `math.radians(x)` — converts angle x from degrees to radians.
fn math_radians(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.radians", heap)?;
    defer_drop!(value, heap);

    let f = value_to_float(value, "math.radians", heap)?;
    Ok(Value::Float(f.to_radians()))
}

// ==========================
// Helper functions
// ==========================

/// Converts a rounded float to an integer `Value`, checking for infinity/NaN.
///
/// `rounded` is the already-rounded float value (e.g., from `floor()`, `ceil()`, `trunc()`).
/// `original` is the original input float, used only to determine the error type:
/// infinity produces `OverflowError`, NaN produces `ValueError`.
fn float_to_int_checked(rounded: f64, original: f64) -> RunResult<Value> {
    if original.is_infinite() {
        Err(SimpleException::new_msg(ExcType::OverflowError, "cannot convert float infinity to integer").into())
    } else if original.is_nan() {
        Err(SimpleException::new_msg(ExcType::ValueError, "cannot convert float NaN to integer").into())
    } else {
        // Saturating cast: values outside i64 range clamp to i64::MIN/MAX
        #[expect(
            clippy::cast_possible_truncation,
            reason = "intentional: after inf/NaN check, float-to-int saturates which is correct behavior"
        )]
        let result = rounded as i64;
        Ok(Value::Int(result))
    }
}

/// Converts a `Value` to `f64`, raising `TypeError` if the value is not numeric.
///
/// Accepts `Float`, `Int`, and `Bool` values. For other types, raises a `TypeError`
/// with a message matching CPython's format: "must be real number, not <type>".
fn value_to_float(value: &Value, _func_name: &str, heap: &Heap<impl ResourceTracker>) -> RunResult<f64> {
    match value {
        Value::Float(f) => Ok(*f),
        Value::Int(n) => Ok(*n as f64),
        Value::Bool(b) => Ok(if *b { 1.0 } else { 0.0 }),
        _ => Err(ExcType::type_error(format!(
            "must be real number, not {}",
            value.py_type(heap)
        ))),
    }
}

/// Converts a `Value` to `i64`, raising `TypeError` if the value is not an integer.
///
/// Accepts `Int` and `Bool` values. For other types, raises a `TypeError`
/// with a message matching CPython's format.
fn value_to_int(value: &Value, _func_name: &str, heap: &Heap<impl ResourceTracker>) -> RunResult<i64> {
    match value {
        Value::Int(n) => Ok(*n),
        Value::Bool(b) => Ok(i64::from(*b)),
        _ => Err(ExcType::type_error(format!(
            "'{}' object cannot be interpreted as an integer",
            value.py_type(heap)
        ))),
    }
}

/// Euclidean GCD algorithm for unsigned 64-bit integers.
fn gcd(mut a: u64, mut b: u64) -> u64 {
    while b != 0 {
        let t = b;
        b = a % b;
        a = t;
    }
    a
}
