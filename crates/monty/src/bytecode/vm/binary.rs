//! Binary and in-place operation helpers for the VM.

use super::VM;
use crate::{
    defer_drop,
    exception_private::{ExcType, RunError},
    heap::HeapGuard,
    resource::ResourceTracker,
    types::{
        PyTrait,
        set::{SetBinaryOp, binary_set_op},
    },
    value::{BitwiseOp, Value},
};

impl<T: ResourceTracker> VM<'_, '_, T> {
    /// Binary addition with proper refcount handling.
    ///
    /// Uses lazy type capture: only calls `py_type()` in error paths to avoid
    /// overhead on the success path (99%+ of operations).
    pub(super) fn binary_add(&mut self) -> Result<(), RunError> {
        let this = self;

        let rhs = this.pop();
        defer_drop!(rhs, this);
        let lhs = this.pop();
        defer_drop!(lhs, this);

        match lhs.py_add(rhs, this.heap, this.interns) {
            Ok(Some(v)) => {
                this.push(v);
                Ok(())
            }
            Ok(None) => {
                let lhs_type = lhs.py_type(this.heap);
                let rhs_type = rhs.py_type(this.heap);
                Err(ExcType::binary_type_error("+", lhs_type, rhs_type))
            }
            Err(e) => Err(e.into()),
        }
    }

    /// Binary subtraction with proper refcount handling.
    ///
    /// Handles both numeric subtraction and set difference (`-` operator).
    /// For sets/frozensets, delegates to [`binary_set_op`] which needs `interns`
    /// for element hashing and equality. Uses lazy type capture: only calls
    /// `py_type()` in error paths.
    pub(super) fn binary_sub(&mut self) -> Result<(), RunError> {
        let this = self;

        let rhs = this.pop();
        defer_drop!(rhs, this);
        let lhs = this.pop();
        defer_drop!(lhs, this);

        // Set/frozenset difference: handled here because `py_sub` doesn't
        // have access to `interns`, which set operations need for hashing.
        if let (Value::Ref(lhs_id), Value::Ref(rhs_id)) = (lhs, rhs) {
            let interns = this.interns;
            if let Some(result) = binary_set_op(SetBinaryOp::Difference, *lhs_id, *rhs_id, this.heap, interns)? {
                this.push(result);
                return Ok(());
            }
        }

        match lhs.py_sub(rhs, this.heap) {
            Ok(Some(v)) => {
                this.push(v);
                Ok(())
            }
            Ok(None) => {
                let lhs_type = lhs.py_type(this.heap);
                let rhs_type = rhs.py_type(this.heap);
                Err(ExcType::binary_type_error("-", lhs_type, rhs_type))
            }
            Err(e) => Err(e.into()),
        }
    }

    /// Binary multiplication with proper refcount handling.
    ///
    /// Uses lazy type capture: only calls `py_type()` in error paths.
    pub(super) fn binary_mult(&mut self) -> Result<(), RunError> {
        let this = self;

        let rhs = this.pop();
        defer_drop!(rhs, this);
        let lhs = this.pop();
        defer_drop!(lhs, this);

        match lhs.py_mult(rhs, this.heap, this.interns) {
            Ok(Some(v)) => {
                this.push(v);
                Ok(())
            }
            Ok(None) => {
                let lhs_type = lhs.py_type(this.heap);
                let rhs_type = rhs.py_type(this.heap);
                Err(ExcType::binary_type_error("*", lhs_type, rhs_type))
            }
            Err(e) => Err(e),
        }
    }

    /// Binary division with proper refcount handling.
    ///
    /// Uses lazy type capture: only calls `py_type()` in error paths.
    pub(super) fn binary_div(&mut self) -> Result<(), RunError> {
        let this = self;

        let rhs = this.pop();
        defer_drop!(rhs, this);
        let lhs = this.pop();
        defer_drop!(lhs, this);

        match lhs.py_div(rhs, this.heap, this.interns) {
            Ok(Some(v)) => {
                this.push(v);
                Ok(())
            }
            Ok(None) => {
                let lhs_type = lhs.py_type(this.heap);
                let rhs_type = rhs.py_type(this.heap);
                Err(ExcType::binary_type_error("/", lhs_type, rhs_type))
            }
            Err(e) => Err(e),
        }
    }

    /// Binary floor division with proper refcount handling.
    ///
    /// Uses lazy type capture: only calls `py_type()` in error paths.
    pub(super) fn binary_floordiv(&mut self) -> Result<(), RunError> {
        let this = self;

        let rhs = this.pop();
        defer_drop!(rhs, this);
        let lhs = this.pop();
        defer_drop!(lhs, this);

        match lhs.py_floordiv(rhs, this.heap) {
            Ok(Some(v)) => {
                this.push(v);
                Ok(())
            }
            Ok(None) => {
                let lhs_type = lhs.py_type(this.heap);
                let rhs_type = rhs.py_type(this.heap);
                Err(ExcType::binary_type_error("//", lhs_type, rhs_type))
            }
            Err(e) => Err(e),
        }
    }

