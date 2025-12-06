"""
Validation script for dataeng_toolbox package.

This script validates that the package is properly structured and ready for publishing.
"""

import os
import sys
import importlib.util
from pathlib import Path


def check_file_exists(filepath: str, description: str) -> bool:
    """Check if a required file exists."""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ Missing {description}: {filepath}")
        return False


def check_package_import() -> bool:
    """Test if the package can be imported."""
    try:
        sys.path.insert(0, os.getcwd())
        from dataeng_toolbox import Core

        # Test basic functionality
        core = Core()
        message = core.hello_world()
        info = core.get_info()

        print(f"✅ Package import successful")
        print(f"   Hello message: {message}")
        print(f"   Package info: {info['name']} v{info['version']}")
        return True
    except Exception as e:
        print(f"❌ Package import failed: {e}")
        return False


def check_tests() -> bool:
    """Check if tests can run."""
    try:
        import subprocess
        result = subprocess.run([sys.executable, '-m', 'pytest', 'tests/', '-v'],
                              capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ Tests passed")
            # Count test results
            lines = result.stdout.split('\n')
            for line in lines:
                if 'passed' in line and '=' in line:
                    print(f"   {line.strip()}")
            return True
        else:
            print(f"❌ Tests failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Could not run tests: {e}")
        return False


def check_build_artifacts() -> bool:
    """Check if build artifacts exist."""
    wheel_files = list(Path('dist').glob('*.whl'))
    tar_files = list(Path('dist').glob('*.tar.gz'))

    if wheel_files and tar_files:
        print("✅ Build artifacts found:")
        for file in wheel_files + tar_files:
            print(f"   {file}")
        return True
    else:
        print("❌ Build artifacts missing. Run 'python build_package.py' first.")
        return False


def validate_package_structure() -> bool:
    """Validate the overall package structure."""
    print("DataEng Toolbox Package Validation")
    print("=" * 40)

    checks = []

    # Required files
    checks.append(check_file_exists("pyproject.toml", "Build configuration"))
    checks.append(check_file_exists("README.md", "README file"))
    checks.append(check_file_exists("LICENSE", "License file"))
    checks.append(check_file_exists("dataeng_toolbox/__init__.py", "Package init"))
    checks.append(check_file_exists("dataeng_toolbox/core.py", "Core module"))
    checks.append(check_file_exists("tests/test_core.py", "Test files"))
    checks.append(check_file_exists("examples/basic_usage.py", "Example files"))
    checks.append(check_file_exists(".github/workflows/ci-cd.yml", "GitHub Actions"))

    # Package functionality
    checks.append(check_package_import())
    checks.append(check_tests())

    # Build artifacts (optional)
    if os.path.exists('dist'):
        checks.append(check_build_artifacts())
    else:
        print("ℹ️  No dist/ directory found. Run 'python build_package.py' to create build artifacts.")

    print("\n" + "=" * 40)

    passed = sum(checks)
    total = len(checks)

    if passed == total:
        print(f"✅ All checks passed ({passed}/{total})")
        print("\n🎉 Package is ready for publishing!")
        print("\nNext steps:")
        print("1. Run 'python build_package.py' to build the package")
        print("2. Follow the instructions in PUBLISHING.md to publish to PyPI")
        return True
    else:
        print(f"❌ Some checks failed ({passed}/{total})")
        print("\n🔧 Please fix the issues above before publishing.")
        return False


def main():
    """Main validation function."""
    return validate_package_structure()


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
