#!/usr/bin/env python3

import os
import sys
import json
import toml
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Tuple, Set
from xml.etree import ElementTree

# 1. Dependency Dataclass
@dataclass
class Dependency:
    name: str
    version: str
    ecosystem: str
    license: str = "unknown"
    implementations: int = 1
    vendor_specific: bool = False
    documentation: bool = False
    migration_path: bool = False
    scope: str = ""
    source: str = ""

# 2. Parsing Methods
class DependencyParser:
    def parse(self, project_root: Path) -> List[Dependency]:
        all_deps = []
        all_deps.extend(self._parse_python(project_root))
        all_deps.extend(self._parse_node(project_root))
        all_deps.extend(self._parse_java(project_root))
        return self._deduplicate(all_deps)

    def _parse_python(self, project_root: Path) -> List[Dependency]:
        deps = []
        # Poetry
        pyproject_path = project_root / "pyproject.toml"
        if pyproject_path.exists():
            pyproject = toml.load(pyproject_path)
            py_deps = pyproject.get('tool', {}).get('poetry', {}).get('dependencies', {})
            for name, version in py_deps.items():
                if name != "python":
                    deps.append(Dependency(name=name, version=version if isinstance(version, str) else version.get("version", "*"), ecosystem="Python", source="PyPI"))
        # requirements.txt
        req_path = project_root / "requirements.txt"
        if req_path.exists():
            with open(req_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        # More robust parsing for different version specifiers
                        for spec in ['==', '>=', '<=', '~=', '>', '<']:
                            if spec in line:
                                parts = line.split(spec)
                                deps.append(Dependency(name=parts[0], version=parts[1] if len(parts) > 1 else "*", ecosystem="Python", source="PyPI"))
                                break
                        else:
                            deps.append(Dependency(name=line, version="*", ecosystem="Python", source="PyPI"))
        return deps

    def _parse_node(self, project_root: Path) -> List[Dependency]:
        deps = []
        package_json_path = project_root / "package.json"
        if package_json_path.exists():
            with open(package_json_path, "r") as f:
                package_json = json.load(f)
                for name, version in package_json.get('dependencies', {}).items():
                    deps.append(Dependency(name=name, version=version, ecosystem="Node.js", source="npm"))
                for name, version in package_json.get('devDependencies', {}).items():
                    deps.append(Dependency(name=name, version=version, ecosystem="Node.js", source="npm", scope="development"))
        return deps

    def _parse_java(self, project_root: Path) -> List[Dependency]:
        deps = []
        pom_path = project_root / "pom.xml"
        if pom_path.exists():
            try:
                tree = ElementTree.parse(pom_path)
                root = tree.getroot()
                ns = {'m': 'http://maven.apache.org/POM/4.0.0'}

                # Parse dependencyManagement to resolve versions
                managed_versions = {}
                dep_management = root.find('.//m:dependencyManagement', ns)
                if dep_management is not None:
                    managed_deps = dep_management.findall('.//m:dependency', ns)
                    for dep in managed_deps:
                        groupId = dep.find('m:groupId', ns).text
                        artifactId = dep.find('m:artifactId', ns).text
                        version_element = dep.find('m:version', ns)
                        if version_element is not None:
                            managed_versions[f"{groupId}:{artifactId}"] = version_element.text

                # Find all dependencies
                dependencies = root.findall('.//m:dependencies/m:dependency', ns)
                for dep in dependencies:
                    groupId = dep.find('m:groupId', ns).text
                    artifactId = dep.find('m:artifactId', ns).text
                    dep_name = f"{groupId}:{artifactId}"

                    version_element = dep.find('m:version', ns)
                    version = version_element.text if version_element is not None else managed_versions.get(dep_name, "")

                    scope_element = dep.find('m:scope', ns)
                    scope = scope_element.text if scope_element is not None else "compile"

                    if scope != "test":
                        deps.append(Dependency(name=dep_name, version=version, ecosystem="Java", source="Maven Central", scope=scope))
            except ElementTree.ParseError as e:
                print(f"Warning: Could not parse {pom_path}. Error: {e}", file=sys.stderr)
        return deps

    def _deduplicate(self, deps: List[Dependency]) -> List[Dependency]:
        unique_deps = {}
        for dep in deps:
            key = (dep.name, dep.ecosystem)
            if key not in unique_deps:
                unique_deps[key] = dep
        return list(unique_deps.values())

# 3. Policy Enforcement
class PolicyEnforcer:
    def __init__(self, exceptions: Dict):
        self.exceptions = exceptions
        self.osi_approved_licenses = {"MIT", "GPL-3.0", "Apache-2.0", "BSD-3-Clause"} # Abridged list

    def check(self, dep: Dependency) -> List[Tuple[str, str]]:
        violations = []

        # Apply overrides from exceptions
        exception_info = self.exceptions.get(dep.name, {})
        if "overrides" in exception_info:
            for key, value in exception_info["overrides"].items():
                if hasattr(dep, key):
                    setattr(dep, key, value)

        # Check for exceptions
        if exception_info.get("ignore_all", False):
            return []

        violations.extend(self._check_license(dep))
        violations.extend(self._check_implementations(dep))
        violations.extend(self._check_vendor_lock_in(dep))

        return violations

    def _check_license(self, dep: Dependency) -> List[Tuple[str, str]]:
        if dep.license == "unknown":
            return [("License", f"License unknown for {dep.name}")]
        if dep.license not in self.osi_approved_licenses:
             return [("License", f"License '{dep.license}' for {dep.name} is not OSI approved.")]
        return []

    def _check_implementations(self, dep: Dependency) -> List[Tuple[str, str]]:
        if dep.implementations < 2:
            return [("Implementations", f"{dep.name} has only {dep.implementations} implementation(s).")]
        return []

    def _check_vendor_lock_in(self, dep: Dependency) -> List[Tuple[str, str]]:
        if dep.vendor_specific and not (dep.documentation and dep.migration_path):
            return [("Vendor Lock-in", f"{dep.name} is vendor-specific without a clear documentation or migration path.")]
        return []

    def check_ecosystem_diversity(self, deps: List[Dependency]) -> List[Tuple[str, str]]:
        ecosystem_counts = {}
        for dep in deps:
            ecosystem_counts[dep.ecosystem] = ecosystem_counts.get(dep.ecosystem, 0) + 1

        total_deps = len(deps)
        warnings = []
        for ecosystem, count in ecosystem_counts.items():
            if total_deps > 0 and (count / total_deps) > 0.7:
                warnings.append(("Ecosystem Diversity", f"Over 70% of dependencies are from the {ecosystem} ecosystem."))
        return warnings

# 4. Report Generation
class Report:
    def __init__(self):
        self.passed = []
        self.warnings = []
        self.violations = []

    def add_result(self, dep: Dependency, violations: List[Tuple[str, str]]):
        if not violations:
            self.passed.append(dep)
        else:
            self.violations.append((dep, violations))

    def add_warning(self, warning: Tuple[str, str]):
        self.warnings.append(warning)
    def print_report(self):
        print("--- Policy Check Report ---")
        if self.violations:
            print("\nViolations:")
            for dep, violations in self.violations:
                print(f"  - {dep.name} ({dep.ecosystem}):")
                for check, msg in violations:
                    print(f"    - [{check}] {msg}")

        if self.warnings:
            print("\nWarnings:")
            for check, msg in self.warnings:
                print(f"  - [{check}] {msg}")

        print(f"\nSummary: {len(self.passed)} passed, {len(self.violations)} violations, {len(self.warnings)} warnings.")

    def to_json(self) -> str:
        return json.dumps({
            "summary": {
                "passed": len(self.passed),
                "violations": len(self.violations),
                "warnings": len(self.warnings),
            },
            "violations": [
                {
                    "dependency": dep.name,
                    "ecosystem": dep.ecosystem,
                    "details": [{"check": v[0], "message": v[1]} for v in violations],
                }
                for dep, violations in self.violations
            ],
            "warnings": [
                {"check": w[0], "message": w[1]} for w in self.warnings
            ],
        }, indent=2)

    def has_violations(self) -> bool:
        return bool(self.violations)

# 5. Main Execution Logic
def main():
    project_root = Path(".")

    # Load exceptions
    exceptions = {}
    exceptions_path = project_root / "policy_exceptions.json"
    if exceptions_path.exists():
        with open(exceptions_path, "r") as f:
            exceptions = json.load(f)

    parser = DependencyParser()
    deps = parser.parse(project_root)

    # Auto-resolve licenses (stub)
    for dep in deps:
        if dep.license == "unknown":
            # In a real implementation, you would call a tool like `pip-licenses`,
            # `npm-license-crawler`, or the Maven License Plugin here.
            pass

    enforcer = PolicyEnforcer(exceptions)
    report = Report()

    for dep in deps:
        violations = enforcer.check(dep)
        report.add_result(dep, violations)

    # Ecosystem diversity check
    ecosystem_warnings = enforcer.check_ecosystem_diversity(deps)
    for warning in ecosystem_warnings:
        report.add_warning(warning)

    report.print_report()

    # Export JSON report
    with open("policy_report.json", "w") as f:
        f.write(report.to_json())

    if report.has_violations():
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