    /// Binary modulo with proper refcount handling.
    ///
    /// Uses lazy type capture: only calls `py_type()` in error paths.
    pub(super) fn binary_mod(&mut self) -> Result<(), RunError> {
        let this = self;

        let rhs = this.pop();
        defer_drop!(rhs, this);
        let lhs = this.pop();
        defer_drop!(lhs, this);

        match lhs.py_mod(rhs, this.heap) {
            Ok(Some(v)) => {
                this.push(v);
                Ok(())
            }
            Ok(None) => {
                let lhs_type = lhs.py_type(this.heap);
                let rhs_type = rhs.py_type(this.heap);
                Err(ExcType::binary_type_error("%", lhs_type, rhs_type))
            }
            Err(e) => Err(e),
        }
    }

    /// Binary power with proper refcount handling.
    ///
    /// Uses lazy type capture: only calls `py_type()` in error paths.
    #[inline(never)]
    pub(super) fn binary_pow(&mut self) -> Result<(), RunError> {
        let this = self;

        let rhs = this.pop();
        defer_drop!(rhs, this);
        let lhs = this.pop();
        defer_drop!(lhs, this);

        match lhs.py_pow(rhs, this.heap) {
            Ok(Some(v)) => {
                this.push(v);
                Ok(())
            }
            Ok(None) => {
                let lhs_type = lhs.py_type(this.heap);
                let rhs_type = rhs.py_type(this.heap);
                Err(ExcType::binary_type_error("** or pow()", lhs_type, rhs_type))
            }
            Err(e) => Err(e),
        }
    }

    /// Binary bitwise operation on integers and sets.
    ///
    /// For integers, performs standard bitwise operations (AND, OR, XOR, shifts).
    /// For sets/frozensets, `|` maps to union, `&` to intersection, and `^` to
    /// symmetric difference. Set operations are handled here because `py_bitwise`
    /// doesn't have access to `interns`, which set operations need for hashing.
    pub(super) fn binary_bitwise(&mut self, op: BitwiseOp) -> Result<(), RunError> {
        let this = self;

        let rhs = this.pop();
        defer_drop!(rhs, this);
        let lhs = this.pop();
        defer_drop!(lhs, this);

        // Set/frozenset operations: |, &, ^ map to union, intersection,
        // symmetric_difference. Shifts don't apply to sets.
        if let (Value::Ref(lhs_id), Value::Ref(rhs_id)) = (lhs, rhs) {
            let set_op = match op {
                BitwiseOp::Or => Some(SetBinaryOp::Union),
                BitwiseOp::And => Some(SetBinaryOp::Intersection),
                BitwiseOp::Xor => Some(SetBinaryOp::SymmetricDifference),
                BitwiseOp::LShift | BitwiseOp::RShift => None,
            };
            if let Some(set_op) = set_op {
                let interns = this.interns;
                if let Some(result) = binary_set_op(set_op, *lhs_id, *rhs_id, this.heap, interns)? {
                    this.push(result);
                    return Ok(());
                }
            }
        }

        let result = lhs.py_bitwise(rhs, op, this.heap)?;
        this.push(result);
        Ok(())
    }

    /// In-place addition (uses py_iadd for mutable containers, falls back to py_add).
    ///
    /// For mutable types like lists, `py_iadd` mutates in place and returns true.
    /// For immutable types, we fall back to regular addition.
    ///
    /// Uses lazy type capture: only calls `py_type()` in error paths.
    ///
    /// Note: Cannot use `defer_drop!` for `lhs` here because on successful in-place
    /// operation, we need to push `lhs` back onto the stack rather than drop it.
    pub(super) fn inplace_add(&mut self) -> Result<(), RunError> {
        let this = self;

        let rhs = this.pop();
        defer_drop!(rhs, this);
        // Use HeapGuard because inplace addition will push lhs back on the stack if successful
        let mut lhs_guard = HeapGuard::new(this.pop(), this);
        let (lhs, this) = lhs_guard.as_parts_mut();

        // Try in-place operation first (for mutable types like lists)
        if lhs.py_iadd(rhs.clone_with_heap(this.heap), this.heap, lhs.ref_id(), this.interns)? {
            // In-place operation succeeded - push lhs back
            let (lhs, this) = lhs_guard.into_parts();
            this.push(lhs);
            return Ok(());
        }

        // Next try regular addition
        if let Some(v) = lhs.py_add(rhs, this.heap, this.interns)? {
            this.push(v);
            return Ok(());
        }

        let lhs_type = lhs.py_type(this.heap);
        let rhs_type = rhs.py_type(this.heap);
        Err(ExcType::binary_type_error("+=", lhs_type, rhs_type))
    }

    /// Binary matrix multiplication (`@` operator).
    ///
    /// Currently not implemented - returns a `NotImplementedError`.
    /// Matrix multiplication requires numpy-like array types which Monty doesn't support.
    pub(super) fn binary_matmul(&mut self) -> Result<(), RunError> {
        let rhs = self.pop();
        let lhs = self.pop();
        lhs.drop_with_heap(self.heap);
        rhs.drop_with_heap(self.heap);
        Err(ExcType::not_implemented("matrix multiplication (@) is not supported").into())
    }
}
