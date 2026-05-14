"""
Install-level integration tests.

These tests verify that all documented import paths resolve correctly
and that __all__ exports match actual module contents. They catch
packaging and __init__.py wiring issues that unit tests miss because
unit tests import from deep paths within the source tree.
"""

import importlib
import pytest

import panchi
import panchi.primitives
import panchi.algorithms
import panchi.visualizations


class TestTopLevelImports:
    """Every symbol in panchi.__all__ must be importable from panchi."""

    @pytest.mark.parametrize("name", panchi.__all__)
    def test_top_level_export(self, name):
        assert hasattr(panchi, name), f"panchi.{name} not accessible"


class TestPrimitivesImports:
    """Every symbol in panchi.primitives.__all__ must be importable."""

    @pytest.mark.parametrize("name", panchi.primitives.__all__)
    def test_primitives_export(self, name):
        assert hasattr(panchi.primitives, name), f"panchi.primitives.{name} not accessible"


class TestAlgorithmsImports:
    """Every symbol in panchi.algorithms.__all__ must be importable."""

    @pytest.mark.parametrize("name", panchi.algorithms.__all__)
    def test_algorithms_export(self, name):
        assert hasattr(panchi.algorithms, name), f"panchi.algorithms.{name} not accessible"


class TestSubpackageImportPaths:
    """Test the documented import paths users would actually write."""

    def test_from_panchi_import_vector(self):
        from panchi import Vector
        assert Vector is not None

    def test_from_panchi_import_matrix(self):
        from panchi import Matrix
        assert Matrix is not None

    def test_from_panchi_import_vector_space(self):
        from panchi import VectorSpace
        assert VectorSpace is not None

    def test_from_primitives_import_vector(self):
        from panchi.primitives import Vector
        assert Vector is not None

    def test_from_primitives_import_matrix(self):
        from panchi.primitives import Matrix
        assert Matrix is not None

    def test_from_primitives_import_vector_space(self):
        from panchi.primitives import VectorSpace
        assert VectorSpace is not None

    def test_from_primitives_import_factories(self):
        from panchi.primitives import identity, zero_matrix, zero_vector
        assert all(callable(f) for f in [identity, zero_matrix, zero_vector])

    def test_from_algorithms_import_reductions(self):
        from panchi.algorithms import ref, rref
        assert all(callable(f) for f in [ref, rref])

    def test_from_algorithms_import_decompositions(self):
        from panchi.algorithms import lu
        assert callable(lu)

    def test_from_algorithms_import_solvers(self):
        from panchi.algorithms import inverse, solve, determinant_lu
        assert all(callable(f) for f in [inverse, solve, determinant_lu])

    def test_from_algorithms_import_vector_ops(self):
        from panchi.algorithms import dot, cross, orthogonal_complement
        assert all(callable(f) for f in [dot, cross, orthogonal_complement])

    def test_from_algorithms_import_row_operations(self):
        from panchi.algorithms import RowSwap, RowScale, RowAdd
        assert all(f is not None for f in [RowSwap, RowScale, RowAdd])

    def test_from_algorithms_import_result_types(self):
        from panchi.algorithms import LUDecomposition, InverseResult, Solution
        assert all(f is not None for f in [LUDecomposition, InverseResult, Solution])


class TestDeepImportPaths:
    """Test that deep (module-level) imports still work."""

    def test_deep_vector(self):
        from panchi.primitives.vector import Vector
        assert Vector is not None

    def test_deep_matrix(self):
        from panchi.primitives.matrix import Matrix
        assert Matrix is not None

    def test_deep_vector_space(self):
        from panchi.primitives.vector_space import VectorSpace
        assert VectorSpace is not None

    def test_deep_factories(self):
        from panchi.primitives.factories import identity, zero_matrix
        assert all(callable(f) for f in [identity, zero_matrix])

    def test_deep_row_operations(self):
        from panchi.algorithms.row_operations import RowSwap, RowScale, RowAdd
        assert all(f is not None for f in [RowSwap, RowScale, RowAdd])

    def test_deep_reductions(self):
        from panchi.algorithms.reductions import ref, rref
        assert all(callable(f) for f in [ref, rref])

    def test_deep_decompositions(self):
        from panchi.algorithms.decompositions import lu
        assert callable(lu)

    def test_deep_matrix_operations(self):
        from panchi.algorithms.matrix_operations import inverse, solve, determinant_lu
        assert all(callable(f) for f in [inverse, solve, determinant_lu])

    def test_deep_vector_operations(self):
        from panchi.algorithms.vector_operations import dot, cross, orthogonal_complement
        assert all(callable(f) for f in [dot, cross, orthogonal_complement])

    def test_deep_results(self):
        from panchi.algorithms.results import LUDecomposition, InverseResult, Solution
        assert all(f is not None for f in [LUDecomposition, InverseResult, Solution])


class TestVisualizationsImport:
    """Visualizations module must import without crashing, even without manim."""

    def test_visualizations_importable(self):
        mod = importlib.import_module("panchi.visualizations")
        assert mod is not None

    def test_matplotlib_backend_importable(self):
        from panchi.visualizations.backends import matplotlib_2d
        assert matplotlib_2d is not None


class TestVersionAndMetadata:
    """Package metadata must be present and well-formed."""

    def test_version_exists(self):
        assert hasattr(panchi, "__version__")
        assert isinstance(panchi.__version__, str)
        assert len(panchi.__version__) > 0

    def test_version_matches_pep440(self):
        from packaging.version import Version
        Version(panchi.__version__)

    def test_all_is_list_of_strings(self):
        assert isinstance(panchi.__all__, list)
        assert all(isinstance(name, str) for name in panchi.__all__)


class TestAllConsistency:
    """__all__ must match what's actually importable — no ghosts, no gaps."""

    def test_top_level_all_no_extras(self):
        for name in panchi.__all__:
            obj = getattr(panchi, name, None)
            assert obj is not None, f"panchi.__all__ lists '{name}' but it's None"

    def test_primitives_all_no_extras(self):
        for name in panchi.primitives.__all__:
            obj = getattr(panchi.primitives, name, None)
            assert obj is not None, f"panchi.primitives.__all__ lists '{name}' but it's None"

    def test_algorithms_all_no_extras(self):
        for name in panchi.algorithms.__all__:
            obj = getattr(panchi.algorithms, name, None)
            assert obj is not None, f"panchi.algorithms.__all__ lists '{name}' but it's None"
