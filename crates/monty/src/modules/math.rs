//! Implementation of Python's `math` module.
//!
//! Provides mathematical functions and constants matching CPython 3.14 behavior
//! and error messages. All functions are pure computations that don't require
//! host involvement, so they return `Value` directly rather than `AttrCallResult`.
//!
//! ## Implemented functions
//!
//! **Rounding**: `floor`, `ceil`, `trunc`
//! **Roots & powers**: `sqrt`, `isqrt`, `cbrt`, `pow`, `exp`, `exp2`, `expm1`
//! **Logarithms**: `log`, `log2`, `log10`, `log1p`
//! **Trigonometric**: `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `atan2`
//! **Hyperbolic**: `sinh`, `cosh`, `tanh`, `asinh`, `acosh`, `atanh`
//! **Angular**: `degrees`, `radians`
//! **Float properties**: `fabs`, `isnan`, `isinf`, `isfinite`, `copysign`, `isclose`,
//!   `nextafter`, `ulp`
//! **Integer math**: `factorial`, `gcd`, `lcm`, `comb`, `perm`
//! **Modular**: `fmod`, `remainder`, `modf`, `frexp`, `ldexp`
//! **Special**: `gamma`, `lgamma`, `erf`, `erfc`
//!
//! ## Constants
//!
//! `pi`, `e`, `tau`, `inf`, `nan`

use smallvec::smallvec;

use crate::{
    args::ArgValues,
    defer_drop,
    exception_private::{ExcType, RunResult, SimpleException},
    heap::{Heap, HeapData, HeapId},
    intern::{Interns, StaticStrings},
    modules::ModuleFunctions,
    resource::{ResourceError, ResourceTracker},
    types::{Module, PyTrait, allocate_tuple},
    value::Value,
};

/// Math module functions — each variant corresponds to a Python-visible function.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, strum::Display, serde::Serialize, serde::Deserialize)]
#[strum(serialize_all = "lowercase")]
pub(crate) enum MathFunctions {
    // Rounding
    Floor,
    Ceil,
    Trunc,
    // Roots & powers
    Sqrt,
    Isqrt,
    Cbrt,
    Pow,
    Exp,
    Exp2,
    Expm1,
    // Logarithms
    Log,
    Log1p,
    Log2,
    Log10,
    // Float properties
    Fabs,
    Isnan,
    Isinf,
    Isfinite,
    Copysign,
    Isclose,
    Nextafter,
    Ulp,
    // Trigonometric
    Sin,
    Cos,
    Tan,
    Asin,
    Acos,
    Atan,
    Atan2,
    // Hyperbolic
    Sinh,
    Cosh,
    Tanh,
    Asinh,
    Acosh,
    Atanh,
    // Angular conversion
    Degrees,
    Radians,
    // Integer math
    Factorial,
    Gcd,
    Lcm,
    Comb,
    Perm,
    // Modular / decomposition
    Fmod,
    Remainder,
    Modf,
    Frexp,
    Ldexp,
    // Special functions
    Gamma,
    Lgamma,
    Erf,
    Erfc,
}

