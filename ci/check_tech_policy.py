import json
import toml
import xml.etree.ElementTree as ET
import sys
import subprocess
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Tuple
import re

@dataclass
class Dependency:
    """Unified dependency representation across ecosystems"""
    name: str
    version: str
    ecosystem: str
    license: str = "unknown"
    implementations: int = 1
    vendor_specific: bool = False
    documentation: bool = False
    migration_path: bool = False

    def __hash__(self):
        return hash((self.name, self.ecosystem))

class LicenseFetcher:
    """Fetches real license data using external tools"""

    @staticmethod
    def fetch_python_licenses() -> Dict[str, str]:
        """Runs pip-licenses to get licenses for installed Python packages"""
        licenses = {}
        print("🔍 Fetching Python licenses using pip-licenses...")
        try:
            # Install dependencies first
            if Path("pyproject.toml").exists():
                subprocess.run(["pip", "install", "poetry"], check=True, capture_output=True, text=True)
                subprocess.run(["poetry", "install", "--no-root"], check=True, capture_output=True, text=True)
            elif Path("requirements.txt").exists():
                subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True, capture_output=True, text=True)

            # Now get licenses
            result = subprocess.run(
                ["pip-licenses", "--format=json"],
                capture_output=True, text=True, check=True
            )
            data = json.loads(result.stdout)
            for item in data:
                licenses[item['Name'].lower()] = item['License']
            print(f"✅ Found {len(licenses)} Python licenses.")
        except subprocess.CalledProcessError as e:
            print(f"⚠ Warning: Failed to fetch Python licenses. Poetry install failed: {e}")
            print(f"Stderr: {e.stderr}")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"⚠ Warning: Failed to process Python licenses: {e}")
        return licenses

    @staticmethod
    def fetch_nodejs_licenses() -> Dict[str, str]:
        """Runs license-checker for Node.js packages"""
        licenses = {}
        print("🔍 Fetching Node.js licenses using license-checker...")
        try:
            # Install dependencies first
            subprocess.run(["npm", "install"], check=True, capture_output=True, text=True)

            # Now get licenses
            result = subprocess.run(
                ["./node_modules/.bin/license-checker", "--json"],
                capture_output=True, text=True, check=True
            )
            data = json.loads(result.stdout)
            for name_version, info in data.items():
                name = name_version.rsplit('@', 1)[0]
                licenses[name] = info.get('licenses', 'unknown')
            print(f"✅ Found {len(licenses)} Node.js licenses.")
        except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError) as e:
            print(f"⚠ Warning: Failed to fetch Node.js licenses: {e}")
        return licenses

