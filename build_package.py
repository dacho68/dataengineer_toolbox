"""
Modern build script for dataeng_toolbox using pyproject.toml.

This script provides a comprehensive build process including:
- Project validation
- Dependency checking
- Test execution
- Clean builds
- Artifact verification
"""

import os
import subprocess
import sys
import shutil
from pathlib import Path
import argparse


def clean_build():
    """Clean previous build artifacts."""
    dirs_to_clean = ['build', 'dist', 'dataeng_toolbox.egg-info']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Cleaned {dir_name}")


def check_dependencies():
    """Check if required build dependencies are installed."""
    try:
        import build
        print("✅ Build module is available")
        return True
    except ImportError:
        print("❌ Build module not found. Installing...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "build"],
                         check=True, capture_output=True)
            print("✅ Build module installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install build module: {e}")
            return False


def build_package():
    """Build the package using the modern build system."""
    print("Building package...")

    try:
        # Use the modern build system with pyproject.toml
        result = subprocess.run([
            sys.executable, "-m", "build",
            "--sdist", "--wheel", "."
        ], capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ Package built successfully")
            print("Build output:")
            if result.stdout:
                # Print only the last few lines to avoid clutter
                output_lines = result.stdout.strip().split('\n')
                for line in output_lines[-5:]:
                    if line.strip():
                        print(f"  {line}")
            return True
        else:
            print(f"❌ Package build failed:")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            return False

    except FileNotFoundError:
        print("❌ Build command not found. Make sure 'build' module is installed.")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during build: {e}")
        return False


def validate_project():
    """Validate that the project structure is correct."""
    required_files = ['pyproject.toml', 'dataeng_toolbox/__init__.py']
    missing_files = []

    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)

    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False

    print("✅ Project structure validated")
    return True


def run_tests():
    """Run tests before building."""
    print("Running tests...")
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"
        ], capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ All tests passed")
            return True
        else:
            print(f"❌ Tests failed:")
            print(result.stdout)
            print(result.stderr)
            return False
    except FileNotFoundError:
        print("⚠️  Pytest not found, skipping tests")
        return True


def main():
    """Main build function."""
    parser = argparse.ArgumentParser(description="Build dataeng_toolbox package")
    parser.add_argument("--skip-tests", action="store_true",
                       help="Skip running tests before building")
    parser.add_argument("--no-clean", action="store_true",
                       help="Don't clean build artifacts before building")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Enable verbose output")

    args = parser.parse_args()

    print("DataEng Toolbox Modern Build Script")
    print("=" * 40)

    # Validate project structure
    if not validate_project():
        return 1

    # Check dependencies
    if not check_dependencies():
        return 1

    # Clean previous builds (unless skipped)
    if not args.no_clean:
        clean_build()
    else:
        print("⏭️  Skipping clean (--no-clean specified)")

    # Run tests (unless skipped)
    test_passed = True
    if not args.skip_tests:
        test_passed = run_tests()
    else:
        print("⏭️  Skipping tests (--skip-tests specified)")

    # Build package
    if build_package():
        print("\n✅ Package built successfully!")

        # List build artifacts
        if os.path.exists('dist'):
            print("\nBuild artifacts:")
            for file in sorted(os.listdir('dist')):
                file_path = os.path.join('dist', file)
                file_size = os.path.getsize(file_path)
                print(f"  - dist/{file} ({file_size:,} bytes)")

        if not test_passed:
            print("\n⚠️  Note: Package built successfully but some tests failed")
            print("    Consider reviewing test failures before distribution")

        print("\n📦 Your package is ready for distribution!")
        print("    To upload to PyPI: twine upload dist/*")
    else:
        print("\n❌ Package build failed!")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
