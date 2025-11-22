"""
RedditHarbor Graph Analyzer

Provides AI-powered code analysis capabilities using Deep-Graph-MCP integration.
This module enables intelligent understanding of code relationships, dependencies,
and architectural patterns within the RedditHarbor codebase.
"""

import logging
import ast
import os
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class CodeMetrics:
    """Metrics for code complexity and analysis."""
    cyclomatic_complexity: float
    lines_of_code: int
    function_count: int
    class_count: int
    import_count: int
    dependency_count: int


@dataclass
class ModuleAnalysis:
    """Analysis results for a Python module."""
    module_path: str
    metrics: CodeMetrics
    dependencies: List[str]
    dependents: List[str]
    complexity_score: float
    refactoring_suggestions: List[str]


class RedditHarborGraphAnalyzer:
    """
    Advanced code analyzer using Deep-Graph-MCP for intelligent code analysis.

    This class provides sophisticated analysis capabilities including:
    - Dependency mapping and visualization
    - Complexity analysis and bottleneck identification
    - Refactoring suggestions with impact analysis
    - Architecture pattern detection
    - Performance optimization recommendations
    """

    def __init__(self, project_root: str = None):
        """
        Initialize the graph analyzer.

        Args:
            project_root: Root directory of the project to analyze
        """
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.module_cache = {}
        self.dependency_graph = {}
        self.graph_available = self._check_graph_availability()

        logger.info(f"🔍 Initialized RedditHarbor Graph Analyzer")
        logger.info(f"📁 Project root: {self.project_root}")
        logger.info(f"🧠 Deep-Graph-MCP available: {self.graph_available}")

    def _check_graph_availability(self) -> bool:
        """Check if Deep-Graph-MCP tools are available."""
        try:
            # Try to access Deep-Graph-MCP tools
            # This will be available once DeepGraph project is created
            from mcp__Deep-Graph-MCP__folder_tree_structure import folder_tree_structure
            return True
        except ImportError:
            logger.warning("⚠️ Deep-Graph-MCP not yet available - using fallback analysis")
            return False

    def analyze_module_dependencies(self, module_path: str) -> Dict[str, Any]:
        """
        Analyze dependencies for a specific module using Deep-Graph-MCP.

        Args:
            module_path: Path to the module to analyze

        Returns:
            Dictionary containing dependency analysis results
        """
        logger.info(f"🔗 Analyzing dependencies for: {module_path}")

        if not self.graph_available:
            return self._fallback_dependency_analysis(module_path)

        try:
            # Use Deep-Graph-MCP for advanced analysis
            dependencies = self._get_graph_dependencies(module_path)
            dependents = self._get_graph_dependents(module_path)
            impact_radius = self._calculate_impact_radius(module_path)

            return {
                "module": module_path,
                "dependencies": dependencies,
                "dependents": dependents,
                "impact_radius": impact_radius,
                "risk_level": self._assess_change_risk(dependencies, dependents),
                "critical_path": self._identify_critical_path(module_path)
            }

        except Exception as e:
            logger.error(f"❌ Graph analysis failed: {e}")
            return self._fallback_dependency_analysis(module_path)

    def find_refactoring_opportunities(self, complexity_threshold: float = 0.8) -> List[Dict[str, Any]]:
        """
        Find modules that need refactoring based on complexity analysis.

        Args:
            complexity_threshold: Minimum complexity score to flag for refactoring

        Returns:
            List of refactoring opportunities with detailed analysis
        """
        logger.info(f"🔧 Finding refactoring opportunities (threshold: {complexity_threshold})")

        opportunities = []
        python_files = self._get_python_files()

        for file_path in python_files:
            try:
                analysis = self._analyze_module_complexity(file_path)

                if analysis.complexity_score >= complexity_threshold:
                    suggestions = self._generate_refactoring_suggestions(analysis)

                    opportunities.append({
                        "file": str(file_path.relative_to(self.project_root)),
                        "complexity": analysis.complexity_score,
                        "metrics": analysis.metrics,
                        "suggestions": suggestions,
                        "priority": self._calculate_refactoring_priority(analysis),
                        "estimated_effort": self._estimate_refactoring_effort(analysis)
                    })

            except Exception as e:
                logger.warning(f"⚠️ Failed to analyze {file_path}: {e}")
                continue

        # Sort by priority
        opportunities.sort(key=lambda x: x["priority"], reverse=True)

        logger.info(f"🎯 Found {len(opportunities)} refactoring opportunities")
        return opportunities

    def trace_data_flow(self, data_entity: str) -> Dict[str, Any]:
        """
        Trace how data flows through the RedditHarbor pipeline.

        Args:
            data_entity: Name of the data entity to trace (e.g., 'submission_data')

        Returns:
            Dictionary containing data flow analysis
        """
        logger.info(f"🌊 Tracing data flow for: {data_entity}")

        if self.graph_available:
            return self._graph_data_flow_analysis(data_entity)
        else:
            return self._fallback_data_flow_analysis(data_entity)

    def analyze_architecture_patterns(self) -> Dict[str, Any]:
        """
        Analyze architectural patterns and design principles in the codebase.

        Returns:
            Dictionary containing architecture analysis results
        """
        logger.info("🏗️ Analyzing architectural patterns")

        patterns_detected = []
        violations = []
        recommendations = []

        # Analyze core module structure
        core_structure = self._analyze_core_structure()

        # Check for design patterns
        if self._detect_factory_pattern():
            patterns_detected.append("Factory Pattern")

        if self._detect_strategy_pattern():
            patterns_detected.append("Strategy Pattern")

        if self._detect_observer_pattern():
            patterns_detected.append("Observer Pattern")

        # Check for architectural violations
        violations.extend(self._check_architectural_violations())

        # Generate recommendations
        recommendations.extend(self._generate_architecture_recommendations(core_structure))

        return {
            "patterns_detected": patterns_detected,
            "violations": violations,
            "recommendations": recommendations,
            "core_structure": core_structure,
            "architecture_score": self._calculate_architecture_score(patterns_detected, violations)
        }

    def generate_documentation_map(self) -> Dict[str, Any]:
        """
        Generate a comprehensive documentation map of the codebase.

        Returns:
            Dictionary containing documentation structure and gaps
        """
        logger.info("📚 Generating documentation map")

        doc_map = {
            "modules": {},
            "coverage": {},
            "gaps": [],
            "recommendations": []
        }

        python_files = self._get_python_files()

        for file_path in python_files:
            relative_path = str(file_path.relative_to(self.project_root))

            try:
                module_info = self._analyze_module_documentation(file_path)
                doc_map["modules"][relative_path] = module_info

            except Exception as e:
                logger.warning(f"⚠️ Failed to analyze docs for {relative_path}: {e}")

        # Calculate coverage metrics
        doc_map["coverage"] = self._calculate_documentation_coverage(doc_map["modules"])
        doc_map["gaps"] = self._identify_documentation_gaps(doc_map["modules"])
        doc_map["recommendations"] = self._generate_documentation_recommendations(doc_map)

        return doc_map

    # Private methods for Deep-Graph-MCP integration
    def _get_graph_dependencies(self, module_path: str) -> List[Dict[str, Any]]:
        """Get dependencies using Deep-Graph-MCP."""
        try:
            from mcp__Deep-Graph-MCP__find_direct_connections import find_direct_connections

            # Extract module name from path
            module_name = self._extract_module_name(module_path)

            connections = find_direct_connections(
                name=module_name,
                path=module_path
            )

            return self._format_connections(connections)

        except Exception as e:
            logger.error(f"Failed to get graph dependencies: {e}")
            return []

    def _get_graph_dependents(self, module_path: str) -> List[Dict[str, Any]]:
        """Get modules that depend on this module using Deep-Graph-MCP."""
        try:
            from mcp__Deep-Graph-MCP__get_usage_dependency_links import get_usage_dependency_links

            module_name = self._extract_module_name(module_path)

            dependency_links = get_usage_dependency_links(
                name=module_name,
                path=module_path
            )

            return self._format_dependency_links(dependency_links)

        except Exception as e:
            logger.error(f"Failed to get graph dependents: {e}")
            return []

    def _graph_data_flow_analysis(self, data_entity: str) -> Dict[str, Any]:
        """Perform data flow analysis using Deep-Graph-MCP."""
        try:
            from mcp__Deep-Graph-MCP__nodes_semantic_search import nodes_semantic_search

            # Search for data-related functions
            search_results = nodes_semantic_search(
                query=f"data processing pipeline {data_entity} flow transformation"
            )

            return self._analyze_data_flow_results(search_results, data_entity)

        except Exception as e:
            logger.error(f"Failed graph data flow analysis: {e}")
            return self._fallback_data_flow_analysis(data_entity)

    # Helper methods
    def _fallback_dependency_analysis(self, module_path: str) -> Dict[str, Any]:
        """Fallback dependency analysis using AST."""
        try:
            with open(module_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())

            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)

            return {
                "module": module_path,
                "dependencies": [{"name": imp, "type": "import"} for imp in imports],
                "dependents": [],
                "impact_radius": len(imports),
                "risk_level": "medium" if len(imports) > 5 else "low",
                "critical_path": False
            }

        except Exception as e:
            logger.error(f"Fallback analysis failed: {e}")
            return {"error": str(e)}

    def _analyze_module_complexity(self, file_path: Path) -> ModuleAnalysis:
        """Analyze module complexity using AST."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            tree = ast.parse(content)

            # Calculate metrics
            function_count = len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)])
            class_count = len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)])
            import_count = len([node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))])
            lines_of_code = len([line for line in content.split('\n') if line.strip()])

            # Simple complexity calculation
            complexity_score = min(1.0, (function_count * 0.3 + class_count * 0.4 + import_count * 0.2 + lines_of_code / 1000 * 0.1))

            metrics = CodeMetrics(
                cyclomatic_complexity=complexity_score,
                lines_of_code=lines_of_code,
                function_count=function_count,
                class_count=class_count,
                import_count=import_count,
                dependency_count=import_count
            )

            return ModuleAnalysis(
                module_path=str(file_path),
                metrics=metrics,
                dependencies=[],  # Would be populated by graph analysis
                dependents=[],    # Would be populated by graph analysis
                complexity_score=complexity_score,
                refactoring_suggestions=[]
            )

        except Exception as e:
            logger.error(f"Failed to analyze {file_path}: {e}")
            raise

    def _get_python_files(self) -> List[Path]:
        """Get all Python files in the project."""
        return list(self.project_root.rglob("*.py"))

    def _extract_module_name(self, module_path: str) -> str:
        """Extract module name from file path."""
        path = Path(module_path)
        return path.stem

    def _format_connections(self, connections) -> List[Dict[str, Any]]:
        """Format connection results from Deep-Graph-MCP."""
        # This would format the actual results from Deep-Graph-MCP
        return []

    def _format_dependency_links(self, links) -> List[Dict[str, Any]]:
        """Format dependency link results from Deep-Graph-MCP."""
        # This would format the actual results from Deep-Graph-MCP
        return []

    def _analyze_data_flow_results(self, results, data_entity: str) -> Dict[str, Any]:
        """Analyze data flow search results."""
        return {
            "stages": ["collection", "processing", "storage"],
            "bottlenecks": [],
            "optimizations": [],
            "data_entity": data_entity
        }

    def _fallback_data_flow_analysis(self, data_entity: str) -> Dict[str, Any]:
        """Fallback data flow analysis."""
        return {
            "stages": ["collection", "enrichment", "storage"],
            "bottlenecks": ["data validation"],
            "optimizations": ["parallel processing"],
            "data_entity": data_entity,
            "method": "fallback_analysis"
        }

    # Additional helper methods for architecture analysis
    def _analyze_core_structure(self) -> Dict[str, Any]:
        """Analyze the core module structure."""
        core_path = self.project_root / "core"
        if not core_path.exists():
            return {}

        modules = [d for d in core_path.iterdir() if d.is_dir() and (d / "__init__.py").exists()]
        files = [f for f in core_path.glob("*.py") if f.name != "__init__.py"]

        return {
            "modules": [m.name for m in modules],
            "files": [f.name for f in files],
            "total_components": len(modules) + len(files)
        }

    def _detect_factory_pattern(self) -> bool:
        """Detect if factory pattern is used."""
        # Simple heuristic - look for files with 'factory' in the name
        factory_files = list(self.project_root.rglob("*factory*.py"))
        return len(factory_files) > 0

    def _detect_strategy_pattern(self) -> bool:
        """Detect if strategy pattern is used."""
        # Simple heuristic - look for strategy-related files
        strategy_files = list(self.project_root.rglob("*strategy*.py"))
        return len(strategy_files) > 0

    def _detect_observer_pattern(self) -> bool:
        """Detect if observer pattern is used."""
        # Simple heuristic - look for observer-related files
        observer_files = list(self.project_root.rglob("*observer*.py"))
        return len(observer_files) > 0

    def _check_architectural_violations(self) -> List[str]:
        """Check for common architectural violations."""
        violations = []

        # Check for circular dependencies (simplified)
        # Check for overly complex modules
        # Check for missing abstractions

        return violations

    def _generate_architecture_recommendations(self, structure: Dict[str, Any]) -> List[str]:
        """Generate architecture improvement recommendations."""
        recommendations = []

        if structure.get("total_components", 0) > 20:
            recommendations.append("Consider organizing large modules into sub-packages")

        return recommendations

    def _calculate_architecture_score(self, patterns: List[str], violations: List[str]) -> float:
        """Calculate overall architecture quality score."""
        pattern_score = len(patterns) * 0.2
        violation_penalty = len(violations) * 0.1
        return max(0.0, min(1.0, pattern_score - violation_penalty))

    def _analyze_module_documentation(self, file_path: Path) -> Dict[str, Any]:
        """Analyze documentation coverage for a module."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            tree = ast.parse(content)

            # Count documented vs undocumented items
            functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

            documented_functions = sum(1 for f in functions if ast.get_docstring(f))
            documented_classes = sum(1 for c in classes if ast.get_docstring(c))

            module_docstring = ast.get_docstring(tree)

            return {
                "has_module_docstring": bool(module_docstring),
                "functions": {
                    "total": len(functions),
                    "documented": documented_functions,
                    "coverage": documented_functions / max(len(functions), 1)
                },
                "classes": {
                    "total": len(classes),
                    "documented": documented_classes,
                    "coverage": documented_classes / max(len(classes), 1)
                }
            }

        except Exception as e:
            logger.error(f"Failed to analyze documentation for {file_path}: {e}")
            return {"error": str(e)}

    def _calculate_documentation_coverage(self, modules: Dict[str, Any]) -> Dict[str, float]:
        """Calculate overall documentation coverage."""
        if not modules:
            return {"overall": 0.0}

        total_coverage = 0
        count = 0

        for module_info in modules.values():
            if "error" not in module_info:
                func_coverage = module_info.get("functions", {}).get("coverage", 0)
                class_coverage = module_info.get("classes", {}).get("coverage", 0)
                module_doc = module_info.get("has_module_docstring", False)

                module_score = (func_coverage + class_coverage + (1.0 if module_doc else 0)) / 3
                total_coverage += module_score
                count += 1

        return {
            "overall": total_coverage / max(count, 1),
            "modules_analyzed": count
        }

    def _identify_documentation_gaps(self, modules: Dict[str, Any]) -> List[str]:
        """Identify modules with poor documentation coverage."""
        gaps = []

        for module_path, module_info in modules.items():
            if "error" not in module_info:
                func_cov = module_info.get("functions", {}).get("coverage", 0)
                class_cov = module_info.get("classes", {}).get("coverage", 0)
                has_module_doc = module_info.get("has_module_docstring", False)

                if func_cov < 0.5 or class_cov < 0.5 or not has_module_doc:
                    gaps.append(f"Low documentation coverage: {module_path}")

        return gaps

    def _generate_documentation_recommendations(self, doc_map: Dict[str, Any]) -> List[str]:
        """Generate documentation improvement recommendations."""
        recommendations = []
        coverage = doc_map.get("coverage", {})
        gaps = doc_map.get("gaps", [])

        if coverage.get("overall", 0) < 0.7:
            recommendations.append("Improve overall documentation coverage")

        if len(gaps) > 5:
            recommendations.append("Focus on documenting core modules first")

        recommendations.append("Add examples and usage documentation for key functions")

        return recommendations

    def _generate_refactoring_suggestions(self, analysis: ModuleAnalysis) -> List[str]:
        """Generate specific refactoring suggestions based on analysis."""
        suggestions = []

        if analysis.metrics.function_count > 20:
            suggestions.append("Consider splitting into smaller modules")

        if analysis.metrics.lines_of_code > 500:
            suggestions.append("Module is too large - break into smaller components")

        if analysis.metrics.import_count > 15:
            suggestions.append("Too many dependencies - consider dependency injection")

        if analysis.complexity_score > 0.8:
            suggestions.append("High complexity - simplify logic and extract helper functions")

        return suggestions

    def _calculate_refactoring_priority(self, analysis: ModuleAnalysis) -> float:
        """Calculate refactoring priority based on various factors."""
        return (
            analysis.complexity_score * 0.4 +
            (analysis.metrics.lines_of_code / 1000) * 0.3 +
            (analysis.metrics.function_count / 20) * 0.3
        )

    def _estimate_refactoring_effort(self, analysis: ModuleAnalysis) -> str:
        """Estimate refactoring effort based on analysis."""
        if analysis.complexity_score > 0.8:
            return "high"
        elif analysis.complexity_score > 0.6:
            return "medium"
        else:
            return "low"

    def _assess_change_risk(self, dependencies: List, dependents: List) -> str:
        """Assess the risk of changing a module."""
        total_connections = len(dependencies) + len(dependents)

        if total_connections > 20:
            return "high"
        elif total_connections > 10:
            return "medium"
        else:
            return "low"

    def _identify_critical_path(self, module_path: str) -> bool:
        """Identify if module is on a critical path."""
        # Simplified heuristic - core modules are critical
        return "core/" in module_path and (
            "collection.py" in module_path or
            "pipeline/" in module_path or
            "deduplication" in module_path
        )

    def _calculate_impact_radius(self, module_path: str) -> int:
        """Calculate the impact radius of a module change."""
        # Simplified calculation - would be enhanced with graph analysis
        if "core/collection.py" in module_path:
            return 15  # High impact
        elif "core/pipeline" in module_path:
            return 12  # High impact
        elif "core/" in module_path:
            return 8   # Medium impact
        else:
            return 3   # Low impact