class DependencyParser:
    """Parse dependencies and enrich with real and supplemental data"""

    OSI_APPROVED = [
        "MIT", "Apache-2.0", "Apache License 2.0",
        "BSD-3-Clause", "BSD-2-Clause",
        "GPL-3.0", "GPL-3.0-or-later", "LGPL-3.0",
        "ISC", "MPL-2.0", "CDDL-1.0", "EPL-1.0"
    ]

    @staticmethod
    def parse_python_dependencies() -> List[Dependency]:
        deps = []
        pyproject_path = Path("pyproject.toml")
        if pyproject_path.exists():
            try:
                config = toml.load(pyproject_path)
                py_deps = config.get('tool', {}).get('poetry', {}).get('dependencies', {})
                for name, spec in py_deps.items():
                    if name.lower() == "python": continue
                    version = spec if isinstance(spec, str) else spec.get("version", "*")
                    deps.append(Dependency(name=name.lower(), version=version, ecosystem="python"))
            except Exception as e:
                print(f"⚠ Warning: Failed to parse pyproject.toml: {e}")
        return deps

    @staticmethod
    def parse_nodejs_dependencies() -> List[Dependency]:
        deps = []
        package_path = Path("package.json")
        if not package_path.exists(): return deps
        try:
            with open(package_path, 'r') as f:
                package_json = json.load(f)
            for name, version in package_json.get('dependencies', {}).items():
                deps.append(Dependency(name=name, version=version, ecosystem="nodejs"))
            for name, version in package_json.get('devDependencies', {}).items():
                deps.append(Dependency(name=name, version=version, ecosystem="nodejs"))
        except Exception as e:
            print(f"⚠ Warning: Failed to parse package.json: {e}")
        return deps

    @staticmethod
    def parse_java_dependencies() -> List[Dependency]:
        deps = []
        pom_path = Path("pom.xml")
        if not pom_path.exists(): return deps
        try:
            tree = ET.parse(pom_path)
            root = tree.getroot()
            namespace = root.tag.split('}')[0][1:] if '}' in root.tag else ''
            ns_map = {'m': namespace} if namespace else {}

            def find_all_in_ns(element, path):
                return element.findall(path, ns_map) if namespace else element.findall(path.replace('m:', ''))

            def find_in_ns(element, path):
                return element.find(path, ns_map) if namespace else element.find(path.replace('m:', ''))

            for dep_node in find_all_in_ns(root, './/m:dependency'):
                scope = find_in_ns(dep_node, 'm:scope')
                if scope is not None and scope.text == 'test': continue

                group_id = (find_in_ns(dep_node, 'm:groupId') or ET.Element("")).text
                artifact_id = (find_in_ns(dep_node, 'm:artifactId') or ET.Element("")).text
                version = (find_in_ns(dep_node, 'm:version') or ET.Element("")).text or "*"

                if artifact_id:
                    full_name = f"{group_id}:{artifact_id}"
                    deps.append(Dependency(name=full_name, version=version, ecosystem="java"))
        except Exception as e:
            print(f"⚠ Warning: Failed to parse pom.xml: {e}")
        return deps

    @staticmethod
    def load_supplemental_metadata() -> Dict:
        metadata_path = Path("ci/dependency_metadata.json")
        if not metadata_path.exists(): return {}
        try:
            with open(metadata_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    @staticmethod
    def load_all_dependencies() -> List[Dependency]:
        # Fetch real license data
        python_licenses = LicenseFetcher.fetch_python_licenses()
        nodejs_licenses = LicenseFetcher.fetch_nodejs_licenses()

        # Parse dependency lists from manifests
        all_deps = []
        all_deps.extend(DependencyParser.parse_python_dependencies())
        all_deps.extend(DependencyParser.parse_nodejs_dependencies())
        all_deps.extend(DependencyParser.parse_java_dependencies())

        # Load supplemental (manual) metadata
        supplemental_meta = DependencyParser.load_supplemental_metadata()

        # Enrich dependencies with fetched and supplemental data
        for dep in all_deps:
            # Set real license data
            if dep.ecosystem == "python":
                dep.license = python_licenses.get(dep.name, "unknown")
            elif dep.ecosystem == "nodejs":
                dep.license = nodejs_licenses.get(dep.name, "unknown")

            # Apply supplemental metadata
            eco_meta = supplemental_meta.get(dep.ecosystem, {})
            dep_meta = eco_meta.get(dep.name, {})
            dep.implementations = dep_meta.get("implementations", 1)
            dep.vendor_specific = dep_meta.get("vendor_specific", False)
            dep.documentation = dep_meta.get("documentation", False)
            dep.migration_path = dep_meta.get("migration_path", False)

        # Deduplicate
        seen = set()
        unique_deps = [d for d in all_deps if (d.name, d.ecosystem) not in seen and not seen.add((d.name, d.ecosystem))]
        return unique_deps

class PolicyEnforcer:
    @staticmethod
    def check_license(dep: Dependency) -> Tuple[bool, str]:
        if dep.license == "unknown":
            return False, f"License unknown for {dep.name}"
        if dep.license not in DependencyParser.OSI_APPROVED:
            return False, f"{dep.name}: License '{dep.license}' not OSI-approved"
        return True, f"✓ {dep.name}: License compliant"

    @staticmethod
    def check_implementations(dep: Dependency) -> Tuple[bool, str]:
        if dep.implementations < 2:
            return False, f"{dep.name}: Only {dep.implementations} implementation(s) found (need ≥2)"
        return True, f"✓ {dep.name}: Multiple implementations verified"

    @staticmethod
    def check_vendor_lock_in(dep: Dependency) -> Tuple[bool, str]:
        if not dep.vendor_specific:
            return True, f"✓ {dep.name}: Not vendor-specific"
        if not (dep.documentation and dep.migration_path):
            missing = [p for p, v in [("documentation", dep.documentation), ("migration path", dep.migration_path)] if not v]
            return False, f"{dep.name}: Vendor-specific but missing {', '.join(missing)}"
        return True, f"✓ {dep.name}: Vendor-specific with migration path & docs"

    @staticmethod
    def check_ecosystem_diversity(deps: List[Dependency]) -> Tuple[bool, str]:
        eco_counts = {}
        for dep in deps: eco_counts[dep.ecosystem] = eco_counts.get(dep.ecosystem, 0) + 1
        total = len(deps)
        warnings = [f"{eco}: {(count/total*100):.0f}%" for eco, count in eco_counts.items() if (count/total) > 0.7]
        if warnings:
            return False, f"Ecosystem concentration risk: {', '.join(warnings)}"
        return True, "✓ Ecosystem diversity acceptable"

class Report:
    def __init__(self):
        self.violations = []
        self.warnings = []
        self.passed = []

    def add(self, passed: bool, msg: str, is_violation: bool):
        if passed: self.passed.append(msg)
        elif is_violation: self.violations.append(msg)
        else: self.warnings.append(msg)

    def print_report(self):
        print("\n" + "="*70 + "\nTECHNOLOGY POLICY COMPLIANCE REPORT\n" + "="*70 + "\n")
        if self.passed: print(f"✅ PASSED CHECKS ({len(self.passed)} total)\n")
        if self.warnings:
            print("⚠ WARNINGS:")
            for msg in self.warnings: print(f"   {msg}")
            print()
        if self.violations:
            print("❌ VIOLATIONS (CI WILL FAIL):")
            for msg in self.violations: print(f"   {msg}")
            print()
            return False
        print("✅ ALL COMPLIANCE CHECKS PASSED\n")
        return True

def main():
    print("🔍 Scanning and verifying dependencies...\n")
    deps = DependencyParser.load_all_dependencies()

    if not deps:
        print("⚠ No dependencies found. Skipping policy checks.")
        sys.exit(0)

    print(f"Found {len(deps)} unique dependencies.\n")

    report = Report()
    for dep in deps:
        passed, msg = PolicyEnforcer.check_license(dep)
        report.add(passed, msg, is_violation=True)

        passed, msg = PolicyEnforcer.check_implementations(dep)
        report.add(passed, msg, is_violation=False) # This is a warning

        passed, msg = PolicyEnforcer.check_vendor_lock_in(dep)
        report.add(passed, msg, is_violation=True)

    passed, msg = PolicyEnforcer.check_ecosystem_diversity(deps)
    report.add(passed, msg, is_violation=False) # This is a warning

    success = report.print_report()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
