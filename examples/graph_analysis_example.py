#!/usr/bin/env python3
"""
RedditHarbor Graph Analysis Example

Demonstrates the usage of Deep-Graph-MCP integration for intelligent code analysis.
This example shows how to use the graph integration tools to analyze dependencies,
identify refactoring opportunities, and improve code quality.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.graph_integration.analyzer import RedditHarborGraphAnalyzer
from core.graph_integration.dependencies import DependencyMapper
from core.graph_integration.refactoring import IntelligentRefactorer


def main():
    """Main demonstration of graph analysis capabilities."""
    print("🚀 RedditHarbor Graph Analysis Example")
    print("=" * 50)

    # Initialize the graph analyzer
    analyzer = RedditHarborGraphAnalyzer()
    mapper = DependencyMapper()
    refactorer = IntelligentRefactorer()

    print(f"📁 Analyzing project: {project_root}")
    print(f"🧠 Deep-Graph-MCP available: {analyzer.graph_available}")
    print()

    # Example 1: Analyze module dependencies
    print("1️⃣ Analyzing Core Module Dependencies")
    print("-" * 40)

    collection_analysis = analyzer.analyze_module_dependencies("core/collection.py")
    print(f"Module: {collection_analysis.get('module', 'core/collection.py')}")
    print(f"Dependencies: {len(collection_analysis.get('dependencies', []))}")
    print(f"Risk Level: {collection_analysis.get('risk_level', 'unknown')}")
    print(f"Critical Path: {collection_analysis.get('critical_path', False)}")
    print()

    # Example 2: Find refactoring opportunities
    print("2️⃣ Finding Refactoring Opportunities")
    print("-" * 40)

    opportunities = analyzer.find_refactoring_opportunities(complexity_threshold=0.3)
    print(f"Found {len(opportunities)} refactoring opportunities:")

    for i, opp in enumerate(opportunities[:3], 1):  # Show top 3
        print(f"  {i}. {opp['file']}")
        print(f"     Complexity: {opp['complexity']:.2f}")
        print(f"     Priority: {opp['priority']:.2f}")
        print(f"     Suggestions: {len(opp['suggestions'])}")
    print()

    # Example 3: Build dependency graph
    print("3️⃣ Building Dependency Graph")
    print("-" * 40)

    graph_summary = mapper.build_dependency_graph()
    print(f"Total Nodes: {graph_summary.get('total_nodes', 0)}")
    print(f"Total Edges: {graph_summary.get('total_edges', 0)}")
    print(f"Graph Density: {graph_summary.get('graph_density', 0):.3f}")
    print(f"Is Connected: {graph_summary.get('is_connected', False)}")
    print()

    # Example 4: Detect circular dependencies
    print("4️⃣ Detecting Circular Dependencies")
    print("-" * 40)

    circular_deps = mapper.detect_circular_dependencies()
    print(f"Found {len(circular_deps)} circular dependencies:")

    for cycle in circular_deps[:2]:  # Show first 2
        print(f"  Cycle {cycle['cycle_id']}: {cycle['cycle']}")
        print(f"  Severity: {cycle['severity']}")
        print(f"  Impact: {cycle['impact']:.2f}")
    print()

    # Example 5: Generate refactoring plan
    print("5️⃣ Generating Refactoring Plan")
    print("-" * 40)

    refactoring_plan = refactorer.generate_refactoring_suggestions(severity_threshold="low")
    print(f"Target Files: {len(refactoring_plan.target_files)}")
    print(f"Total Suggestions: {len(refactoring_plan.suggestions)}")
    print(f"Estimated Effort: {refactoring_plan.estimated_effort}")
    print(f"Risk Assessment: {refactoring_plan.risk_assessment}")
    print()

    # Example 6: Analyze architectural patterns
    print("6️⃣ Analyzing Architectural Patterns")
    print("-" * 40)

    arch_analysis = analyzer.analyze_architecture_patterns()
    print(f"Patterns Detected: {arch_analysis.get('patterns_detected', [])}")
    print(f"Violations: {len(arch_analysis.get('violations', []))}")
    print(f"Architecture Score: {arch_analysis.get('architecture_score', 0):.2f}")
    print()

    # Generate comprehensive report
    print("📊 Generating Comprehensive Analysis Report")
    print("=" * 50)

    report = generate_comprehensive_report(
        analyzer, mapper, refactorer,
        collection_analysis, opportunities,
        graph_summary, circular_deps, refactoring_plan,
        arch_analysis
    )

    # Save report to file
    report_path = project_root / "analysis_report.md"
    with open(report_path, 'w') as f:
        f.write(report)

    print(f"📄 Report saved to: {report_path}")
    print("✅ Graph analysis complete!")


def generate_comprehensive_report(
    analyzer, mapper, refactorer,
    collection_analysis, opportunities,
    graph_summary, circular_deps, refactoring_plan,
    arch_analysis
):
    """Generate a comprehensive analysis report."""

    report = f"""# RedditHarbor Graph Analysis Report

Generated: {{analysis_date}}

## Executive Summary

This report provides comprehensive analysis of the RedditHarbor codebase using Deep-Graph-MCP integration.
The analysis covers dependency mapping, code quality assessment, refactoring opportunities, and architectural patterns.

## Key Metrics