/// Creates the `math` module and allocates it on the heap.
///
/// Registers all math functions and constants (`pi`, `e`, `tau`, `inf`, `nan`)
/// matching CPython's `math` module. Functions are registered as
/// `ModuleFunctions::Math` variants.
///
/// # Returns
/// A `HeapId` pointing to the newly allocated module.
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
    // Rounding
    (StaticStrings::Floor, MathFunctions::Floor),
    (StaticStrings::Ceil, MathFunctions::Ceil),
    (StaticStrings::Trunc, MathFunctions::Trunc),
    // Roots & powers
    (StaticStrings::Sqrt, MathFunctions::Sqrt),
    (StaticStrings::Isqrt, MathFunctions::Isqrt),
    (StaticStrings::Cbrt, MathFunctions::Cbrt),
    (StaticStrings::Pow, MathFunctions::Pow),
    (StaticStrings::Exp, MathFunctions::Exp),
    (StaticStrings::Exp2, MathFunctions::Exp2),
    (StaticStrings::Expm1, MathFunctions::Expm1),
    // Logarithms
    (StaticStrings::Log, MathFunctions::Log),
    (StaticStrings::Log1p, MathFunctions::Log1p),
    (StaticStrings::Log2, MathFunctions::Log2),
    (StaticStrings::Log10, MathFunctions::Log10),
    // Float properties
    (StaticStrings::Fabs, MathFunctions::Fabs),
    (StaticStrings::Isnan, MathFunctions::Isnan),
    (StaticStrings::Isinf, MathFunctions::Isinf),
    (StaticStrings::Isfinite, MathFunctions::Isfinite),
    (StaticStrings::Copysign, MathFunctions::Copysign),
    (StaticStrings::Isclose, MathFunctions::Isclose),
    (StaticStrings::Nextafter, MathFunctions::Nextafter),
    (StaticStrings::Ulp, MathFunctions::Ulp),
    // Trigonometric
    (StaticStrings::Sin, MathFunctions::Sin),
    (StaticStrings::Cos, MathFunctions::Cos),
    (StaticStrings::Tan, MathFunctions::Tan),
    (StaticStrings::Asin, MathFunctions::Asin),
    (StaticStrings::Acos, MathFunctions::Acos),
    (StaticStrings::Atan, MathFunctions::Atan),
    (StaticStrings::Atan2, MathFunctions::Atan2),
    // Hyperbolic
    (StaticStrings::Sinh, MathFunctions::Sinh),
    (StaticStrings::Cosh, MathFunctions::Cosh),
    (StaticStrings::Tanh, MathFunctions::Tanh),
    (StaticStrings::Asinh, MathFunctions::Asinh),
    (StaticStrings::Acosh, MathFunctions::Acosh),
    (StaticStrings::Atanh, MathFunctions::Atanh),
    // Angular conversion
    (StaticStrings::Degrees, MathFunctions::Degrees),
    (StaticStrings::Radians, MathFunctions::Radians),
    // Integer math
    (StaticStrings::Factorial, MathFunctions::Factorial),
    (StaticStrings::Gcd, MathFunctions::Gcd),
    (StaticStrings::Lcm, MathFunctions::Lcm),
    (StaticStrings::Comb, MathFunctions::Comb),
    (StaticStrings::Perm, MathFunctions::Perm),
    // Modular / decomposition
    (StaticStrings::Fmod, MathFunctions::Fmod),
    (StaticStrings::Remainder, MathFunctions::Remainder),
    (StaticStrings::Modf, MathFunctions::Modf),
    (StaticStrings::Frexp, MathFunctions::Frexp),
    (StaticStrings::Ldexp, MathFunctions::Ldexp),
    // Special functions
    (StaticStrings::Gamma, MathFunctions::Gamma),
    (StaticStrings::Lgamma, MathFunctions::Lgamma),
    (StaticStrings::Erf, MathFunctions::Erf),
    (StaticStrings::Erfc, MathFunctions::Erfc),
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
        // Rounding
        MathFunctions::Floor => math_floor(heap, args),
        MathFunctions::Ceil => math_ceil(heap, args),
        MathFunctions::Trunc => math_trunc(heap, args),
        // Roots & powers
        MathFunctions::Sqrt => math_sqrt(heap, args),
        MathFunctions::Isqrt => math_isqrt(heap, args),
        MathFunctions::Cbrt => math_cbrt(heap, args),
        MathFunctions::Pow => math_pow(heap, args),
        MathFunctions::Exp => math_exp(heap, args),
        MathFunctions::Exp2 => math_exp2(heap, args),
        MathFunctions::Expm1 => math_expm1(heap, args),
        // Logarithms
        MathFunctions::Log => math_log(heap, args),
        MathFunctions::Log1p => math_log1p(heap, args),
        MathFunctions::Log2 => math_log2(heap, args),
        MathFunctions::Log10 => math_log10(heap, args),
        // Float properties
        MathFunctions::Fabs => math_fabs(heap, args),
        MathFunctions::Isnan => math_isnan(heap, args),
        MathFunctions::Isinf => math_isinf(heap, args),
        MathFunctions::Isfinite => math_isfinite(heap, args),
        MathFunctions::Copysign => math_copysign(heap, args),
        MathFunctions::Isclose => math_isclose(heap, args),
        MathFunctions::Nextafter => math_nextafter(heap, args),
        MathFunctions::Ulp => math_ulp(heap, args),
        // Trigonometric
        MathFunctions::Sin => math_sin(heap, args),
        MathFunctions::Cos => math_cos(heap, args),
        MathFunctions::Tan => math_tan(heap, args),
        MathFunctions::Asin => math_asin(heap, args),
        MathFunctions::Acos => math_acos(heap, args),
        MathFunctions::Atan => math_atan(heap, args),
        MathFunctions::Atan2 => math_atan2(heap, args),
        // Hyperbolic
        MathFunctions::Sinh => math_sinh(heap, args),
        MathFunctions::Cosh => math_cosh(heap, args),
        MathFunctions::Tanh => math_tanh(heap, args),
        MathFunctions::Asinh => math_asinh(heap, args),
        MathFunctions::Acosh => math_acosh(heap, args),
        MathFunctions::Atanh => math_atanh(heap, args),
        // Angular conversion
        MathFunctions::Degrees => math_degrees(heap, args),
        MathFunctions::Radians => math_radians(heap, args),
        // Integer math
        MathFunctions::Factorial => math_factorial(heap, args),
        MathFunctions::Gcd => math_gcd(heap, args),
        MathFunctions::Lcm => math_lcm(heap, args),
        MathFunctions::Comb => math_comb(heap, args),
        MathFunctions::Perm => math_perm(heap, args),
        // Modular / decomposition
        MathFunctions::Fmod => math_fmod(heap, args),
        MathFunctions::Remainder => math_remainder(heap, args),
        MathFunctions::Modf => math_modf(heap, args),
        MathFunctions::Frexp => math_frexp(heap, args),
        MathFunctions::Ldexp => math_ldexp(heap, args),
        // Special functions
        MathFunctions::Gamma => math_gamma(heap, args),
        MathFunctions::Lgamma => math_lgamma(heap, args),
        MathFunctions::Erf => math_erf(heap, args),
        MathFunctions::Erfc => math_erfc(heap, args),
    }
}

// ==========================
// Rounding functions
// ==========================

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

// ==========================
// Roots & powers
// ==========================

/// `math.sqrt(x)` — returns the square root of x.
///
/// Always returns a float. Raises `ValueError` for negative inputs with a
/// descriptive message matching CPython 3.14: "expected a nonnegative input, got <x>".
fn math_sqrt(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.sqrt", heap)?;
    defer_drop!(value, heap);

    let f = value_to_float(value, "math.sqrt", heap)?;
    if f < 0.0 {
        Err(SimpleException::new_msg(ExcType::ValueError, format!("expected a nonnegative input, got {f:?}")).into())
    } else {
        Ok(Value::Float(f.sqrt()))
    }
}

