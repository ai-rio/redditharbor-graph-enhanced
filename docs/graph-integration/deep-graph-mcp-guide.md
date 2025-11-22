# Deep-Graph-MCP Integration Guide

## Overview

This guide provides comprehensive documentation for integrating Deep-Graph-MCP with RedditHarbor, enabling intelligent code analysis, dependency mapping, and automated refactoring capabilities.

## Architecture

### Core Components

#### 1. RedditHarborGraphAnalyzer

The main analysis engine that provides:

- **Semantic Code Analysis**: AI-powered understanding of code relationships
- **Dependency Mapping**: Comprehensive dependency visualization and analysis
- **Complexity Assessment**: Multi-dimensional code complexity evaluation
- **Refactoring Intelligence**: Automated suggestion generation with risk assessment
- **Architecture Pattern Detection**: Identification of design patterns and violations

#### 2. DependencyMapper

Advanced dependency analysis tool featuring:

- **Multi-level Graph Analysis**: Module, class, and function-level dependencies
- **Circular Dependency Detection**: Automated detection with impact analysis
- **Critical Path Identification**: Key dependency path analysis
- **Architectural Layer Analysis**: Layer adherence and violation detection
- **Impact Analysis**: Change propagation and risk assessment

#### 3. IntelligentRefactorer

Automated refactoring assistant providing:

- **Code Quality Analysis**: Comprehensive quality metrics and assessment
- **Automated Fix Generation**: AI-powered code improvement suggestions
- **Risk Assessment**: Change impact and rollback planning
- **Validation Pipeline**: Safety checks before applying changes
- **Reporting**: Detailed refactoring recommendations and implementation plans

## Installation and Setup

### Prerequisites

1. **Python Environment**: Python 3.8+
2. **DeepGraph Project**: Create project at https://deepgraph.co/projects/redditharbor-graph-enhanced
3. **Dependencies**: Install via `uv sync` or `pip install -r requirements.txt`

### Configuration

```python
# config/graph_settings.py
GRAPH_CONFIG = {
    "deepgraph_project": "redditharbor-graph-enhanced",
    "auto_analysis": True,
    "refactoring_threshold": 0.8,
    "dependency_depth": 5,
    "semantic_search_enabled": True,
    "fallback_analysis": True,
    "risk_assessment_enabled": True
}

# MCP Tool Configuration
MCP_CONFIG = {
    "semantic_search_enabled": True,
    "dependency_mapping_enabled": True,
    "usage_analysis_enabled": True,
    "graph_visualization_enabled": True
}
```

## Usage Examples

### Basic Analysis

```python
from core.graph_integration import RedditHarborGraphAnalyzer

# Initialize analyzer
analyzer = RedditHarborGraphAnalyzer(project_root=".")

# Analyze specific module
deps = analyzer.analyze_module_dependencies("core/collection.py")
print(f"Dependencies: {len(deps['dependencies'])}")
print(f"Risk Level: {deps['risk_level']}")

# Find refactoring opportunities
opportunities = analyzer.find_refactoring_opportunities()
for opp in opportunities[:5]:
    print(f"- {opp['file']}: {opp['complexity']:.2f}")
```

### Advanced Dependency Analysis

```python
from core.graph_integration import DependencyMapper

# Initialize mapper
mapper = DependencyMapper()

# Build comprehensive dependency graph
graph_summary = mapper.build_dependency_graph(depth=3)
print(f"Total Nodes: {graph_summary['total_nodes']}")
print(f"Total Edges: {graph_summary['total_edges']}")

# Detect circular dependencies
circular_deps = mapper.detect_circular_dependencies()
for dep in circular_deps:
    print(f"Cycle: {dep['cycle']}")
    print(f"Severity: {dep['severity']}")
```

### Intelligent Refactoring

```python
from core.graph_integration.refactoring import IntelligentRefactorer

# Initialize refactorer
refactorer = IntelligentRefactorer()

# Generate comprehensive refactoring plan
plan = refactorer.generate_refactoring_suggestions()
print(f"Target Files: {len(plan.target_files)}")
print(f"Estimated Effort: {plan.estimated_effort}")

# Validate refactoring plan
validation = refactorer.validate_refactoring(plan)
if validation['is_valid']:
    print("✅ Refactoring plan validated")
else:
    print("❌ Validation issues found")
    for error in validation['errors']:
        print(f"- {error}")
```

## API Reference

### RedditHarborGraphAnalyzer

#### Methods

