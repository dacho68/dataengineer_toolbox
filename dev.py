#!/usr/bin/env python3
"""
Setup script for dataeng_toolbox development.

This script provides common development tasks like building, testing, and publishing.
"""

import subprocess
import sys
import argparse
from pathlib import Path


def run_command(command: str, description: str = None) -> int:
    """Run a shell command and return the exit code."""
    if description:
        print(f"🔄 {description}")

    print(f"   Running: {command}")
    result = subprocess.run(command, shell=True)

    if result.returncode == 0:
        print(f"✅ Success!")
    else:
        print(f"❌ Failed with exit code {result.returncode}")

    return result.returncode


def install_dev():
    """Install the package in development mode."""
    return run_command("pip install -e .[dev]", "Installing package in development mode")


def test():
    """Run the test suite."""
    return run_command("pytest tests/ -v --cov=dataeng_toolbox", "Running test suite")


def lint():
    """Run linting checks."""
    commands = [
        ("flake8 dataeng_toolbox tests", "Running flake8 linting"),
        ("black --check dataeng_toolbox tests examples", "Checking code formatting"),
        ("mypy dataeng_toolbox", "Running type checking"),
    ]

    for command, description in commands:
        exit_code = run_command(command, description)
        if exit_code != 0:
            return exit_code

    return 0


def format_code():
    """Format code with black."""
    return run_command("black dataeng_toolbox tests examples", "Formatting code with black")


def build():
    """Build the package."""
    # Clean previous builds
    run_command("rm -rf dist/ build/ *.egg-info", "Cleaning previous builds")

    # Build the package
    return run_command("python -m build", "Building package")


def publish_test():
    """Publish to Test PyPI."""
    print("🚀 Publishing to Test PyPI")
    return run_command("twine upload --repository testpypi dist/*", "Uploading to Test PyPI")


def publish():
    """Publish to PyPI."""
    print("🚀 Publishing to PyPI")
    response = input("Are you sure you want to publish to PyPI? (y/N): ")
    if response.lower() != 'y':
        print("❌ Publication cancelled")
        return 1

    return run_command("twine upload dist/*", "Uploading to PyPI")


def run_example():
    """Run the basic usage example."""
    return run_command("python examples/basic_usage.py", "Running basic usage example")


def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(description="DataEng Toolbox development helper")
    parser.add_argument("command", choices=[
        "install-dev", "test", "lint", "format", "build",
        "publish-test", "publish", "example", "all"
    ], help="Command to run")

    args = parser.parse_args()

    exit_code = 0

    if args.command == "install-dev":
        exit_code = install_dev()
    elif args.command == "test":
        exit_code = test()
    elif args.command == "lint":
        exit_code = lint()
    elif args.command == "format":
        exit_code = format_code()
    elif args.command == "build":
        exit_code = build()
    elif args.command == "publish-test":
        exit_code = publish_test()
    elif args.command == "publish":
        exit_code = publish()
    elif args.command == "example":
        exit_code = run_example()
    elif args.command == "all":
        # Run the full development pipeline
        commands = [
            ("install-dev", install_dev),
            ("format", format_code),
            ("lint", lint),
            ("test", test),
            ("example", run_example),
            ("build", build),
        ]

        for name, func in commands:
            print(f"\n{'='*50}")
            print(f"Running: {name}")
            print('='*50)
            exit_code = func()
            if exit_code != 0:
                print(f"❌ Pipeline failed at step: {name}")
                break
        else:
            print(f"\n{'='*50}")
            print("✅ All development tasks completed successfully!")
            print('='*50)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