/// `math.isqrt(n)` — returns the integer square root of a non-negative integer.
///
/// Returns the largest integer `r` such that `r * r <= n`.
/// Only accepts non-negative integers (and bools).
fn math_isqrt(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.isqrt", heap)?;
    defer_drop!(value, heap);

    let n = value_to_int(value, "math.isqrt", heap)?;
    if n < 0 {
        return Err(SimpleException::new_msg(ExcType::ValueError, "isqrt() argument must be nonnegative").into());
    }
    if n == 0 {
        return Ok(Value::Int(0));
    }

    // Newton's method for integer square root.
    // Initial estimate from f64 sqrt, refined to exact i64 result.
    #[expect(
        clippy::cast_precision_loss,
        clippy::cast_possible_truncation,
        reason = "initial estimate doesn't need to be exact, Newton's method refines it"
    )]
    let mut x = (n as f64).sqrt() as i64;
    // Refine: divide-and-average avoids overflow from (x + n/x)
    loop {
        let q = n / x;
        if q >= x {
            break;
        }
        x = x - (x - q) / 2;
        if x <= q {
            x = q;
            break;
        }
    }
    // Ensure we don't overshoot due to rounding.
    // Use `x > n / x` instead of `x * x > n` to avoid i64 overflow for large n.
    while x > n / x {
        x -= 1;
    }
    Ok(Value::Int(x))
}

/// `math.cbrt(x)` — returns the cube root of x.
///
/// Always returns a float. Unlike `sqrt`, works for negative inputs.
fn math_cbrt(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.cbrt", heap)?;
    defer_drop!(value, heap);

    let f = value_to_float(value, "math.cbrt", heap)?;
    Ok(Value::Float(f.cbrt()))
}

/// `math.pow(x, y)` — returns x raised to the power y.
///
/// Always returns a float. Unlike the builtin `pow()`, does not support
/// three-argument modular exponentiation. Raises `ValueError` for
/// negative base with non-integer exponent.
fn math_pow(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let (x_val, y_val) = args.get_two_args("math.pow", heap)?;
    defer_drop!(x_val, heap);
    defer_drop!(y_val, heap);

    let x = value_to_float(x_val, "math.pow", heap)?;
    let y = value_to_float(y_val, "math.pow", heap)?;
    let result = x.powf(y);
    // CPython raises ValueError for domain errors: 0**negative, negative**non-integer
    if result.is_nan() && !x.is_nan() && !y.is_nan() {
        return Err(SimpleException::new_msg(ExcType::ValueError, "math domain error").into());
    }
    if result.is_infinite() && x.is_finite() && y.is_finite() {
        // 0**negative is a domain error (ValueError), not overflow
        if x == 0.0 && y < 0.0 {
            return Err(SimpleException::new_msg(ExcType::ValueError, "math domain error").into());
        }
        return Err(SimpleException::new_msg(ExcType::OverflowError, "math range error").into());
    }
    Ok(Value::Float(result))
}

/// `math.exp(x)` — returns e raised to the power x.
fn math_exp(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.exp", heap)?;
    defer_drop!(value, heap);

    let f = value_to_float(value, "math.exp", heap)?;
    let result = f.exp();
    if result.is_infinite() && f.is_finite() {
        return Err(SimpleException::new_msg(ExcType::OverflowError, "math range error").into());
    }
    Ok(Value::Float(result))
}

/// `math.exp2(x)` — returns 2 raised to the power x.
fn math_exp2(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.exp2", heap)?;
    defer_drop!(value, heap);

    let f = value_to_float(value, "math.exp2", heap)?;
    let result = f.exp2();
    if result.is_infinite() && f.is_finite() {
        return Err(SimpleException::new_msg(ExcType::OverflowError, "math range error").into());
    }
    Ok(Value::Float(result))
}

/// `math.expm1(x)` — returns e**x - 1.
///
/// More accurate than `exp(x) - 1` for small values of x.
fn math_expm1(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.expm1", heap)?;
    defer_drop!(value, heap);

    let f = value_to_float(value, "math.expm1", heap)?;
    let result = f.exp_m1();
    if result.is_infinite() && f.is_finite() {
        return Err(SimpleException::new_msg(ExcType::OverflowError, "math range error").into());
    }
    Ok(Value::Float(result))
}

// ==========================
// Logarithms
// ==========================

/// `math.log(x[, base])` — returns the logarithm of x.
///
/// With one argument, returns the natural logarithm (base e).
/// With two arguments, returns `log(x) / log(base)`.
/// Raises `ValueError` for non-positive inputs (CPython 3.14: "expected a positive input").
fn math_log(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let (x_val, base_val) = args.get_one_two_args("math.log", heap)?;
    defer_drop!(x_val, heap);
    defer_drop!(base_val, heap);

    let x = value_to_float(x_val, "math.log", heap)?;
    if x <= 0.0 {
        return Err(SimpleException::new_msg(ExcType::ValueError, "expected a positive input").into());
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
                return Err(SimpleException::new_msg(ExcType::ZeroDivisionError, "division by zero").into());
            }
            if base <= 0.0 {
                return Err(SimpleException::new_msg(ExcType::ValueError, "expected a positive input").into());
            }
            Ok(Value::Float(x.ln() / base.ln()))
        }
        None => Ok(Value::Float(x.ln())),
    }
}

/// `math.log1p(x)` — returns the natural logarithm of 1 + x.
///
/// More accurate than `log(1 + x)` for small values of x.
/// CPython 3.14 raises ValueError with "expected argument value > -1, got <x>".
fn math_log1p(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.log1p", heap)?;
    defer_drop!(value, heap);

    let f = value_to_float(value, "math.log1p", heap)?;
    if f <= -1.0 {
        return Err(
            SimpleException::new_msg(ExcType::ValueError, format!("expected argument value > -1, got {f:?}")).into(),
        );
    }
    Ok(Value::Float(f.ln_1p()))
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
        Err(SimpleException::new_msg(ExcType::ValueError, "expected a positive input").into())
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
        Err(SimpleException::new_msg(ExcType::ValueError, "expected a positive input").into())
    } else {
        Ok(Value::Float(f.log10()))
    }
}