##### `analyze_module_dependencies(module_path: str) -> Dict[str, Any]`

Analyzes dependencies for a specific module.

**Parameters:**
- `module_path`: Path to the module to analyze

**Returns:**
- Dictionary containing dependency analysis results

**Example:**
```python
result = analyzer.analyze_module_dependencies("core/collection.py")
# Returns: {
#     "module": "core/collection.py",
#     "dependencies": [...],
#     "dependents": [...],
#     "risk_level": "medium",
#     "critical_path": True
# }
```

##### `find_refactoring_opportunities(complexity_threshold: float = 0.8) -> List[Dict[str, Any]]`

Identifies modules that need refactoring.

**Parameters:**
- `complexity_threshold`: Minimum complexity score to flag for refactoring

**Returns:**
- List of refactoring opportunities with detailed analysis

##### `trace_data_flow(data_entity: str) -> Dict[str, Any]`

Traces data flow through the RedditHarbor pipeline.

**Parameters:**
- `data_entity`: Name of the data entity to trace

**Returns:**
- Dictionary containing data flow analysis

##### `analyze_architectural_patterns() -> Dict[str, Any]`

Analyzes architectural patterns and design principles.

**Returns:**
- Dictionary containing architecture analysis results

### DependencyMapper

#### Methods

##### `build_dependency_graph(depth: int = 3) -> Dict[str, Any]`

Builds comprehensive dependency graph.

**Parameters:**
- `depth`: Depth of dependency analysis

**Returns:**
- Dictionary containing graph analysis results

##### `detect_circular_dependencies() -> List[Dict[str, Any]]`

Detects circular dependencies in the codebase.

**Returns:**
- List of circular dependency chains with analysis

##### `identify_critical_dependencies() -> Dict[str, Any]`

Identifies critical dependencies that could impact the entire system.

**Returns:**
- Dictionary containing critical dependency analysis

##### `analyze_architectural_layers() -> Dict[str, Any]`

Analyzes architectural layers and their dependencies.

**Returns:**
- Dictionary containing layer analysis results

### IntelligentRefactorer

#### Methods

##### `analyze_code_quality(target_path: str = None) -> Dict[str, Any]`

Performs comprehensive code quality analysis.

**Parameters:**
- `target_path`: Specific path to analyze (None for entire project)

**Returns:**
- Dictionary containing code quality analysis results

##### `generate_refactoring_suggestions(severity_threshold: str = "medium") -> RefactoringPlan`

Generates comprehensive refactoring suggestions.

**Parameters:**
- `severity_threshold`: Minimum severity level for suggestions

**Returns:**
- Comprehensive refactoring plan

##### `implement_automated_fixes(plan: RefactoringPlan, backup: bool = True) -> Dict[str, Any]`

Implements automated fixes from refactoring plan.

**Parameters:**
- `plan`: Refactoring plan to implement
- `backup`: Whether to create backups before making changes

**Returns:**
- Dictionary containing implementation results

##### `validate_refactoring(plan: RefactoringPlan) -> Dict[str, Any]`

Validates refactoring plan for potential issues.

**Parameters:**
- `plan`: Refactoring plan to validate

**Returns:**
- Dictionary containing validation results

## Advanced Features

### Semantic Code Search

Deep-Graph-MCP integration enables semantic code search:

```python
# Search for similar functionality
similar_code = mcp__Deep-Graph-MCP__nodes_semantic_search(
    query="Reddit data collection pipeline optimization"
)

# Find related modules
related_modules = mcp__Deep-Graph-MCP__nodes_semantic_search(
    query="database schema validation and migration"
)
```

### Impact Analysis

Advanced change impact analysis:

```python
# Analyze impact of proposed changes
impact = mapper.generate_impact_analysis("core/collection.py")
print(f"Affected modules: {len(impact['affected_modules'])}")
print(f"Testing required: {len(impact['needs_testing'])}")
```

### Graph Visualization

Generate interactive dependency graphs:

```python
# Visualize dependency graph
graph_path = mapper.visualize_dependency_graph(
    output_path="dependency_graph.png",
    layout="hierarchical"
)

# Export dependency matrix
matrix_path = mapper.export_dependency_matrix(
    output_path="dependency_matrix.json"
)
```

## Configuration Options

### Analysis Settings

