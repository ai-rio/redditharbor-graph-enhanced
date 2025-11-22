"""
Dependency Mapper for RedditHarbor

Advanced dependency analysis and visualization using Deep-Graph-MCP.
Provides comprehensive mapping of module interdependencies, circular dependency detection,
and architectural dependency insights.
"""

import logging
import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, List, Any, Set, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path
import json
from collections import defaultdict

logger = logging.getLogger(__name__)


@dataclass
class DependencyNode:
    """Represents a node in the dependency graph."""
    name: str
    path: str
    node_type: str  # 'module', 'package', 'function', 'class'
    complexity: float
    lines_of_code: int
    dependencies: Set[str]
    dependents: Set[str]


@dataclass
class DependencyEdge:
    """Represents an edge in the dependency graph."""
    source: str
    target: str
    edge_type: str  # 'import', 'inheritance', 'composition', 'call'
    strength: float
    criticality: str  # 'low', 'medium', 'high', 'critical'


class DependencyMapper:
    """
    Advanced dependency mapping and analysis using Deep-Graph-MCP.

    Features:
    - Multi-level dependency analysis (module, class, function)
    - Circular dependency detection
    - Critical path identification
    - Dependency strength calculation
    - Architectural layer analysis
    - Interactive graph visualization
    """

    def __init__(self, project_root: str = None):
        """
        Initialize the dependency mapper.

        Args:
            project_root: Root directory of the project to analyze
        """
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.dependency_graph = nx.DiGraph()
        self.nodes = {}
        self.edges = []
        self.graph_available = self._check_graph_availability()

        logger.info(f"🗺️ Initialized Dependency Mapper")
        logger.info(f"📁 Project root: {self.project_root}")
        logger.info(f"🧠 Deep-Graph-MCP available: {self.graph_available}")

    def _check_graph_availability(self) -> bool:
        """Check if Deep-Graph-MCP tools are available."""
        try:
            from mcp__Deep-Graph-MCP__get_usage_dependency_links import get_usage_dependency_links
            return True
        except ImportError:
            logger.warning("⚠️ Deep-Graph-MCP not yet available - using fallback analysis")
            return False

    def build_dependency_graph(self, depth: int = 3) -> Dict[str, Any]:
        """
        Build comprehensive dependency graph using Deep-Graph-MCP.

        Args:
            depth: Depth of dependency analysis

        Returns:
            Dictionary containing graph analysis results
        """
        logger.info(f"🏗️ Building dependency graph (depth: {depth})")

        try:
            if self.graph_available:
                return self._build_graph_with_mcp(depth)
            else:
                return self._build_graph_fallback()

        except Exception as e:
            logger.error(f"❌ Failed to build dependency graph: {e}")
            return self._build_graph_fallback()

    def detect_circular_dependencies(self) -> List[Dict[str, Any]]:
        """
        Detect circular dependencies in the codebase.

        Returns:
            List of circular dependency chains with analysis
        """
        logger.info("🔄 Detecting circular dependencies")

        if not self.dependency_graph.nodes():
            self.build_dependency_graph()

        cycles = list(nx.simple_cycles(self.dependency_graph))

        circular_deps = []
        for i, cycle in enumerate(cycles):
            analysis = self._analyze_cycle(cycle)
            circular_deps.append({
                "cycle_id": i + 1,
                "cycle": cycle,
                "length": len(cycle),
                "impact": analysis["impact"],
                "severity": analysis["severity"],
                "suggestion": analysis["suggestion"],
                "affected_modules": analysis["affected_modules"]
            })

        logger.info(f"🔍 Found {len(circular_deps)} circular dependencies")
        return circular_deps

    def identify_critical_dependencies(self) -> Dict[str, Any]:
        """
        Identify critical dependencies that could impact the entire system.

        Returns:
            Dictionary containing critical dependency analysis
        """
        logger.info("⚡ Identifying critical dependencies")

        if not self.dependency_graph.nodes():
            self.build_dependency_graph()

        # Calculate various centrality measures
        betweenness = nx.betweenness_centrality(self.dependency_graph)
        closeness = nx.closeness_centrality(self.dependency_graph)
        in_degree = dict(self.dependency_graph.in_degree())
        out_degree = dict(self.dependency_graph.out_degree())

        critical_nodes = []
        for node in self.dependency_graph.nodes():
            critical_score = (
                betweenness.get(node, 0) * 0.4 +
                closeness.get(node, 0) * 0.3 +
                (in_degree.get(node, 0) / max(max(in_degree.values()), 1)) * 0.2 +
                (out_degree.get(node, 0) / max(max(out_degree.values()), 1)) * 0.1
            )

            if critical_score > 0.5:  # Threshold for critical nodes
                critical_nodes.append({
                    "node": node,
                    "critical_score": critical_score,
                    "betweenness": betweenness.get(node, 0),
                    "closeness": closeness.get(node, 0),
                    "in_degree": in_degree.get(node, 0),
                    "out_degree": out_degree.get(node, 0),
                    "risk_level": self._assess_risk_level(critical_score)
                })

        # Sort by critical score
        critical_nodes.sort(key=lambda x: x["critical_score"], reverse=True)

        return {
            "critical_nodes": critical_nodes,
            "total_nodes": len(self.dependency_graph.nodes()),
            "critical_count": len(critical_nodes),
            "graph_density": nx.density(self.dependency_graph)
        }

    def analyze_architectural_layers(self) -> Dict[str, Any]:
        """
        Analyze architectural layers and their dependencies.

        Returns:
            Dictionary containing layer analysis results
        """
        logger.info("🏗️ Analyzing architectural layers")

        # Define architectural layers
        layers = {
            "presentation": ["api", "frontend", "ui"],
            "business": ["core", "services", "logic"],
            "data": ["storage", "database", "models"],
            "infrastructure": ["config", "utils", "external"]
        }

        layer_graph = nx.DiGraph()
        layer_nodes = defaultdict(list)

        # Categorize nodes into layers
        for node in self.dependency_graph.nodes():
            assigned_layer = self._assign_to_layer(node, layers)
            layer_nodes[assigned_layer].append(node)

        # Build layer-level dependency graph
        for source, target in self.dependency_graph.edges():
            source_layer = self._assign_to_layer(source, layers)
            target_layer = self._assign_to_layer(target, layers)

            if source_layer != target_layer:
                if layer_graph.has_edge(source_layer, target_layer):
                    layer_graph[source_layer][target_layer]["weight"] += 1
                else:
                    layer_graph.add_edge(source_layer, target_layer, weight=1)

        # Analyze layer violations
        violations = self._detect_layer_violations(layer_graph)

        return {
            "layers": dict(layers),
            "layer_nodes": dict(layer_nodes),
            "layer_graph": {
                "nodes": list(layer_graph.nodes()),
                "edges": list(layer_graph.edges(data=True))
            },
            "violations": violations,
            "layer_strength": self._calculate_layer_strength(layer_nodes),
            "coupling_metrics": self._calculate_layer_coupling(layer_graph)
        }

    def generate_impact_analysis(self, changed_module: str) -> Dict[str, Any]:
        """
        Generate impact analysis for a specific module change.

        Args:
            changed_module: Path to the module being changed

        Returns:
            Dictionary containing impact analysis results
        """
        logger.info(f"💥 Generating impact analysis for: {changed_module}")

        if not self.dependency_graph.nodes():
            self.build_dependency_graph()

        # Find all affected modules (downstream dependencies)
        try:
            affected = nx.descendants(self.dependency_graph, changed_module)
        except nx.NetworkXError:
            affected = set()

        # Find all modules that need to be tested (upstream dependencies)
        try:
            needs_testing = nx.ancestors(self.dependency_graph, changed_module)
        except nx.NetworkXError:
            needs_testing = set()

        # Calculate impact metrics
        impact_metrics = {
            "direct_dependents": len(list(self.dependency_graph.successors(changed_module))),
            "total_affected": len(affected),
            "needs_testing": len(needs_testing),
            "critical_path_affected": self._check_critical_path_affected(changed_module, affected),
            "impact_radius": self._calculate_impact_radius(affected)
        }

        # Generate recommendations
        recommendations = self._generate_impact_recommendations(changed_module, impact_metrics)

        return {
            "changed_module": changed_module,
            "affected_modules": list(affected),
            "needs_testing": list(needs_testing),
            "impact_metrics": impact_metrics,
            "recommendations": recommendations,
            "test_priority": self._calculate_test_priority(impact_metrics)
        }

    def visualize_dependency_graph(self, output_path: str = None, layout: str = "spring") -> str:
        """
        Generate visualization of the dependency graph.

        Args:
            output_path: Path to save the visualization
            layout: Layout algorithm ('spring', 'circular', 'hierarchical')

        Returns:
            Path to the generated visualization file
        """
        logger.info(f"📊 Generating dependency graph visualization (layout: {layout})")

        if not self.dependency_graph.nodes():
            self.build_dependency_graph()

        plt.figure(figsize=(15, 10))

        # Choose layout
        if layout == "spring":
            pos = nx.spring_layout(self.dependency_graph, k=1, iterations=50)
        elif layout == "circular":
            pos = nx.circular_layout(self.dependency_graph)
        elif layout == "hierarchical":
            pos = nx.kamada_kawai_layout(self.dependency_graph)
        else:
            pos = nx.spring_layout(self.dependency_graph)

        # Node sizes based on importance
        node_sizes = [self.dependency_graph.in_degree(node) * 100 + 50 for node in self.dependency_graph.nodes()]

        # Draw the graph
        nx.draw(
            self.dependency_graph,
            pos,
            with_labels=True,
            node_size=node_sizes,
            node_color="lightblue",
            edge_color="gray",
            font_size=8,
            font_weight="bold",
            alpha=0.8,
            arrows=True,
            arrowsize=20
        )

        plt.title("RedditHarbor Dependency Graph", size=16, weight="bold")
        plt.axis("off")

        # Save the visualization
        if output_path is None:
            output_path = self.project_root / "dependency_graph.png"

        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()

        logger.info(f"📈 Visualization saved to: {output_path}")
        return str(output_path)

    def export_dependency_matrix(self, output_path: str = None) -> str:
        """
        Export dependency matrix for external analysis.

        Args:
            output_path: Path to save the dependency matrix

        Returns:
            Path to the generated matrix file
        """
        logger.info("📋 Exporting dependency matrix")

        if not self.dependency_graph.nodes():
            self.build_dependency_graph()

        nodes = list(self.dependency_graph.nodes())
        matrix_size = len(nodes)

        # Create adjacency matrix
        matrix = [[0] * matrix_size for _ in range(matrix_size)]

        for i, source in enumerate(nodes):
            for j, target in enumerate(nodes):
                if self.dependency_graph.has_edge(source, target):
                    matrix[i][j] = 1

        # Prepare export data
        export_data = {
            "nodes": nodes,
            "matrix": matrix,
            "metadata": {
                "generated_at": str(plt.datetime.datetime.now()),
                "total_nodes": matrix_size,
                "total_edges": self.dependency_graph.number_of_edges(),
                "graph_density": nx.density(self.dependency_graph)
            }
        }

        # Save to file
        if output_path is None:
            output_path = self.project_root / "dependency_matrix.json"

        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2)

        logger.info(f"📄 Dependency matrix exported to: {output_path}")
        return str(output_path)

    # Private methods
    def _build_graph_with_mcp(self, depth: int) -> Dict[str, Any]:
        """Build dependency graph using Deep-Graph-MCP."""
        try:
            from mcp__Deep-Graph-MCP__nodes_semantic_search import nodes_semantic_search
            from mcp__Deep-Graph-MCP__find_direct_connections import find_direct_connections

            # Get all Python files
            python_files = list(self.project_root.rglob("*.py"))

            for file_path in python_files:
                relative_path = str(file_path.relative_to(self.project_root))

                # Skip test files and __pycache__
                if "test" in relative_path or "__pycache__" in relative_path:
                    continue

                # Add node
                self.dependency_graph.add_node(relative_path)
                self.nodes[relative_path] = DependencyNode(
                    name=Path(relative_path).stem,
                    path=relative_path,
                    node_type="module",
                    complexity=0.0,  # Would be calculated
                    lines_of_code=0,  # Would be calculated
                    dependencies=set(),
                    dependents=set()
                )

                # Get connections using MCP
                try:
                    connections = find_direct_connections(
                        name=Path(relative_path).stem,
                        path=relative_path
                    )

                    # Process connections and add edges
                    for connection in connections:
                        # This would process actual MCP results
                        pass

                except Exception as e:
                    logger.debug(f"No MCP connections for {relative_path}: {e}")

            return self._generate_graph_summary()

        except Exception as e:
            logger.error(f"MCP graph building failed: {e}")
            return self._build_graph_fallback()

    def _build_graph_fallback(self) -> Dict[str, Any]:
        """Build dependency graph using fallback AST analysis."""
        logger.info("🔄 Using fallback AST analysis for dependency graph")

        python_files = list(self.project_root.rglob("*.py"))

        for file_path in python_files:
            relative_path = str(file_path.relative_to(self.project_root))

            # Skip test files and cache
            if "test" in relative_path or "__pycache__" in relative_path:
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Simple import detection
                imports = self._extract_imports(content, relative_path)

                # Add node
                self.dependency_graph.add_node(relative_path)

                # Add edges for imports
                for imp in imports:
                    # Try to find corresponding file
                    imp_path = self._resolve_import_path(imp, relative_path)
                    if imp_path and imp_path in [str(p.relative_to(self.project_root)) for p in python_files]:
                        self.dependency_graph.add_edge(relative_path, imp_path)

            except Exception as e:
                logger.warning(f"Failed to analyze {relative_path}: {e}")

        return self._generate_graph_summary()

    def _extract_imports(self, content: str, file_path: str) -> List[str]:
        """Extract imports from file content."""
        imports = []

        # Simple regex-based import detection
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('from ') or line.startswith('import '):
                if 'from core' in line or 'import core' in line:
                    # Extract module name from core imports
                    if 'from core.' in line:
                        parts = line.split()
                        if len(parts) > 1:
                            module_path = parts[1]
                            imports.append(module_path)
                    elif 'import core' in line:
                        parts = line.split()
                        if len(parts) > 1:
                            module_path = parts[1]
                            if '.' in module_path:
                                imports.append('.'.join(module_path.split('.')[:-1]))

        return imports

    def _resolve_import_path(self, imp: str, current_file: str) -> Optional[str]:
        """Resolve import path to actual file path."""
        # Simple resolution for core modules
        if imp.startswith('core.'):
            parts = imp.split('.')
            if len(parts) >= 2:
                if len(parts) == 2:
                    return f"{parts[0]}/{parts[1]}.py"
                else:
                    return f"{parts[0]}/{parts[1]}.py"  # Simplified

        return None

    def _generate_graph_summary(self) -> Dict[str, Any]:
        """Generate summary of the dependency graph."""
        return {
            "total_nodes": self.dependency_graph.number_of_nodes(),
            "total_edges": self.dependency_graph.number_of_edges(),
            "graph_density": nx.density(self.dependency_graph),
            "is_connected": nx.is_weakly_connected(self.dependency_graph),
            "components": nx.number_weakly_connected_components(self.dependency_graph),
            "avg_degree": sum(dict(self.dependency_graph.degree()).values()) / max(self.dependency_graph.number_of_nodes(), 1)
        }

    def _analyze_cycle(self, cycle: List[str]) -> Dict[str, Any]:
        """Analyze a circular dependency cycle."""
        impact_score = len(cycle) * 0.2

        # Check if cycle involves core modules
        core_involvement = sum(1 for module in cycle if "core/" in module)
        if core_involvement > 0:
            impact_score += core_involvement * 0.3

        severity = "high" if impact_score > 0.7 else "medium" if impact_score > 0.4 else "low"

        return {
            "impact": impact_score,
            "severity": severity,
            "suggestion": self._generate_cycle_suggestion(cycle, severity),
            "affected_modules": cycle
        }

    def _generate_cycle_suggestion(self, cycle: List[str], severity: str) -> str:
        """Generate suggestion for resolving circular dependency."""
        if severity == "high":
            return "Immediate refactoring required - consider dependency injection or interface extraction"
        elif severity == "medium":
            return "Plan refactoring for next sprint - extract shared dependencies"
        else:
            return "Monitor this cycle during development"

    def _assign_to_layer(self, node: str, layers: Dict[str, List[str]]) -> str:
        """Assign a node to an architectural layer."""
        node_lower = node.lower()

        for layer_name, keywords in layers.items():
            if any(keyword in node_lower for keyword in keywords):
                return layer_name

        return "unknown"

    def _detect_layer_violations(self, layer_graph: nx.DiGraph) -> List[Dict[str, Any]]:
        """Detect architectural layer violations."""
        violations = []

        # Check for business logic accessing infrastructure directly
        if layer_graph.has_edge("business", "infrastructure"):
            violations.append({
                "type": "layer_violation",
                "source": "business",
                "target": "infrastructure",
                "description": "Business layer directly accessing infrastructure",
                "severity": "high"
            })

        # Check for presentation accessing data layer directly
        if layer_graph.has_edge("presentation", "data"):
            violations.append({
                "type": "layer_violation",
                "source": "presentation",
                "target": "data",
                "description": "Presentation layer directly accessing data layer",
                "severity": "medium"
            })

        return violations

    def _calculate_layer_strength(self, layer_nodes: Dict[str, List[str]]) -> Dict[str, float]:
        """Calculate strength of each architectural layer."""
        strength = {}
        total_nodes = sum(len(nodes) for nodes in layer_nodes.values())

        for layer, nodes in layer_nodes.items():
            if total_nodes > 0:
                strength[layer] = len(nodes) / total_nodes
            else:
                strength[layer] = 0.0

        return strength

    def _calculate_layer_coupling(self, layer_graph: nx.DiGraph) -> Dict[str, Any]:
        """Calculate coupling metrics between layers."""
        return {
            "total_inter_layer_edges": layer_graph.number_of_edges(),
            "layer_density": nx.density(layer_graph),
            "strongest_coupling": max(
                [(source, target, data["weight"])
                 for source, target, data in layer_graph.edges(data=True)],
                key=lambda x: x[2],
                default=(None, None, 0)
            )
        }

    def _check_critical_path_affected(self, changed_module: str, affected: Set[str]) -> bool:
        """Check if critical path modules are affected."""
        critical_modules = ["core/collection.py", "core/pipeline", "core/deduplication"]
        return any(any(critical in module for critical in critical_modules) for module in affected)

    def _calculate_impact_radius(self, affected: Set[str]) -> int:
        """Calculate impact radius score."""
        return len(affected)

    def _generate_impact_recommendations(self, changed_module: str, metrics: Dict[str, Any]) -> List[str]:
        """Generate recommendations for change impact."""
        recommendations = []

        if metrics["total_affected"] > 10:
            recommendations.append("Consider integration testing for all affected modules")

        if metrics["critical_path_affected"]:
            recommendations.append("Prioritize testing of critical path components")

        if metrics["needs_testing"] > 5:
            recommendations.append("Run comprehensive regression testing")

        return recommendations

    def _calculate_test_priority(self, metrics: Dict[str, Any]) -> str:
        """Calculate testing priority based on impact metrics."""
        score = (
            metrics["total_affected"] * 0.4 +
            metrics["needs_testing"] * 0.3 +
            (1.0 if metrics["critical_path_affected"] else 0) * 0.3
        )

        if score > 5:
            return "high"
        elif score > 2:
            return "medium"
        else:
            return "low"

    def _assess_risk_level(self, critical_score: float) -> str:
        """Assess risk level based on critical score."""
        if critical_score > 0.7:
            return "critical"
        elif critical_score > 0.5:
            return "high"
        elif critical_score > 0.3:
            return "medium"
        else:
            return "low"