// ==========================
// Float properties
// ==========================

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

/// `math.nextafter(x, y)` — returns the next float after x towards y.
fn math_nextafter(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let (x_val, y_val) = args.get_two_args("math.nextafter", heap)?;
    defer_drop!(x_val, heap);
    defer_drop!(y_val, heap);

    let x = value_to_float(x_val, "math.nextafter", heap)?;
    let y = value_to_float(y_val, "math.nextafter", heap)?;

    // Use bit manipulation to compute nextafter, matching C's nextafter behavior:
    // - If x == y, return y
    // - If x or y is NaN, return NaN
    // - Otherwise, step x towards y by one ULP
    let result = nextafter_impl(x, y);
    Ok(Value::Float(result))
}

/// `math.ulp(x)` — returns the value of the least significant bit of x.
///
/// For finite non-zero x, returns the smallest float `u` such that `x + u != x`.
/// Special cases: `ulp(nan)` returns nan, `ulp(inf)` returns inf.
fn math_ulp(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.ulp", heap)?;
    defer_drop!(value, heap);

    let f = value_to_float(value, "math.ulp", heap)?;
    if f.is_nan() {
        return Ok(Value::Float(f64::NAN));
    }
    if f.is_infinite() {
        return Ok(Value::Float(f64::INFINITY));
    }
    let f = f.abs();
    if f == 0.0 {
        // CPython returns the smallest positive subnormal: 5e-324
        return Ok(Value::Float(f64::from_bits(1)));
    }
    // ULP = nextafter(f, inf) - f
    let next = nextafter_impl(f, f64::INFINITY);
    Ok(Value::Float(next - f))
}

// ==========================
// Trigonometric functions
// ==========================

/// `math.sin(x)` — returns the sine of x (in radians).
///
/// CPython 3.14 raises ValueError for infinity: "expected a finite input, got inf".
fn math_sin(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.sin", heap)?;
    defer_drop!(value, heap);

    let f = value_to_float(value, "math.sin", heap)?;
    require_finite(f)?;
    Ok(Value::Float(f.sin()))
}

/// `math.cos(x)` — returns the cosine of x (in radians).
fn math_cos(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.cos", heap)?;
    defer_drop!(value, heap);

    let f = value_to_float(value, "math.cos", heap)?;
    require_finite(f)?;
    Ok(Value::Float(f.cos()))
}

/// `math.tan(x)` — returns the tangent of x (in radians).
fn math_tan(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.tan", heap)?;
    defer_drop!(value, heap);

    let f = value_to_float(value, "math.tan", heap)?;
    require_finite(f)?;
    Ok(Value::Float(f.tan()))
}

/// `math.asin(x)` — returns the arc sine of x (in radians).
///
/// CPython 3.14: "expected a number in range from -1 up to 1, got <x>".
fn math_asin(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.asin", heap)?;
    defer_drop!(value, heap);

    let f = value_to_float(value, "math.asin", heap)?;
    // NaN passes through (asin(nan) = nan), but out-of-range finite values raise
    if !f.is_nan() && !(-1.0..=1.0).contains(&f) {
        return Err(SimpleException::new_msg(
            ExcType::ValueError,
            format!("expected a number in range from -1 up to 1, got {f:?}"),
        )
        .into());
    }
    Ok(Value::Float(f.asin()))
}

/// `math.acos(x)` — returns the arc cosine of x (in radians).
///
/// CPython 3.14: "expected a number in range from -1 up to 1, got <x>".
fn math_acos(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.acos", heap)?;
    defer_drop!(value, heap);

    let f = value_to_float(value, "math.acos", heap)?;
    // NaN passes through (acos(nan) = nan), but out-of-range finite values raise
    if !f.is_nan() && !(-1.0..=1.0).contains(&f) {
        return Err(SimpleException::new_msg(
            ExcType::ValueError,
            format!("expected a number in range from -1 up to 1, got {f:?}"),
        )
        .into());
    }
    Ok(Value::Float(f.acos()))
}

/// `math.atan(x)` — returns the arc tangent of x (in radians).
fn math_atan(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.atan", heap)?;
    defer_drop!(value, heap);

    let f = value_to_float(value, "math.atan", heap)?;
    Ok(Value::Float(f.atan()))
}

/// `math.atan2(y, x)` — returns atan(y/x) in radians, using the signs of both
/// to determine the correct quadrant.
fn math_atan2(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let (y_val, x_val) = args.get_two_args("math.atan2", heap)?;
    defer_drop!(y_val, heap);
    defer_drop!(x_val, heap);

    let y = value_to_float(y_val, "math.atan2", heap)?;
    let x = value_to_float(x_val, "math.atan2", heap)?;
    Ok(Value::Float(y.atan2(x)))
}

// ==========================
// Hyperbolic functions
// ==========================

/// `math.sinh(x)` — returns the hyperbolic sine of x.
fn math_sinh(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.sinh", heap)?;
    defer_drop!(value, heap);

    let f = value_to_float(value, "math.sinh", heap)?;
    let result = f.sinh();
    if result.is_infinite() && f.is_finite() {
        return Err(SimpleException::new_msg(ExcType::OverflowError, "math range error").into());
    }
    Ok(Value::Float(result))
}

/// `math.cosh(x)` — returns the hyperbolic cosine of x.
fn math_cosh(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.cosh", heap)?;
    defer_drop!(value, heap);

    let f = value_to_float(value, "math.cosh", heap)?;
    let result = f.cosh();
    if result.is_infinite() && f.is_finite() {
        return Err(SimpleException::new_msg(ExcType::OverflowError, "math range error").into());
    }
    Ok(Value::Float(result))
}