```python
ANALYSIS_CONFIG = {
    "complexity_thresholds": {
        "low": 0.3,
        "medium": 0.6,
        "high": 0.8
    },
    "dependency_analysis": {
        "max_depth": 5,
        "include_test_dependencies": False,
        "circular_dependency_sensitivity": 0.7
    },
    "refactoring": {
        "automated_fix_enabled": True,
        "backup_before_changes": True,
        "validation_strictness": "medium"
    }
}
```

### Visualization Settings

```python
VISUALIZATION_CONFIG = {
    "graph_layout": "spring",
    "node_size_factor": 100,
    "edge_width_factor": 2,
    "color_scheme": "dependency-based",
    "export_formats": ["png", "svg", "json"]
}
```

## Best Practices

### 1. Incremental Analysis

Start with high-level analysis before diving into details:

```python
# Start with overview
overview = analyzer.analyze_architectural_patterns()

# Then dive into specific areas
if overview["architecture_score"] < 0.7:
    opportunities = analyzer.find_refactoring_opportunities(0.5)
    print(f"Found {len(opportunities)} high-priority improvements")
```

### 2. Risk Assessment

Always validate refactoring plans:

```python
plan = refactorer.generate_refactoring_suggestions()
validation = refactorer.validate_refactoring(plan)

if not validation["is_valid"]:
    print("High-risk refactoring detected:")
    for warning in validation["warnings"]:
        print(f"- {warning}")
```

### 3. Backup Strategy

Maintain backups during automated refactoring:

```python
# Enable automatic backups
result = refactorer.implement_automated_fixes(
    plan=plan,
    backup=True
)

# Store rollback information
rollback_info = result["rollback_info"]
print(f"Backup created: {result['backup_path']}")
```

## Troubleshooting

### Common Issues

#### 1. Deep-Graph-MCP Not Available

**Problem**: MCP tools not accessible
**Solution**: Fallback to AST-based analysis automatically

```python
# Check availability
if analyzer.graph_available:
    # Use MCP tools
    deps = analyzer._get_graph_dependencies(module_path)
else:
    # Use fallback analysis
    deps = analyzer._fallback_dependency_analysis(module_path)
```

#### 2. Large Repository Analysis

**Problem**: Analysis takes too long
**Solution**: Use targeted analysis

```python
# Analyze specific modules instead of entire project
target_modules = ["core/collection.py", "core/pipeline/"]
for module in target_modules:
    analysis = analyzer.analyze_module_dependencies(module)
    # Process results
```

#### 3. Memory Issues

**Problem**: Graph analysis consumes too much memory
**Solution**: Limit analysis depth

```python
# Use limited depth analysis
graph_summary = mapper.build_dependency_graph(depth=2)
```

## Performance Optimization

### Analysis Optimization

```python
# Cache analysis results
analyzer.module_cache = {}

# Use incremental analysis
def incremental_analysis():
    if not hasattr(analyzer, '_last_analysis'):
        analyzer._last_analysis = time.time()

    if time.time() - analyzer._last_analysis > 3600:  # 1 hour
        # Rebuild analysis
        analyzer.module_cache.clear()
        analyzer._last_analysis = time.time()
```

### Memory Management

```python
# Clear caches after large operations
def cleanup_after_analysis():
    analyzer.module_cache.clear()
    mapper.dependency_graph.clear()
    import gc
    gc.collect()
```

## Integration Examples

### CI/CD Integration

```yaml
# .github/workflows/graph-analysis.yml
name: Graph Analysis

on: [push, pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run graph analysis
        run: |
          python examples/graph_analysis_example.py
      - name: Upload analysis report
        uses: actions/upload-artifact@v2
        with:
          name: analysis-report
          path: analysis_report.md
```

### IDE Integration

```python
# VS Code settings for graph integration
# .vscode/settings.json
{
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black"
}
```

## Contributing

### Development Setup

```bash
# Clone repository
git clone https://github.com/ai-rio/redditharbor-graph-enhanced.git
cd redditharbor-graph-enhanced

# Set up environment
uv sync

# Run tests
python tests/test_graph_integration.py

# Run example
python examples/graph_analysis_example.py
```

### Code Style

Follow these conventions:
- Use type hints for all functions
- Include comprehensive docstrings
- Follow PEP 8 naming conventions
- Write tests for new features
- Update documentation

## Support

For support with Deep-Graph-MCP integration:

1. **Documentation**: Check this guide and inline docstrings
2. **Examples**: Review `examples/graph_analysis_example.py`
3. **Tests**: Consult `tests/test_graph_integration.py`
4. **Issues**: Report problems on GitHub issues

## License

This integration is released under the MIT License. See LICENSE for details.