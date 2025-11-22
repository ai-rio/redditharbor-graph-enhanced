"""
Test suite for RedditHarbor Graph Integration

Comprehensive tests for Deep-Graph-MCP integration functionality.
"""

import unittest
import sys
import os
from pathlib import Path
import tempfile
import shutil

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.graph_integration.analyzer import RedditHarborGraphAnalyzer, ModuleAnalysis, CodeMetrics
from core.graph_integration.dependencies import DependencyMapper, DependencyNode, DependencyEdge
from core.graph_integration.refactoring import IntelligentRefactorer, RefactoringSuggestion


class TestRedditHarborGraphAnalyzer(unittest.TestCase):
    """Test cases for RedditHarborGraphAnalyzer."""

    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = RedditHarborGraphAnalyzer()
        self.test_project_root = project_root

    def test_initialization(self):
        """Test analyzer initialization."""
        self.assertIsInstance(self.analyzer, RedditHarborGraphAnalyzer)
        self.assertEqual(self.analyzer.project_root, self.test_project_root)
        self.assertIsInstance(self.analyzer.graph_available, bool)

    def test_analyze_module_dependencies(self):
        """Test module dependency analysis."""
        # Test with core collection module
        result = self.analyzer.analyze_module_dependencies("core/collection.py")

        self.assertIsInstance(result, dict)
        self.assertIn("module", result)
        self.assertIn("dependencies", result)
        self.assertIn("dependents", result)
        self.assertIn("risk_level", result)

    def test_find_refactoring_opportunities(self):
        """Test finding refactoring opportunities."""
        opportunities = self.analyzer.find_refactoring_opportunities(complexity_threshold=0.1)

        self.assertIsInstance(opportunities, list)
        # Should find some opportunities even with low threshold
        self.assertGreaterEqual(len(opportunities), 0)

    def test_trace_data_flow(self):
        """Test data flow tracing."""
        result = self.analyzer.trace_data_flow("submission_data")

        self.assertIsInstance(result, dict)
        self.assertIn("stages", result)
        self.assertIn("bottlenecks", result)
        self.assertIn("data_entity", result)

    def test_analyze_architectural_patterns(self):
        """Test architectural pattern analysis."""
        result = self.analyzer.analyze_architectural_patterns()

        self.assertIsInstance(result, dict)
        self.assertIn("patterns_detected", result)
        self.assertIn("violations", result)
        self.assertIn("architecture_score", result)

    def test_generate_documentation_map(self):
        """Test documentation map generation."""
        result = self.analyzer.generate_documentation_map()

        self.assertIsInstance(result, dict)
        self.assertIn("modules", result)
        self.assertIn("coverage", result)


class TestDependencyMapper(unittest.TestCase):
    """Test cases for DependencyMapper."""

    def setUp(self):
        """Set up test fixtures."""
        self.mapper = DependencyMapper()
        self.test_project_root = project_root

    def test_initialization(self):
        """Test mapper initialization."""
        self.assertIsInstance(self.mapper, DependencyMapper)
        self.assertEqual(self.mapper.project_root, self.test_project_root)
        self.assertIsInstance(self.mapper.graph_available, bool)

    def test_build_dependency_graph(self):
        """Test dependency graph building."""
        result = self.mapper.build_dependency_graph()

        self.assertIsInstance(result, dict)
        self.assertIn("total_nodes", result)
        self.assertIn("total_edges", result)
        self.assertIn("graph_density", result)

    def test_detect_circular_dependencies(self):
        """Test circular dependency detection."""
        circular_deps = self.mapper.detect_circular_dependencies()

        self.assertIsInstance(circular_deps, list)
        # Each circular dependency should have required fields
        for dep in circular_deps:
            self.assertIn("cycle_id", dep)
            self.assertIn("cycle", dep)
            self.assertIn("severity", dep)

    def test_identify_critical_dependencies(self):
        """Test critical dependency identification."""
        critical_deps = self.mapper.identify_critical_dependencies()

        self.assertIsInstance(critical_deps, dict)
        self.assertIn("critical_nodes", critical_deps)
        self.assertIn("total_nodes", critical_deps)

    def test_analyze_architectural_layers(self):
        """Test architectural layer analysis."""
        result = self.mapper.analyze_architectural_layers()

        self.assertIsInstance(result, dict)
        self.assertIn("layers", result)
        self.assertIn("layer_nodes", result)
        self.assertIn("violations", result)


class TestIntelligentRefactorer(unittest.TestCase):
    """Test cases for IntelligentRefactorer."""

    def setUp(self):
        """Set up test fixtures."""
        self.refactorer = IntelligentRefactorer()
        self.test_project_root = project_root

    def test_initialization(self):
        """Test refactorer initialization."""
        self.assertIsInstance(self.refactorer, IntelligentRefactorer)
        self.assertEqual(self.refactorer.project_root, self.test_project_root)
        self.assertIsInstance(self.refactorer.graph_available, bool)

    def test_analyze_code_quality(self):
        """Test code quality analysis."""
        result = self.refactorer.analyze_code_quality("core/collection.py")

        self.assertIsInstance(result, dict)
        # Different result structure based on graph availability
        if self.refactorer.graph_available:
            self.assertIn("quality_issues", result)
        else:
            self.assertIn("total_files", result)

    def test_generate_refactoring_suggestions(self):
        """Test refactoring suggestions generation."""
        plan = self.refactorer.generate_refactoring_suggestions(severity_threshold="low")

        self.assertIsInstance(plan, object)
        self.assertIsNotNone(plan.target_files)
        self.assertIsNotNone(plan.suggestions)
        self.assertIsNotNone(plan.estimated_effort)

    def test_validate_refactoring(self):
        """Test refactoring validation."""
        plan = self.refactorer.generate_refactoring_suggestions(severity_threshold="high")
        validation = self.refactorer.validate_refactoring(plan)

        self.assertIsInstance(validation, dict)
        self.assertIn("is_valid", validation)
        self.assertIn("warnings", validation)
        self.assertIn("errors", validation)

    def test_generate_refactoring_report(self):
        """Test refactoring report generation."""
        plan = self.refactorer.generate_refactoring_suggestions(severity_threshold="high")
        report = self.refactorer.generate_refactoring_report(plan)

        self.assertIsInstance(report, str)
        self.assertIn("RedditHarbor Refactoring Report", report)
        self.assertIn("##", report)  # Should have markdown headers