/// `math.tanh(x)` — returns the hyperbolic tangent of x.
fn math_tanh(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.tanh", heap)?;
    defer_drop!(value, heap);

    let f = value_to_float(value, "math.tanh", heap)?;
    Ok(Value::Float(f.tanh()))
}

/// `math.asinh(x)` — returns the inverse hyperbolic sine of x.
fn math_asinh(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.asinh", heap)?;
    defer_drop!(value, heap);

    let f = value_to_float(value, "math.asinh", heap)?;
    Ok(Value::Float(f.asinh()))
}

/// `math.acosh(x)` — returns the inverse hyperbolic cosine of x.
///
/// CPython 3.14: "expected argument value not less than 1, got <x>".
fn math_acosh(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.acosh", heap)?;
    defer_drop!(value, heap);

    let f = value_to_float(value, "math.acosh", heap)?;
    if f < 1.0 {
        return Err(SimpleException::new_msg(
            ExcType::ValueError,
            format!("expected argument value not less than 1, got {f:?}"),
        )
        .into());
    }
    Ok(Value::Float(f.acosh()))
}

/// `math.atanh(x)` — returns the inverse hyperbolic tangent of x.
///
/// CPython 3.14: "expected a number between -1 and 1, got <x>".
fn math_atanh(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.atanh", heap)?;
    defer_drop!(value, heap);

    let f = value_to_float(value, "math.atanh", heap)?;
    if f <= -1.0 || f >= 1.0 {
        return Err(SimpleException::new_msg(
            ExcType::ValueError,
            format!("expected a number between -1 and 1, got {f:?}"),
        )
        .into());
    }
    Ok(Value::Float(f.atanh()))
}

// ==========================
// Angular conversion
// ==========================

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
// Integer math
// ==========================

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
    let lcm_u = (abs_a / g)
        .checked_mul(abs_b)
        .ok_or_else(|| SimpleException::new_msg(ExcType::OverflowError, "integer overflow in lcm"))?;
    Ok(Value::Int(lcm_u.cast_signed()))
}

/// `math.comb(n, k)` — returns the number of ways to choose k items from n.
///
/// Both arguments must be non-negative integers.
fn math_comb(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let (n_val, k_val) = args.get_two_args("math.comb", heap)?;
    defer_drop!(n_val, heap);
    defer_drop!(k_val, heap);

    let n = value_to_int(n_val, "math.comb", heap)?;
    let k = value_to_int(k_val, "math.comb", heap)?;

    if n < 0 {
        return Err(SimpleException::new_msg(ExcType::ValueError, "n must be a non-negative integer").into());
    }
    if k < 0 {
        return Err(SimpleException::new_msg(ExcType::ValueError, "k must be a non-negative integer").into());
    }
    if k > n {
        return Ok(Value::Int(0));
    }

    // Use the smaller of k and n-k for efficiency: C(n, k) = C(n, n-k)
    let k = k.min(n - k);
    let mut result: i64 = 1;
    for i in 0..k {
        // result = result * (n - i) / (i + 1), done carefully to avoid overflow
        match result.checked_mul(n - i) {
            Some(v) => result = v / (i + 1),
            None => {
                return Err(SimpleException::new_msg(ExcType::OverflowError, "integer overflow in comb").into());
            }
        }
    }
    Ok(Value::Int(result))
}

/// `math.perm(n, k)` — returns the number of k-length permutations from n items.
///
/// Both arguments must be non-negative integers.
fn math_perm(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let (n_val, k_val) = args.get_two_args("math.perm", heap)?;
    defer_drop!(n_val, heap);
    defer_drop!(k_val, heap);

    let n = value_to_int(n_val, "math.perm", heap)?;
    let k = value_to_int(k_val, "math.perm", heap)?;

    if n < 0 {
        return Err(SimpleException::new_msg(ExcType::ValueError, "n must be a non-negative integer").into());
    }
    if k < 0 {
        return Err(SimpleException::new_msg(ExcType::ValueError, "k must be a non-negative integer").into());
    }
    if k > n {
        return Ok(Value::Int(0));
    }

    let mut result: i64 = 1;
    for i in 0..k {
        match result.checked_mul(n - i) {
            Some(v) => result = v,
            None => {
                return Err(SimpleException::new_msg(ExcType::OverflowError, "integer overflow in perm").into());
            }
        }
    }
    Ok(Value::Int(result))
}

// ==========================
// Modular / decomposition
// ==========================

/// `math.fmod(x, y)` — returns x modulo y as a float.
///
/// Unlike `x % y`, the result has the same sign as x. Raises `ValueError`
/// when y is zero (CPython: "math domain error").
fn math_fmod(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let (x_val, y_val) = args.get_two_args("math.fmod", heap)?;
    defer_drop!(x_val, heap);
    defer_drop!(y_val, heap);

    let x = value_to_float(x_val, "math.fmod", heap)?;
    let y = value_to_float(y_val, "math.fmod", heap)?;

    if y == 0.0 || x.is_infinite() {
        // CPython raises for both fmod(x, 0) and fmod(inf, y)
        // but NaN inputs propagate
        if !x.is_nan() && !y.is_nan() {
            return Err(SimpleException::new_msg(ExcType::ValueError, "math domain error").into());
        }
    }
    Ok(Value::Float(x % y))
}