### Codebase Overview
- **Total Python Files**: {graph_summary.get('total_nodes', 0)}
- **Dependency Graph Density**: {graph_summary.get('graph_density', 0):.3f}
- **Graph Connectivity**: {'Connected' if graph_summary.get('is_connected') else 'Disconnected'}
- **Circular Dependencies**: {len(circular_deps)}
- **Refactoring Opportunities**: {len(opportunities)}

### Quality Assessment
- **Architecture Score**: {arch_analysis.get('architecture_score', 0):.2f}/1.0
- **Patterns Detected**: {', '.join(arch_analysis.get('patterns_detected', []))}
- **Violations Found**: {len(arch_analysis.get('violations', []))}

## Detailed Analysis

### 1. Core Module Analysis

**Module**: core/collection.py
- **Dependencies**: {len(collection_analysis.get('dependencies', []))}
- **Risk Level**: {collection_analysis.get('risk_level', 'unknown').title()}
- **Critical Path**: {'Yes' if collection_analysis.get('critical_path') else 'No'}
- **Impact Radius**: {collection_analysis.get('impact_radius', 0)}

### 2. Refactoring Opportunities

**High Priority Items**:
"""

    # Add high priority refactoring opportunities
    high_priority = [opp for opp in opportunities if opp['priority'] > 0.7][:5]
    for i, opp in enumerate(high_priority, 1):
        report += f"""
{i}. **{opp['file']}**
   - Complexity: {opp['complexity']:.2f}
   - Issues: {len(opp['suggestions'])}
   - Estimated Effort: {opp.get('estimated_effort', 'medium')}
"""

    report += f"""
### 3. Dependency Analysis

**Graph Statistics**:
- **Nodes**: {graph_summary.get('total_nodes', 0)}
- **Edges**: {graph_summary.get('total_edges', 0)}
- **Components**: {graph_summary.get('components', 1)}
- **Average Degree**: {graph_summary.get('avg_degree', 0):.2f}

**Circular Dependencies**:
"""

    if circular_deps:
        for cycle in circular_deps[:3]:
            report += f"""
- **Cycle {cycle['cycle_id']}**: {' → '.join(cycle['cycle'])}
  - Severity: {cycle['severity']}
  - Impact: {cycle['impact']:.2f}
  - Suggestion: {cycle['suggestion']}
"""
    else:
        report += "No circular dependencies detected. ✅"

    report += f"""
### 4. Architectural Analysis

**Detected Patterns**:
"""

    for pattern in arch_analysis.get('patterns_detected', []):
        report += f"- ✅ {pattern}\n"

    violations = arch_analysis.get('violations', [])
    if violations:
        report += "\n**Architectural Violations**:\n"
        for violation in violations[:3]:
            report += f"- ⚠️ {violation.get('description', 'Unknown violation')}\n"

    recommendations = arch_analysis.get('recommendations', [])
    if recommendations:
        report += "\n**Recommendations**:\n"
        for rec in recommendations:
            report += f"- 💡 {rec}\n"

    report += f"""
## Refactoring Plan

**Target Files**: {len(refactoring_plan.target_files)}
**Estimated Effort**: {refactoring_plan.estimated_effort}
**Risk Assessment**: {refactoring_plan.risk_assessment}

### Implementation Order
"""

    for i, file_path in enumerate(refactoring_plan.implementation_order[:5], 1):
        report += f"{i}. {file_path}\n"

    report += f"""
## Next Steps

### Immediate Actions (Week 1)
1. **Address Circular Dependencies**: {len(circular_deps)} cycles need resolution
2. **High Priority Refactoring**: {len(high_priority)} files with complexity > 0.7
3. **Architectural Violations**: {len(violations)} violations to fix

### Medium-term Goals (Month 1)
1. **Dependency Optimization**: Reduce graph density if > 0.3
2. **Code Quality Improvement**: Target architecture score > 0.8
3. **Documentation Enhancement**: Improve module documentation coverage

### Long-term Improvements (Quarter 1)
1. **Automated Refactoring**: Implement automated fixes for common issues
2. **Continuous Monitoring**: Set up automated code quality checks
3. **Knowledge Graph**: Maintain living documentation through graph analysis

## Tool Usage

This analysis was generated using:
- **RedditHarborGraphAnalyzer**: Intelligent code analysis
- **DependencyMapper**: Advanced dependency mapping
- **IntelligentRefactorer**: Automated refactoring suggestions

## Conclusion

The RedditHarbor codebase shows {get_quality_assessment(arch_analysis.get('architecture_score', 0))}.
{get_recommendation_summary(opportunities, circular_deps, violations)}.

---

*Report generated by RedditHarbor Deep-Graph-MCP Integration*
"""

    return report


def get_quality_assessment(score):
    """Get quality assessment based on architecture score."""
    if score > 0.8:
        return "excellent code quality with strong architectural patterns"
    elif score > 0.6:
        return "good code quality with room for improvement"
    elif score > 0.4:
        return "moderate code quality requiring attention"
    else:
        return "code quality issues that need immediate attention"


def get_recommendation_summary(opportunities, circular_deps, violations):
    """Get summary of recommendations."""
    issues = len(opportunities) + len(circular_deps) + len(violations)

    if issues > 20:
        return "Multiple areas require attention for improved maintainability"
    elif issues > 10:
        return "Several improvement opportunities identified for better code quality"
    elif issues > 5:
        return "Some refactoring recommended to enhance the codebase"
    else:
        return "Codebase is in good condition with minor improvements possible"


if __name__ == "__main__":
    main()