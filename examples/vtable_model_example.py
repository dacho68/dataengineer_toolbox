"""
Example demonstrating serialization and deserialization of VTableModel objects.

This example shows how to:
1. Create VTableModel instances
2. Serialize them to JSON
3. Deserialize them back from JSON
4. Work with lists of VTableModel objects
"""

import json
from typing import List

# Add parent directory to path to import dataeng_toolbox
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dataeng_toolbox.model import VTableModel


def create_vtable_models() -> List[VTableModel]:
    """
    Create a list of VTableModel instances.
    
    Returns:
        List[VTableModel]: A list of virtual table models.
    """
    vtables = [
        VTableModel(namespace="sales", table_name="orders"),
        VTableModel(namespace="sales", table_name="customers"),
        VTableModel(namespace="inventory", table_name="products"),
        VTableModel(namespace="inventory", table_name="warehouses"),
    ]
    return vtables


def serialize_vtables(vtables: List[VTableModel]) -> str:
    """
    Serialize a list of VTableModel objects to JSON string.
    
    Args:
        vtables (List[VTableModel]): List of VTableModel instances to serialize.
        
    Returns:
        str: JSON string representation of the vtables.
    """
    # Convert Pydantic models to dictionaries
    vtables_dict = [vtable.model_dump() for vtable in vtables]
    return json.dumps(vtables_dict, indent=2)


def deserialize_vtables(json_str: str) -> List[VTableModel]:
    """
    Deserialize a JSON string to a list of VTableModel objects.
    
    Args:
        json_str (str): JSON string representation of vtables.
        
    Returns:
        List[VTableModel]: List of deserialized VTableModel instances.
    """
    data = json.loads(json_str)
    vtables = [VTableModel(**item) for item in data]
    return vtables


def main():
    """Main example function."""
    print("=" * 60)
    print("VTableModel Serialization and Deserialization Example")
    print("=" * 60)
    
    # Step 1: Create VTableModel instances
    print("\n1. Creating VTableModel instances...")
    vtables = create_vtable_models()
    
    for vtable in vtables:
        print(f"   - {vtable.namespace}.{vtable.table_name}")
    
    # Step 2: Serialize to JSON
    print("\n2. Serializing to JSON...")
    json_str = serialize_vtables(vtables)
    print("JSON Output:")
    print(json_str)
    
    # Step 3: Deserialize from JSON
    print("\n3. Deserializing from JSON...")
    deserialized_vtables = deserialize_vtables(json_str)
    
    print("Deserialized VTableModel objects:")
    for vtable in deserialized_vtables:
        print(f"   - namespace: {vtable.namespace}, table_name: {vtable.table_name}")
    
    # Step 4: Verify serialization/deserialization integrity
    print("\n4. Verifying data integrity...")
    all_match = all(
        original.namespace == deserialized.namespace and
        original.table_name == deserialized.table_name
        for original, deserialized in zip(vtables, deserialized_vtables)
    )
    
    if all_match:
        print("   ✅ All objects match after serialization/deserialization!")
    else:
        print("   ❌ Data mismatch detected!")
    
    # Step 5: Modify a model and show validation
    print("\n5. Modifying a VTableModel instance...")
    modified_vtable = deserialized_vtables[0]
    print(f"   Before: {modified_vtable.namespace}.{modified_vtable.table_name}")
    
    modified_vtable.table_name = "orders_updated"
    print(f"   After:  {modified_vtable.namespace}.{modified_vtable.table_name}")
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