/// `math.remainder(x, y)` — IEEE 754 remainder of x with respect to y.
///
/// The result is `x - n*y` where n is the closest integer to `x/y`.
fn math_remainder(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let (x_val, y_val) = args.get_two_args("math.remainder", heap)?;
    defer_drop!(x_val, heap);
    defer_drop!(y_val, heap);

    let x = value_to_float(x_val, "math.remainder", heap)?;
    let y = value_to_float(y_val, "math.remainder", heap)?;

    // NaN propagates
    if x.is_nan() || y.is_nan() {
        return Ok(Value::Float(f64::NAN));
    }
    if y == 0.0 {
        return Err(SimpleException::new_msg(ExcType::ValueError, "math domain error").into());
    }
    if x.is_infinite() {
        return Err(SimpleException::new_msg(ExcType::ValueError, "math domain error").into());
    }
    if y.is_infinite() {
        return Ok(Value::Float(x));
    }

    // IEEE 754 remainder: result = x - round_half_even(x/y) * y
    let n = round_half_even(x / y);
    let result = x - n * y;
    Ok(Value::Float(result))
}

/// `math.modf(x)` — returns the fractional and integer parts of x as a tuple.
///
/// Both values carry the sign of x. Returns `(fractional, integer)`.
fn math_modf(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.modf", heap)?;
    defer_drop!(value, heap);

    let f = value_to_float(value, "math.modf", heap)?;

    // Special cases: modf(inf) = (0.0, inf), modf(nan) = (nan, nan)
    if f.is_nan() {
        let tuple = allocate_tuple(smallvec![Value::Float(f64::NAN), Value::Float(f64::NAN)], heap)?;
        return Ok(tuple);
    }
    if f.is_infinite() {
        // The fractional part is ±0.0 (signed to match the input sign)
        let frac = if f > 0.0 { 0.0 } else { -0.0_f64 };
        let tuple = allocate_tuple(smallvec![Value::Float(frac), Value::Float(f)], heap)?;
        return Ok(tuple);
    }

    let integer = f.trunc();
    let fractional = f - integer;
    let tuple = allocate_tuple(smallvec![Value::Float(fractional), Value::Float(integer)], heap)?;
    Ok(tuple)
}

/// `math.frexp(x)` — returns (mantissa, exponent) such that `x == mantissa * 2**exponent`.
///
/// The mantissa is always in the range [0.5, 1.0) or zero.
/// Returns a tuple `(float, int)`.
#[expect(
    clippy::cast_possible_wrap,
    reason = "IEEE 754 bit manipulation requires u64-to-i64 casts for exponent values masked to 11 bits"
)]
fn math_frexp(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.frexp", heap)?;
    defer_drop!(value, heap);

    let f = value_to_float(value, "math.frexp", heap)?;

    if f == 0.0 || f.is_nan() || f.is_infinite() {
        // Special cases: frexp(0) = (0.0, 0), frexp(nan) = (nan, 0), frexp(inf) = (inf, 0)
        let tuple = allocate_tuple(smallvec![Value::Float(f), Value::Int(0)], heap)?;
        return Ok(tuple);
    }

    // Decompose using bit manipulation of IEEE 754 representation
    let bits = f.to_bits();
    let sign = bits & (1u64 << 63);
    let exponent_bits = ((bits >> 52) & 0x7ff) as i64;
    let mantissa_bits = bits & 0x000f_ffff_ffff_ffff;

    if exponent_bits == 0 {
        // Subnormal: multiply by 2^53 to normalize, then adjust
        let normalized = f * (1u64 << 53) as f64;
        let n_bits = normalized.to_bits();
        let n_exp = ((n_bits >> 52) & 0x7ff) as i64;
        let n_mant = n_bits & 0x000f_ffff_ffff_ffff;
        // Exponent: (biased_exp - 1022) gives the frexp exponent for normal numbers,
        // minus 53 to compensate for the 2^53 normalization factor
        let exp = n_exp - 1022 - 53;
        let m = f64::from_bits(sign | (0x3fe_u64 << 52) | n_mant);
        let tuple = allocate_tuple(smallvec![Value::Float(m), Value::Int(exp)], heap)?;
        return Ok(tuple);
    }

    // For normal numbers: frexp exponent = biased_exponent - 1022
    // (1022 = IEEE 754 bias 1023 minus 1, since mantissa is in [0.5, 1.0) not [1.0, 2.0))
    let exp = exponent_bits - 1022;
    let m = f64::from_bits(sign | (0x3fe_u64 << 52) | mantissa_bits);

    let tuple = allocate_tuple(smallvec![Value::Float(m), Value::Int(exp)], heap)?;
    Ok(tuple)
}

/// `math.ldexp(x, i)` — returns `x * 2**i`, the inverse of `frexp`.
#[expect(
    clippy::cast_sign_loss,
    reason = "exponent values are validated to be in range before casting"
)]
fn math_ldexp(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let (x_val, i_val) = args.get_two_args("math.ldexp", heap)?;
    defer_drop!(x_val, heap);
    defer_drop!(i_val, heap);

    let x = value_to_float(x_val, "math.ldexp", heap)?;
    let i = value_to_int(i_val, "math.ldexp", heap)?;

    // Special cases: inf/nan/zero pass through regardless of exponent
    if x.is_nan() || x.is_infinite() || x == 0.0 {
        return Ok(Value::Float(x));
    }

    // Clamp exponent and check for overflow, matching CPython behavior.
    let result = if i > 1074 {
        // Would overflow to infinity — CPython raises OverflowError
        return Err(SimpleException::new_msg(ExcType::OverflowError, "math range error").into());
    } else if i < -1074 {
        // Underflows to zero
        if x > 0.0 { 0.0 } else { -0.0 }
    } else {
        // Use successive doubling/halving to avoid intermediate overflow
        let mut result = x;
        let mut exp = i;
        while exp > 0 {
            let step = exp.min(1023);
            result *= f64::from_bits(((1023 + step) as u64) << 52);
            exp -= step;
        }
        while exp < 0 {
            let step = (-exp).min(1022);
            result *= f64::from_bits(((1023 - step) as u64) << 52);
            exp += step;
        }
        result
    };

    // If the result overflowed to infinity, CPython raises OverflowError
    if result.is_infinite() {
        return Err(SimpleException::new_msg(ExcType::OverflowError, "math range error").into());
    }

    Ok(Value::Float(result))
}

