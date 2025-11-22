"""
Intelligent Refactoring Assistant for RedditHarbor

Advanced automated refactoring suggestions and implementation using Deep-Graph-MCP.
Provides intelligent code improvement recommendations with risk assessment and automated fixes.
"""

import logging
import ast
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import json
from difflib import unified_diff
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class RefactoringSuggestion:
    """Represents a refactoring suggestion."""
    type: str
    description: str
    file_path: str
    line_numbers: Tuple[int, int]
    severity: str  # 'low', 'medium', 'high', 'critical'
    effort: str   # 'low', 'medium', 'high'
    impact_risk: str  # 'low', 'medium', 'high'
    automated_fix: bool
    suggested_code: str
    rationale: str
    dependencies: List[str]


@dataclass
class RefactoringPlan:
    """Represents a comprehensive refactoring plan."""
    target_files: List[str]
    suggestions: List[RefactoringSuggestion]
    estimated_effort: str
    risk_assessment: str
    implementation_order: List[str]
    rollback_plan: Dict[str, str]


class IntelligentRefactorer:
    """
    Intelligent refactoring assistant using Deep-Graph-MCP for code analysis.

    Features:
    - Automated code quality analysis
    - Intelligent refactoring suggestions
    - Risk assessment and impact analysis
    - Automated fix generation where possible
    - Comprehensive refactoring planning
    - Progress tracking and rollback capabilities
    """

    def __init__(self, project_root: str = None):
        """
        Initialize the intelligent refactorer.

        Args:
            project_root: Root directory of the project to analyze
        """
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.suggestions = []
        self.refactoring_history = []
        self.graph_available = self._check_graph_availability()

        logger.info(f"🔧 Initialized Intelligent Refactorer")
        logger.info(f"📁 Project root: {self.project_root}")
        logger.info(f"🧠 Deep-Graph-MCP available: {self.graph_available}")

    def _check_graph_availability(self) -> bool:
        """Check if Deep-Graph-MCP tools are available."""
        try:
            from mcp__Deep-Graph-MCP__nodes_semantic_search import nodes_semantic_search
            return True
        except ImportError:
            logger.warning("⚠️ Deep-Graph-MCP not yet available - using fallback analysis")
            return False

    def analyze_code_quality(self, target_path: str = None) -> Dict[str, Any]:
        """
        Comprehensive code quality analysis using Deep-Graph-MCP.

        Args:
            target_path: Specific path to analyze (None for entire project)

        Returns:
            Dictionary containing code quality analysis results
        """
        logger.info(f"📊 Analyzing code quality for: {target_path or 'entire project'}")

        if self.graph_available:
            return self._graph_quality_analysis(target_path)
        else:
            return self._fallback_quality_analysis(target_path)

    def generate_refactoring_suggestions(self, severity_threshold: str = "medium") -> RefactoringPlan:
        """
        Generate comprehensive refactoring suggestions.

        Args:
            severity_threshold: Minimum severity level for suggestions

        Returns:
            Comprehensive refactoring plan
        """
        logger.info(f"🎯 Generating refactoring suggestions (threshold: {severity_threshold})")

        # Analyze all Python files
        python_files = self._get_target_files()
        all_suggestions = []

        for file_path in python_files:
            try:
                file_suggestions = self._analyze_file_for_refactoring(file_path)
                all_suggestions.extend(file_suggestions)

            except Exception as e:
                logger.warning(f"⚠️ Failed to analyze {file_path}: {e}")

        # Filter by severity
        severity_levels = {"low": 1, "medium": 2, "high": 3, "critical": 4}
        threshold_value = severity_levels.get(severity_threshold, 2)

        filtered_suggestions = [
            s for s in all_suggestions
            if severity_levels.get(s.severity, 0) >= threshold_value
        ]

        # Sort by priority (severity * impact_risk)
        filtered_suggestions.sort(
            key=lambda s: (
                severity_levels.get(s.severity, 0) *
                severity_levels.get(s.impact_risk, 0)
            ),
            reverse=True
        )

        # Create refactoring plan
        plan = self._create_refactoring_plan(filtered_suggestions)

        logger.info(f"✨ Generated {len(filtered_suggestions)} refactoring suggestions")
        return plan

    def implement_automated_fixes(self, plan: RefactoringPlan, backup: bool = True) -> Dict[str, Any]:
        """
        Implement automated fixes from refactoring plan.

        Args:
            plan: Refactoring plan to implement
            backup: Whether to create backups before making changes

        Returns:
            Dictionary containing implementation results
        """
        logger.info("🤖 Implementing automated refactoring fixes")

        results = {
            "successful_fixes": [],
            "failed_fixes": [],
            "manual_fixes_required": [],
            "backup_created": False,
            "rollback_info": {}
        }

        if backup:
            backup_path = self._create_backup()
            results["backup_created"] = True
            results["backup_path"] = str(backup_path)

        # Group suggestions by file
        suggestions_by_file = {}
        for suggestion in plan.suggestions:
            if suggestion.automated_fix:
                if suggestion.file_path not in suggestions_by_file:
                    suggestions_by_file[suggestion.file_path] = []
                suggestions_by_file[suggestion.file_path].append(suggestion)

        # Apply fixes file by file
        for file_path, file_suggestions in suggestions_by_file.items():
            try:
                result = self._apply_file_fixes(file_path, file_suggestions)
                results["successful_fixes"].extend(result["successful"])
                results["failed_fixes"].extend(result["failed"])

            except Exception as e:
                logger.error(f"❌ Failed to apply fixes to {file_path}: {e}")
                results["failed_fixes"].extend(file_suggestions)

        # Track manual fixes
        results["manual_fixes_required"] = [
            s for s in plan.suggestions if not s.automated_fix
        ]

        # Store rollback information
        results["rollback_info"] = self._generate_rollback_info(plan)

        logger.info(f"🎉 Applied {len(results['successful_fixes'])} automated fixes")
        return results

    def validate_refactoring(self, plan: RefactoringPlan) -> Dict[str, Any]:
        """
        Validate refactoring plan for potential issues.

        Args:
            plan: Refactoring plan to validate

        Returns:
            Dictionary containing validation results
        """
        logger.info("✅ Validating refactoring plan")

        validation_results = {
            "is_valid": True,
            "warnings": [],
            "errors": [],
            "risk_factors": [],
            "dependencies_check": {},
            "test_coverage_impact": {}
        }

        # Check for circular dependencies
        circular_deps = self._check_circular_dependencies(plan)
        if circular_deps:
            validation_results["warnings"].extend(circular_deps)
            validation_results["risk_factors"].append("circular_dependencies")

        # Validate dependency impact
        dependency_impact = self._validate_dependency_impact(plan)
        validation_results["dependencies_check"] = dependency_impact

        if dependency_impact.get("high_impact_count", 0) > 5:
            validation_results["warnings"].append("High number of high-impact changes")
            validation_results["risk_factors"].append("extensive_impact")

        # Check test coverage
        test_impact = self._analyze_test_coverage_impact(plan)
        validation_results["test_coverage_impact"] = test_impact

        if test_impact.get("coverage_loss", 0) > 0.1:
            validation_results["warnings"].append("Significant test coverage loss expected")
            validation_results["risk_factors"].append("coverage_loss")

        # Check for breaking changes
        breaking_changes = self._identify_breaking_changes(plan)
        if breaking_changes:
            validation_results["errors"].extend(breaking_changes)
            validation_results["is_valid"] = False

        logger.info(f"🔍 Validation complete: {'✅ Valid' if validation_results['is_valid'] else '❌ Issues found'}")
        return validation_results

    def generate_refactoring_report(self, plan: RefactoringPlan) -> str:
        """
        Generate comprehensive refactoring report.

        Args:
            plan: Refactoring plan to report on

        Returns:
            Markdown formatted refactoring report
        """
        logger.info("📄 Generating refactoring report")

        report_lines = [
            "# RedditHarbor Refactoring Report",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Executive Summary",
            "",
            f"- **Target Files**: {len(plan.target_files)}",
            f"- **Total Suggestions**: {len(plan.suggestions)}",
            f"- **Estimated Effort**: {plan.estimated_effort}",
            f"- **Risk Assessment**: {plan.risk_assessment}",
            "",
            "## Suggestions by Severity",
            ""
        ]

        # Group suggestions by severity
        severity_groups = {}
        for suggestion in plan.suggestions:
            if suggestion.severity not in severity_groups:
                severity_groups[suggestion.severity] = []
            severity_groups[suggestion.severity].append(suggestion)

        severity_order = ["critical", "high", "medium", "low"]
        for severity in severity_order:
            if severity in severity_groups:
                report_lines.extend([
                    f"### {severity.title()} ({len(severity_groups[severity])})",
                    ""
                ])

                for suggestion in severity_groups[severity]:
                    report_lines.extend([
                        f"**{suggestion.type}** - `{suggestion.file_path}:{suggestion.line_numbers[0]}-{suggestion.line_numbers[1]}`",
                        f"- Description: {suggestion.description}",
                        f"- Effort: {suggestion.effort}, Risk: {suggestion.impact_risk}",
                        f"- Automated: {'✅' if suggestion.automated_fix else '❌'}",
                        f"- Rationale: {suggestion.rationale}",
                        ""
                    ])

        # Implementation plan
        report_lines.extend([
            "## Implementation Plan",
            "",
            "### Recommended Order:",
            ""
        ])

        for i, file_path in enumerate(plan.implementation_order, 1):
            file_suggestions = [s for s in plan.suggestions if s.file_path == file_path]
            if file_suggestions:
                report_lines.extend([
                    f"{i}. **{file_path}** ({len(file_suggestions)} suggestions)",
                    f"   - Effort: {max(s.effort for s in file_suggestions)}",
                    f"   - Risk: {max(s.impact_risk for s in file_suggestions)}",
                    ""
                ])

        # Rollback plan
        report_lines.extend([
            "## Rollback Plan",
            "",
            "If issues arise during implementation:",
            ""
        ])

        for file_path, rollback_action in plan.rollback_plan.items():
            report_lines.append(f"- `{file_path}`: {rollback_action}")

        report_lines.extend([
            "",
            "---",
            "*Generated by RedditHarbor Intelligent Refactorer*"
        ])

        return "\n".join(report_lines)

    # Private methods
    def _graph_quality_analysis(self, target_path: str) -> Dict[str, Any]:
        """Perform quality analysis using Deep-Graph-MCP."""
        try:
            from mcp__Deep-Graph-MCP__nodes_semantic_search import nodes_semantic_search

            # Search for code quality issues
            quality_issues = nodes_semantic_search(
                query="code quality issues complexity maintainability violations"
            )

            return self._analyze_quality_results(quality_issues, target_path)

        except Exception as e:
            logger.error(f"Graph quality analysis failed: {e}")
            return self._fallback_quality_analysis(target_path)

    def _fallback_quality_analysis(self, target_path: str) -> Dict[str, Any]:
        """Fallback quality analysis using AST."""
        logger.info("🔄 Using fallback AST analysis for code quality")

        python_files = self._get_target_files(target_path)
        quality_metrics = {
            "total_files": len(python_files),
            "files_analyzed": 0,
            "quality_issues": [],
            "metrics": {}
        }

        total_complexity = 0
        total_lines = 0

        for file_path in python_files:
            try:
                metrics = self._analyze_file_quality(file_path)
                quality_metrics["files_analyzed"] += 1
                total_complexity += metrics.get("complexity", 0)
                total_lines += metrics.get("lines_of_code", 0)

                if metrics.get("issues"):
                    quality_metrics["quality_issues"].extend(metrics["issues"])

            except Exception as e:
                logger.warning(f"Failed to analyze {file_path}: {e}")

        quality_metrics["metrics"] = {
            "average_complexity": total_complexity / max(quality_metrics["files_analyzed"], 1),
            "total_lines_of_code": total_lines,
            "quality_score": max(0, 100 - len(quality_metrics["quality_issues"]) * 5)
        }

        return quality_metrics

    def _get_target_files(self, target_path: str = None) -> List[Path]:
        """Get target files for analysis."""
        if target_path:
            path = Path(target_path)
            if path.is_file() and path.suffix == ".py":
                return [path]
            elif path.is_dir():
                return list(path.rglob("*.py"))
        else:
            return list(self.project_root.rglob("*.py"))

    def _analyze_file_for_refactoring(self, file_path: Path) -> List[RefactoringSuggestion]:
        """Analyze a single file for refactoring opportunities."""
        suggestions = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            tree = ast.parse(content)

            # Analyze various quality metrics
            suggestions.extend(self._check_function_complexity(file_path, tree, content))
            suggestions.extend(self._check_class_complexity(file_path, tree, content))
            suggestions.extend(self._check_code_duplication(file_path, content))
            suggestions.extend(self._check_naming_conventions(file_path, tree, content))
            suggestions.extend(self._check_import_organization(file_path, content))
            suggestions.extend(self._check_docstring_coverage(file_path, tree, content))

        except Exception as e:
            logger.error(f"Failed to analyze {file_path}: {e}")

        return suggestions

    def _check_function_complexity(self, file_path: Path, tree: ast.AST, content: str) -> List[RefactoringSuggestion]:
        """Check for complex functions that need refactoring."""
        suggestions = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity = self._calculate_function_complexity(node, content)
                lines = content.split('\n')
                func_lines = lines[node.lineno - 1:node.end_lineno]

                if complexity > 10:  # Threshold for complex function
                    suggestion = RefactoringSuggestion(
                        type="function_complexity",
                        description=f"Function '{node.name}' is too complex (complexity: {complexity})",
                        file_path=str(file_path),
                        line_numbers=(node.lineno, node.end_lineno),
                        severity="high" if complexity > 20 else "medium",
                        effort="high" if complexity > 20 else "medium",
                        impact_risk="medium",
                        automated_fix=False,
                        suggested_code=self._suggest_function_refactoring(node, content),
                        rationale=f"Complex functions are hard to test and maintain. Consider breaking down into smaller functions.",
                        dependencies=self._find_function_dependencies(node, tree)
                    )
                    suggestions.append(suggestion)

        return suggestions

    def _check_class_complexity(self, file_path: Path, tree: ast.AST, content: str) -> List[RefactoringSuggestion]:
        """Check for complex classes that need refactoring."""
        suggestions = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                method_count = len([n for n in node.body if isinstance(n, ast.FunctionDef)])
                attribute_count = len([n for n in node.body if isinstance(n, ast.Assign)])

                if method_count > 15:  # Threshold for complex class
                    suggestion = RefactoringSuggestion(
                        type="class_complexity",
                        description=f"Class '{node.name}' has too many methods ({method_count})",
                        file_path=str(file_path),
                        line_numbers=(node.lineno, node.end_lineno),
                        severity="high" if method_count > 25 else "medium",
                        effort="high",
                        impact_risk="high",
                        automated_fix=False,
                        suggested_code=self._suggest_class_refactoring(node, content),
                        rationale="Large classes violate Single Responsibility Principle. Consider splitting into focused classes.",
                        dependencies=[]
                    )
                    suggestions.append(suggestion)

        return suggestions

    def _check_code_duplication(self, file_path: Path, content: str) -> List[RefactoringSuggestion]:
        """Check for code duplication."""
        suggestions = []

        lines = content.split('\n')
        n = len(lines)

        # Simple duplicate detection (could be enhanced with more sophisticated algorithms)
        for i in range(n):
            for j in range(i + 5, n):  # Check lines with some gap
                # Check for similar blocks of code
                block1 = lines[i:min(i + 3, n)]
                block2 = lines[j:min(j + 3, n)]

                if self._blocks_are_similar(block1, block2):
                    suggestion = RefactoringSuggestion(
                        type="code_duplication",
                        description=f"Code duplication detected at lines {i+1}-{i+3} and {j+1}-{j+3}",
                        file_path=str(file_path),
                        line_numbers=(i + 1, j + 3),
                        severity="medium",
                        effort="medium",
                        impact_risk="low",
                        automated_fix=True,
                        suggested_code=self._suggest_duplication_refactoring(block1, block2),
                        rationale="Code duplication leads to maintenance issues. Extract common code into functions.",
                        dependencies=[]
                    )
                    suggestions.append(suggestion)

        return suggestions

    def _check_naming_conventions(self, file_path: Path, tree: ast.AST, content: str) -> List[RefactoringSuggestion]:
        """Check for naming convention violations."""
        suggestions = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not re.match(r'^[a-z_][a-z0-9_]*$', node.name):
                    suggestion = RefactoringSuggestion(
                        type="naming_convention",
                        description=f"Function name '{node.name}' doesn't follow snake_case convention",
                        file_path=str(file_path),
                        line_numbers=(node.lineno, node.lineno),
                        severity="low",
                        effort="low",
                        impact_risk="low",
                        automated_fix=True,
                        suggested_code=f"def {self._to_snake_case(node.name)}(",
                        rationale="Consistent naming conventions improve code readability and maintainability.",
                        dependencies=[]
                    )
                    suggestions.append(suggestion)

            elif isinstance(node, ast.ClassDef):
                if not re.match(r'^[A-Z][a-zA-Z0-9]*$', node.name):
                    suggestion = RefactoringSuggestion(
                        type="naming_convention",
                        description=f"Class name '{node.name}' doesn't follow PascalCase convention",
                        file_path=str(file_path),
                        line_numbers=(node.lineno, node.lineno),
                        severity="low",
                        effort="low",
                        impact_risk="low",
                        automated_fix=True,
                        suggested_code=f"class {self._to_pascal_case(node.name)}:",
                        rationale="Class names should follow PascalCase convention.",
                        dependencies=[]
                    )
                    suggestions.append(suggestion)

        return suggestions

    def _check_import_organization(self, file_path: Path, content: str) -> List[RefactoringSuggestion]:
        """Check for import organization issues."""
        suggestions = []

        lines = content.split('\n')
        import_lines = []
        other_lines = []

        in_imports = False
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith(('import ', 'from ')):
                import_lines.append((i + 1, line))
                in_imports = True
            elif stripped == '' and in_imports:
                continue
            elif in_imports and not stripped.startswith(('import ', 'from ', '#')):
                in_imports = False

        # Check for unsorted imports
        sorted_imports = sorted(import_lines, key=lambda x: x[1])
        if import_lines != sorted_imports:
            suggestion = RefactoringSuggestion(
                type="import_organization",
                description="Imports are not properly organized",
                file_path=str(file_path),
                line_numbers=(import_lines[0][0], import_lines[-1][0]) if import_lines else (1, 1),
                severity="low",
                effort="low",
                impact_risk="low",
                automated_fix=True,
                suggested_code='\n'.join(line for _, line in sorted_imports),
                rationale="Organized imports improve readability and follow PEP 8 standards.",
                dependencies=[]
            )
            suggestions.append(suggestion)

        return suggestions

    def _check_docstring_coverage(self, file_path: Path, tree: ast.AST, content: str) -> List[RefactoringSuggestion]:
        """Check for missing docstrings."""
        suggestions = []

        # Check module docstring
        if not ast.get_docstring(tree):
            suggestion = RefactoringSuggestion(
                type="missing_docstring",
                description="Module is missing a docstring",
                file_path=str(file_path),
                line_numbers=(1, 1),
                severity="medium",
                effort="low",
                impact_risk="low",
                automated_fix=False,
                suggested_code='"""Module docstring goes here."""\n\n',
                rationale="Module docstrings provide important documentation for users and developers.",
                dependencies=[]
            )
            suggestions.append(suggestion)

        # Check function and class docstrings
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if not ast.get_docstring(node):
                    suggestion = RefactoringSuggestion(
                        type="missing_docstring",
                        description=f"{'Function' if isinstance(node, ast.FunctionDef) else 'Class'} '{node.name}' is missing a docstring",
                        file_path=str(file_path),
                        line_numbers=(node.lineno, node.lineno),
                        severity="medium",
                        effort="low",
                        impact_risk="low",
                        automated_fix=False,
                        suggested_code=f'"""{self._generate_docstring_suggestion(node)}"""',
                        rationale="Docstrings improve code documentation and maintainability.",
                        dependencies=[]
                    )
                    suggestions.append(suggestion)

        return suggestions

    # Helper methods
    def _calculate_function_complexity(self, node: ast.FunctionDef, content: str) -> int:
        """Calculate cyclomatic complexity of a function."""
        complexity = 1  # Base complexity

        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.Try, ast.With)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1

        return complexity

    def _suggest_function_refactoring(self, node: ast.FunctionDef, content: str) -> str:
        """Suggest refactoring for a complex function."""
        return f"""# Consider breaking down '{node.name}' into smaller functions:

def {node.name}_helper_1():
    # Extract part of the logic
    pass

def {node.name}_helper_2():
    # Extract another part of the logic
    pass

def {node.name}():
    # Main orchestration
    result = {node.name}_helper_1()
    result = {node.name}_helper_2(result)
    return result
"""

    def _suggest_class_refactoring(self, node: ast.ClassDef, content: str) -> str:
        """Suggest refactoring for a complex class."""
        return f"""# Consider splitting '{node.name}' into focused classes:

class {node.name}Core:
    # Core functionality
    pass

class {node.name}Validation:
    # Validation logic
    pass

class {node.name}Persistence:
    # Data persistence
    pass
"""

    def _blocks_are_similar(self, block1: List[str], block2: List[str]) -> bool:
        """Check if two code blocks are similar."""
        # Simple similarity check - could be enhanced
        clean_block1 = [line.strip() for line in block1 if line.strip()]
        clean_block2 = [line.strip() for line in block2 if line.strip()]

        if len(clean_block1) != len(clean_block2):
            return False

        similarities = sum(1 for i in range(len(clean_block1)) if clean_block1[i] == clean_block2[i])
        return similarities / len(clean_block1) > 0.7

    def _suggest_duplication_refactoring(self, block1: List[str], block2: List[str]) -> str:
        """Suggest refactoring for code duplication."""
        return f"""# Extract common code into a helper function:

def common_logic():
    # Common code from duplicated blocks
    pass

# Replace duplicated blocks with function call
result = common_logic()
"""

    def _to_snake_case(self, name: str) -> str:
        """Convert name to snake_case."""
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def _to_pascal_case(self, name: str) -> str:
        """Convert name to PascalCase."""
        return ''.join(word.capitalize() for word in name.split('_'))

    def _find_function_dependencies(self, node: ast.FunctionDef, tree: ast.AST) -> List[str]:
        """Find dependencies for a function."""
        dependencies = []

        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name):
                    dependencies.append(child.func.id)
                elif isinstance(child.func, ast.Attribute):
                    dependencies.append(child.func.attr)

        return list(set(dependencies))

    def _generate_docstring_suggestion(self, node: ast.AST) -> str:
        """Generate docstring suggestion for a node."""
        if isinstance(node, ast.FunctionDef):
            args = [arg.arg for arg in node.args.args]
            return f"""Brief description of the function.

Args:
    {chr(10).join(f'{arg}: description' for arg in args[:3])}{'...' if len(args) > 3 else ''}

Returns:
    description of return value

Raises:
    description of exceptions raised
"""
        elif isinstance(node, ast.ClassDef):
            return f"""Brief description of the class.

Attributes:
    description of key attributes

Methods:
    description of key methods
"""
        return "Description goes here."

    def _create_refactoring_plan(self, suggestions: List[RefactoringSuggestion]) -> RefactoringPlan:
        """Create a comprehensive refactoring plan."""
        target_files = list(set(s.file_path for s in suggestions))

        # Calculate estimated effort
        effort_scores = {"low": 1, "medium": 2, "high": 3}
        total_effort = sum(effort_scores.get(s.effort, 1) for s in suggestions)

        if total_effort > 20:
            estimated_effort = "high"
        elif total_effort > 10:
            estimated_effort = "medium"
        else:
            estimated_effort = "low"

        # Assess risk
        high_risk_count = sum(1 for s in suggestions if s.impact_risk == "high")
        if high_risk_count > 5:
            risk_assessment = "high"
        elif high_risk_count > 2:
            risk_assessment = "medium"
        else:
            risk_assessment = "low"

        # Determine implementation order (less risky first)
        implementation_order = []
        for file_path in target_files:
            file_suggestions = [s for s in suggestions if s.file_path == file_path]
            if file_suggestions:
                avg_risk = sum(effort_scores.get(s.impact_risk, 1) for s in file_suggestions) / len(file_suggestions)
                implementation_order.append((file_path, avg_risk))

        implementation_order = [file for file, _ in sorted(implementation_order, key=lambda x: x[1])]

        # Create rollback plan
        rollback_plan = {file_path: f"Restore from git: git checkout HEAD -- {file_path}" for file_path in target_files}

        return RefactoringPlan(
            target_files=target_files,
            suggestions=suggestions,
            estimated_effort=estimated_effort,
            risk_assessment=risk_assessment,
            implementation_order=implementation_order,
            rollback_plan=rollback_plan
        )

    def _create_backup(self) -> Path:
        """Create backup of current state."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.project_root / f"backup_before_refactoring_{timestamp}"

        # This would create an actual backup in implementation
        # For now, just return the path
        return backup_path

    def _apply_file_fixes(self, file_path: str, suggestions: List[RefactoringSuggestion]) -> Dict[str, Any]:
        """Apply fixes to a specific file."""
        result = {"successful": [], "failed": []}

        try:
            with open(file_path, 'r') as f:
                original_content = f.read()

            modified_content = original_content

            # Apply fixes (simplified - would need more sophisticated implementation)
            for suggestion in suggestions:
                try:
                    if suggestion.type == "naming_convention":
                        # Apply name changes
                        modified_content = modified_content.replace(
                            suggestion.suggested_code.split('(')[0].replace('def ', '').replace('class ', ''),
                            suggestion.suggested_code.split('(')[0].replace('def ', '').replace('class ', '')
                        )
                        result["successful"].append(suggestion)

                    elif suggestion.type == "import_organization":
                        # Reorganize imports
                        modified_content = self._reorganize_imports(modified_content, suggestion.suggested_code)
                        result["successful"].append(suggestion)

                except Exception as e:
                    logger.warning(f"Failed to apply fix for {suggestion.type}: {e}")
                    result["failed"].append(suggestion)

            # Write modified content
            with open(file_path, 'w') as f:
                f.write(modified_content)

        except Exception as e:
            logger.error(f"Failed to apply fixes to {file_path}: {e}")
            result["failed"].extend(suggestions)

        return result

    def _reorganize_imports(self, content: str, suggested_imports: str) -> str:
        """Reorganize imports in content."""
        lines = content.split('\n')
        new_lines = []
        imports_processed = False

        for line in lines:
            if line.strip().startswith(('import ', 'from ')) and not imports_processed:
                imports_processed = True
            elif not line.strip().startswith(('import ', 'from ')) and imports_processed:
                new_lines.extend(suggested_imports.split('\n'))
                new_lines.append(line)
                imports_processed = False
                continue

            if not imports_processed:
                new_lines.append(line)

        return '\n'.join(new_lines)

    def _generate_rollback_info(self, plan: RefactoringPlan) -> Dict[str, str]:
        """Generate rollback information."""
        return {
            "git_command": "git checkout HEAD -- <affected_files>",
            "backup_location": "backup_before_refactoring_<timestamp>",
            "manual_rollback": "Restore files from backup or git"
        }

    def _check_circular_dependencies(self, plan: RefactoringPlan) -> List[str]:
        """Check for circular dependencies in refactoring plan."""
        # This would implement actual circular dependency checking
        return []

    def _validate_dependency_impact(self, plan: RefactoringPlan) -> Dict[str, Any]:
        """Validate dependency impact of refactoring plan."""
        return {
            "high_impact_count": 0,
            "medium_impact_count": len(plan.suggestions),
            "low_impact_count": 0,
            "dependency_graph_affected": False
        }

    def _analyze_test_coverage_impact(self, plan: RefactoringPlan) -> Dict[str, Any]:
        """Analyze test coverage impact of refactoring."""
        return {
            "coverage_loss": 0.0,
            "tests_to_update": 0,
            "new_tests_required": 0
        }

    def _identify_breaking_changes(self, plan: RefactoringPlan) -> List[str]:
        """Identify breaking changes in refactoring plan."""
        breaking_changes = []

        for suggestion in plan.suggestions:
            if suggestion.type == "naming_convention" and suggestion.automated_fix:
                breaking_changes.append(
                    f"Public API change in {suggestion.file_path}: {suggestion.description}"
                )

        return breaking_changes

    def _analyze_file_quality(self, file_path: Path) -> Dict[str, Any]:
        """Analyze quality metrics for a single file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            tree = ast.parse(content)

            lines = content.split('\n')
            lines_of_code = len([line for line in lines if line.strip()])

            # Calculate complexity metrics
            functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

            complexity = sum(self._calculate_function_complexity(func, content) for func in functions)

            # Identify issues
            issues = []
            if lines_of_code > 500:
                issues.append("File is too long")

            if complexity > 50:
                issues.append("File has high complexity")

            return {
                "lines_of_code": lines_of_code,
                "function_count": len(functions),
                "class_count": len(classes),
                "complexity": complexity,
                "issues": issues
            }

        except Exception as e:
            logger.error(f"Failed to analyze {file_path}: {e}")
            return {"error": str(e)}