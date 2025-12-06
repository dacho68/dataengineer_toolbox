"""
Basic usage example for dataeng_toolbox.

This example demonstrates how to use the Core class from the dataeng_toolbox package.
"""

import sys
import os

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dataeng_toolbox import Core


def main():
    """Main function demonstrating basic usage."""
    print("DataEng Toolbox - Basic Usage Example")
    print("=" * 40)

    # Create an instance of the Core class
    toolbox = Core()

    # Use the hello_world method
    print("\n1. Hello World Example:")
    message = toolbox.hello_world()
    print(f"   {message}")

    # Get toolbox information
    print("\n2. Toolbox Information:")
    info = toolbox.get_info()
    for key, value in info.items():
        print(f"   {key.capitalize()}: {value}")

    print("\n" + "=" * 40)
    print("Example completed successfully!")


if __name__ == "__main__":
    main()