// ==========================
// Special functions
// ==========================

/// `math.gamma(x)` — returns the Gamma function at x.
///
/// CPython 3.14 raises ValueError for non-positive integers:
/// "expected a noninteger or positive integer, got <x>".
#[expect(
    clippy::float_cmp,
    reason = "exact comparison detects integer poles of gamma function"
)]
fn math_gamma(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.gamma", heap)?;
    defer_drop!(value, heap);

    let f = value_to_float(value, "math.gamma", heap)?;
    // CPython raises ValueError for -inf
    if f == f64::NEG_INFINITY {
        return Err(SimpleException::new_msg(
            ExcType::ValueError,
            format!("expected a noninteger or positive integer, got {f:?}"),
        )
        .into());
    }
    // Check for non-positive integers (poles of the gamma function)
    if f <= 0.0 && f == f.floor() && f.is_finite() {
        return Err(SimpleException::new_msg(
            ExcType::ValueError,
            format!("expected a noninteger or positive integer, got {f:?}"),
        )
        .into());
    }

    let result = gamma_impl(f);
    if result.is_infinite() && f.is_finite() {
        return Err(SimpleException::new_msg(ExcType::OverflowError, "math range error").into());
    }
    Ok(Value::Float(result))
}

/// `math.lgamma(x)` — returns the natural log of the absolute value of Gamma(x).
#[expect(
    clippy::float_cmp,
    reason = "exact comparison detects integer poles of gamma function"
)]
fn math_lgamma(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.lgamma", heap)?;
    defer_drop!(value, heap);

    let f = value_to_float(value, "math.lgamma", heap)?;
    // Check for non-positive integers (poles of the gamma function)
    if f <= 0.0 && f == f.floor() && f.is_finite() {
        return Err(SimpleException::new_msg(
            ExcType::ValueError,
            format!("expected a noninteger or positive integer, got {f:?}"),
        )
        .into());
    }

    let result = lgamma_impl(f);
    if result.is_infinite() && f.is_finite() {
        return Err(SimpleException::new_msg(ExcType::OverflowError, "math range error").into());
    }
    Ok(Value::Float(result))
}

/// `math.erf(x)` — returns the error function at x.
fn math_erf(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.erf", heap)?;
    defer_drop!(value, heap);

    let f = value_to_float(value, "math.erf", heap)?;
    Ok(Value::Float(erf_impl(f)))
}

/// `math.erfc(x)` — returns the complementary error function at x (1 - erf(x)).
///
/// More accurate than `1 - erf(x)` for large x.
fn math_erfc(heap: &mut Heap<impl ResourceTracker>, args: ArgValues) -> RunResult<Value> {
    let value = args.get_one_arg("math.erfc", heap)?;
    defer_drop!(value, heap);

    let f = value_to_float(value, "math.erfc", heap)?;
    Ok(Value::Float(erfc_impl(f)))
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
#[expect(
    clippy::cast_precision_loss,
    reason = "i64-to-f64 can lose precision for large integers (beyond 2^53), but this matches CPython's conversion semantics"
)]
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

/// Requires that a float is finite, raising ValueError if it's inf or nan.
///
/// CPython 3.14 uses "expected a finite input, got inf" for trig functions.
fn require_finite(f: f64) -> RunResult<()> {
    if f.is_infinite() {
        Err(SimpleException::new_msg(ExcType::ValueError, format!("expected a finite input, got {f:?}")).into())
    } else {
        Ok(())
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

/// Rounds a float using "round half to even" (banker's rounding).
///
/// When the fractional part is exactly 0.5, rounds to the nearest even integer.
/// This matches IEEE 754 rounding behavior used by `math.remainder`.
#[expect(clippy::float_cmp, reason = "exact comparison needed for halfway detection")]
fn round_half_even(x: f64) -> f64 {
    let rounded = x.round();
    // Check if we're exactly at a halfway point
    if (x - rounded).abs() == 0.5 {
        // Round to even: if rounded is odd, go the other way
        let truncated = x.trunc();
        if truncated % 2.0 == 0.0 { truncated } else { rounded }
    } else {
        rounded
    }
}

/// Computes `nextafter(x, y)` — the next representable float from x towards y.
///
/// Matches C's `nextafter` behavior: if x == y returns y, NaN propagates.
#[expect(clippy::float_cmp, reason = "exact comparison is correct for nextafter semantics")]
fn nextafter_impl(x: f64, y: f64) -> f64 {
    if x.is_nan() || y.is_nan() {
        return f64::NAN;
    }
    if x == y {
        return y;
    }
    if x == 0.0 {
        // Step from zero towards y: smallest subnormal with sign of y
        return if y > 0.0 {
            f64::from_bits(1)
        } else {
            f64::from_bits(1 | (1u64 << 63))
        };
    }
    let bits = x.to_bits();
    let result_bits = if (x < y) == (x > 0.0) { bits + 1 } else { bits - 1 };
    f64::from_bits(result_bits)
}

/// Lanczos approximation of the Gamma function for positive arguments.
///
/// Uses a 7-term Lanczos series with g=7, which provides ~15 digits of
/// precision for positive real arguments. For negative non-integer arguments,
/// uses the reflection formula: Γ(x) = π / (sin(πx) · Γ(1-x)).
#[expect(
    clippy::float_cmp,
    clippy::cast_possible_truncation,
    clippy::cast_sign_loss,
    reason = "mathematical function needs exact comparisons and integer factorial computation"
)]
fn gamma_impl(x: f64) -> f64 {
    if x.is_nan() || x == f64::INFINITY {
        return x;
    }
    // Note: NEG_INFINITY and non-positive integer poles are handled by `math_gamma`
    // before this function is called, so we don't need to guard against them here.

    // For positive integers, return exact factorial
    if x > 0.0 && x == x.floor() && x <= 21.0 {
        let n = x as u64;
        let mut result: u64 = 1;
        for i in 2..n {
            result *= i;
        }
        return result as f64;
    }
    if x < 0.5 {
        // Reflection formula: Γ(x) = π / (sin(πx) · Γ(1-x))
        let sin_px = (std::f64::consts::PI * x).sin();
        return std::f64::consts::PI / (sin_px * gamma_impl(1.0 - x));
    }
    lanczos_gamma(x)
}