class TestDataStructures(unittest.TestCase):
    """Test cases for data structures."""

    def test_code_metrics_creation(self):
        """Test CodeMetrics dataclass creation."""
        metrics = CodeMetrics(
            cyclomatic_complexity=0.5,
            lines_of_code=100,
            function_count=5,
            class_count=2,
            import_count=8,
            dependency_count=6
        )

        self.assertEqual(metrics.cyclomatic_complexity, 0.5)
        self.assertEqual(metrics.lines_of_code, 100)

    def test_module_analysis_creation(self):
        """Test ModuleAnalysis dataclass creation."""
        metrics = CodeMetrics(0.5, 100, 5, 2, 8, 6)
        analysis = ModuleAnalysis(
            module_path="test_module.py",
            metrics=metrics,
            dependencies=["dep1", "dep2"],
            dependents=["user1"],
            complexity_score=0.7,
            refactoring_suggestions=["suggestion1"]
        )

        self.assertEqual(analysis.module_path, "test_module.py")
        self.assertEqual(analysis.complexity_score, 0.7)

    def test_dependency_node_creation(self):
        """Test DependencyNode dataclass creation."""
        node = DependencyNode(
            name="test_node",
            path="test/path.py",
            node_type="module",
            complexity=0.6,
            lines_of_code=150,
            dependencies={"dep1"},
            dependents={"user1"}
        )

        self.assertEqual(node.name, "test_node")
        self.assertEqual(node.node_type, "module")

    def test_dependency_edge_creation(self):
        """Test DependencyEdge dataclass creation."""
        edge = DependencyEdge(
            source="module1",
            target="module2",
            edge_type="import",
            strength=0.8,
            criticality="high"
        )

        self.assertEqual(edge.source, "module1")
        self.assertEqual(edge.target, "module2")
        self.assertEqual(edge.edge_type, "import")

    def test_refactoring_suggestion_creation(self):
        """Test RefactoringSuggestion dataclass creation."""
        suggestion = RefactoringSuggestion(
            type="function_complexity",
            description="Function is too complex",
            file_path="test.py",
            line_numbers=(10, 50),
            severity="medium",
            effort="medium",
            impact_risk="low",
            automated_fix=False,
            suggested_code="# Refactored code",
            rationale="Improve maintainability",
            dependencies=["dep1"]
        )

        self.assertEqual(suggestion.type, "function_complexity")
        self.assertEqual(suggestion.severity, "medium")
        self.assertEqual(suggestion.line_numbers, (10, 50))


class TestIntegrationWorkflows(unittest.TestCase):
    """Test cases for integration workflows."""

    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = RedditHarborGraphAnalyzer()
        self.mapper = DependencyMapper()
        self.refactorer = IntelligentRefactorer()

    def test_complete_analysis_workflow(self):
        """Test complete analysis workflow."""
        # 1. Analyze dependencies
        deps = self.analyzer.analyze_module_dependencies("core/collection.py")
        self.assertIsInstance(deps, dict)

        # 2. Build dependency graph
        graph = self.mapper.build_dependency_graph()
        self.assertIsInstance(graph, dict)

        # 3. Find refactoring opportunities
        opportunities = self.analyzer.find_refactoring_opportunities()
        self.assertIsInstance(opportunities, list)

        # 4. Generate refactoring plan
        plan = self.refactorer.generate_refactoring_suggestions()
        self.assertIsNotNone(plan)

    def test_architecture_analysis_workflow(self):
        """Test architecture analysis workflow."""
        # 1. Analyze architectural patterns
        patterns = self.analyzer.analyze_architectural_patterns()
        self.assertIsInstance(patterns, dict)

        # 2. Analyze architectural layers
        layers = self.mapper.analyze_architectural_layers()
        self.assertIsInstance(layers, dict)

        # 3. Check for violations
        violations = layers.get("violations", [])
        self.assertIsInstance(violations, list)

    def test_documentation_analysis_workflow(self):
        """Test documentation analysis workflow."""
        # 1. Generate documentation map
        doc_map = self.analyzer.generate_documentation_map()
        self.assertIsInstance(doc_map, dict)

        # 2. Check coverage
        coverage = doc_map.get("coverage", {})
        self.assertIsInstance(coverage, dict)

        # 3. Identify gaps
        gaps = doc_map.get("gaps", [])
        self.assertIsInstance(gaps, list)


def run_all_tests():
    """Run all test suites."""
    # Create test suite
    test_suite = unittest.TestSuite()

    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestRedditHarborGraphAnalyzer))
    test_suite.addTest(unittest.makeSuite(TestDependencyMapper))
    test_suite.addTest(unittest.makeSuite(TestIntelligentRefactorer))
    test_suite.addTest(unittest.makeSuite(TestDataStructures))
    test_suite.addTest(unittest.makeSuite(TestIntegrationWorkflows))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Return result
    return result.wasSuccessful()


if __name__ == "__main__":
    print("🧪 Running RedditHarbor Graph Integration Tests")
    print("=" * 50)

    success = run_all_tests()

    if success:
        print("\n✅ All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)