/// Lanczos series computation for Γ(x) where x >= 0.5.
#[expect(
    clippy::excessive_precision,
    clippy::inconsistent_digit_grouping,
    reason = "Lanczos coefficients require full precision and exact values"
)]
fn lanczos_gamma(x: f64) -> f64 {
    // Coefficients for g=7, n=9 (from Paul Godfrey's tables)
    const P: [f64; 9] = [
        0.999_999_999_999_809_93,
        676.520_368_121_885_1,
        -1259.139_216_722_402_8,
        771.323_428_777_653_08,
        -176.615_029_162_140_6,
        12.507_343_278_686_905,
        -0.138_571_095_265_720_12,
        9.984_369_578_019_572e-6,
        1.505_632_735_149_311_6e-7,
    ];
    const G: f64 = 7.0;

    let z = x - 1.0;
    let mut sum = P[0];
    for (i, &coeff) in P.iter().enumerate().skip(1) {
        sum += coeff / (z + i as f64);
    }
    let t = z + G + 0.5;
    (2.0 * std::f64::consts::PI).sqrt() * t.powf(z + 0.5) * (-t).exp() * sum
}

/// Computes ln(|Γ(x)|) using the Lanczos approximation.
#[expect(
    clippy::float_cmp,
    clippy::cast_possible_truncation,
    clippy::cast_sign_loss,
    reason = "mathematical function needs exact comparisons and integer factorial computation"
)]
fn lgamma_impl(x: f64) -> f64 {
    if x.is_nan() || x.is_infinite() {
        if x == f64::NEG_INFINITY {
            return f64::INFINITY;
        }
        return x.abs();
    }
    // Exact results for small positive integers: lgamma(n) = ln((n-1)!)
    if x > 0.0 && x == x.floor() && x <= 23.0 {
        let n = x as u64;
        let mut fact: u64 = 1;
        for i in 2..n {
            fact *= i;
        }
        return (fact as f64).ln();
    }
    if x < 0.5 {
        // Reflection: ln|Γ(x)| = ln(π) - ln|sin(πx)| - ln|Γ(1-x)|
        // Note: non-positive integer poles are handled by `math_lgamma` before
        // this function is called, so sin_px is always non-zero here.
        let sin_px = (std::f64::consts::PI * x).sin().abs();
        return std::f64::consts::PI.ln() - sin_px.ln() - lgamma_impl(1.0 - x);
    }
    lanczos_lgamma(x)
}

/// Lanczos series computation for ln(Γ(x)) where x >= 0.5.
#[expect(
    clippy::excessive_precision,
    clippy::inconsistent_digit_grouping,
    reason = "Lanczos coefficients require full precision and exact values"
)]
fn lanczos_lgamma(x: f64) -> f64 {
    const P: [f64; 9] = [
        0.999_999_999_999_809_93,
        676.520_368_121_885_1,
        -1259.139_216_722_402_8,
        771.323_428_777_653_08,
        -176.615_029_162_140_6,
        12.507_343_278_686_905,
        -0.138_571_095_265_720_12,
        9.984_369_578_019_572e-6,
        1.505_632_735_149_311_6e-7,
    ];
    const G: f64 = 7.0;

    let z = x - 1.0;
    let mut sum = P[0];
    for (i, &coeff) in P.iter().enumerate().skip(1) {
        sum += coeff / (z + i as f64);
    }
    let t = z + G + 0.5;
    0.5 * (2.0 * std::f64::consts::PI).ln() + (z + 0.5) * t.ln() - t + sum.ln()
}

/// Error function implementation using Horner's method with rational approximation.
///
/// Uses the Abramowitz and Stegun approximation (formula 7.1.26) which provides
/// a maximum error of 1.5×10⁻⁷.
#[expect(clippy::items_after_statements, reason = "constants grouped near their usage")]
fn erf_impl(x: f64) -> f64 {
    if x.is_nan() {
        return f64::NAN;
    }
    if x == 0.0 {
        return 0.0;
    }
    let sign = if x < 0.0 { -1.0 } else { 1.0 };
    let x = x.abs();
    if x >= 6.0 {
        // erf(x) is essentially ±1 for |x| >= 6
        return sign;
    }

    // Abramowitz & Stegun 7.1.26
    const A1: f64 = 0.254_829_592;
    const A2: f64 = -0.284_496_736;
    const A3: f64 = 1.421_413_741;
    const A4: f64 = -1.453_152_027;
    const A5: f64 = 1.061_405_429;
    const P: f64 = 0.327_591_1;

    let t = 1.0 / (1.0 + P * x);
    let y = 1.0 - (((((A5 * t + A4) * t) + A3) * t + A2) * t + A1) * t * (-x * x).exp();
    sign * y
}

/// Complementary error function: erfc(x) = 1 - erf(x).
///
/// More accurate than `1 - erf(x)` for large x values.
fn erfc_impl(x: f64) -> f64 {
    1.0 - erf_impl(x)
}
