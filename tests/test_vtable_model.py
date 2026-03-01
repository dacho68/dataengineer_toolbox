"""
Unit tests for VTableModel in dataeng_toolbox.model.
"""

import json
import pytest
from pydantic import ValidationError

from dataeng_toolbox.model import VTableModel, TableType


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def basic_vtable() -> VTableModel:
    return VTableModel(catalog="main", namespace="sales", table_name="orders")


@pytest.fixture
def another_vtable() -> VTableModel:
    return VTableModel(catalog="main", namespace="inventory", table_name="products")


# ---------------------------------------------------------------------------
# Instantiation
# ---------------------------------------------------------------------------

class TestVTableModelInstantiation:
    """Tests for valid and invalid construction."""

    def test_create_with_all_fields(self):
        vtable = VTableModel(catalog="main", namespace="sales", table_name="orders")
        assert vtable.catalog == "main"
        assert vtable.namespace == "sales"
        assert vtable.table_name == "orders"

    def test_create_via_keyword_args(self, basic_vtable):
        assert isinstance(basic_vtable, VTableModel)

    def test_missing_catalog_raises(self):
        with pytest.raises(ValidationError):
            VTableModel(namespace="sales", table_name="orders")  # type: ignore[call-arg]

    def test_missing_namespace_raises(self):
        with pytest.raises(ValidationError):
            VTableModel(catalog="main", table_name="orders")  # type: ignore[call-arg]

    def test_missing_table_name_raises(self):
        with pytest.raises(ValidationError):
            VTableModel(catalog="main", namespace="sales")  # type: ignore[call-arg]

    def test_all_fields_missing_raises(self):
        with pytest.raises(ValidationError):
            VTableModel()  # type: ignore[call-arg]

    def test_wrong_type_catalog_raises(self):
        with pytest.raises(ValidationError):
            VTableModel(catalog=123, namespace="sales", table_name="orders")  # type: ignore[arg-type]

    def test_wrong_type_namespace_raises(self):
        with pytest.raises(ValidationError):
            VTableModel(catalog="main", namespace=None, table_name="orders")  # type: ignore[arg-type]

    def test_wrong_type_table_name_raises(self):
        with pytest.raises(ValidationError):
            VTableModel(catalog="main", namespace="sales", table_name=["orders"])  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Field values
# ---------------------------------------------------------------------------

class TestVTableModelFields:
    """Tests verifying field storage and access."""

    def test_catalog_stored_correctly(self, basic_vtable):
        assert basic_vtable.catalog == "main"

    def test_namespace_stored_correctly(self, basic_vtable):
        assert basic_vtable.namespace == "sales"

    def test_table_name_stored_correctly(self, basic_vtable):
        assert basic_vtable.table_name == "orders"

    def test_empty_string_fields_allowed(self):
        vtable = VTableModel(catalog="", namespace="", table_name="")
        assert vtable.catalog == ""
        assert vtable.namespace == ""
        assert vtable.table_name == ""

    def test_fields_with_special_characters(self):
        vtable = VTableModel(
            catalog="my-catalog_01",
            namespace="my.namespace",
            table_name="table/name",
        )
        assert vtable.catalog == "my-catalog_01"
        assert vtable.namespace == "my.namespace"
        assert vtable.table_name == "table/name"


# ---------------------------------------------------------------------------
# Mutability (frozen=False, validate_assignment=True)
# ---------------------------------------------------------------------------

class TestVTableModelMutability:
    """Tests for mutable field assignment with validation."""

    def test_catalog_can_be_updated(self, basic_vtable):
        basic_vtable.catalog = "dev"
        assert basic_vtable.catalog == "dev"

    def test_namespace_can_be_updated(self, basic_vtable):
        basic_vtable.namespace = "finance"
        assert basic_vtable.namespace == "finance"

    def test_table_name_can_be_updated(self, basic_vtable):
        basic_vtable.table_name = "invoices"
        assert basic_vtable.table_name == "invoices"

    def test_invalid_assignment_raises_validation_error(self, basic_vtable):
        with pytest.raises(ValidationError):
            basic_vtable.catalog = None  # type: ignore[assignment]


# ---------------------------------------------------------------------------
# Serialization: model_dump
# ---------------------------------------------------------------------------

class TestVTableModelDump:
    """Tests for model_dump serialization."""

    def test_model_dump_returns_dict(self, basic_vtable):
        result = basic_vtable.model_dump()
        assert isinstance(result, dict)

    def test_model_dump_contains_all_keys(self, basic_vtable):
        result = basic_vtable.model_dump()
        assert set(result.keys()) == {"catalog", "namespace", "file_name", "file_type", "table_name", "table_type"}

    def test_model_dump_values_match(self, basic_vtable):
        result = basic_vtable.model_dump()
        assert result["catalog"] == "main"
        assert result["namespace"] == "sales"
        assert result["table_name"] == "orders"
        # default table_type should be UNDEFINED
        assert basic_vtable.table_type == TableType.UNDEFINED


# ---------------------------------------------------------------------------
# Serialization: model_dump_json / JSON roundtrip
# ---------------------------------------------------------------------------

class TestVTableModelJsonSerialization:
    """Tests for JSON serialization and deserialization."""

    def test_model_dump_json_returns_string(self, basic_vtable):
        result = basic_vtable.model_dump_json()
        assert isinstance(result, str)

    def test_model_dump_json_is_valid_json(self, basic_vtable):
        result = basic_vtable.model_dump_json()
        parsed = json.loads(result)
        assert isinstance(parsed, dict)

    def test_json_roundtrip_preserves_fields(self, basic_vtable):
        json_str = basic_vtable.model_dump_json()
        restored = VTableModel.model_validate_json(json_str)
        assert restored.catalog == basic_vtable.catalog
        assert restored.namespace == basic_vtable.namespace
        assert restored.table_name == basic_vtable.table_name
        assert restored.table_type == basic_vtable.table_type

    def test_dict_roundtrip_via_model_validate(self, basic_vtable):
        data = basic_vtable.model_dump()
        restored = VTableModel.model_validate(data)
        assert restored.catalog == basic_vtable.catalog
        assert restored.namespace == basic_vtable.namespace
        assert restored.table_name == basic_vtable.table_name
        assert restored.table_type == basic_vtable.table_type

    def test_list_json_roundtrip(self, basic_vtable, another_vtable):
        vtables = [basic_vtable, another_vtable]
        json_str = json.dumps([v.model_dump(mode="json") for v in vtables])
        restored = [VTableModel(**item) for item in json.loads(json_str)]

        assert len(restored) == 2
        for original, result in zip(vtables, restored):
            assert original.catalog == result.catalog
            assert original.namespace == result.namespace
            assert original.table_name == result.table_name
            assert original.table_type == result.table_type


# ---------------------------------------------------------------------------
# Deserialization: model_validate
# ---------------------------------------------------------------------------

class TestVTableModelValidate:
    """Tests for construction via model_validate."""

    def test_model_validate_from_dict(self):
        data = {"catalog": "main", "namespace": "hr", "table_name": "employees"}
        vtable = VTableModel.model_validate(data)
        assert vtable.catalog == "main"
        assert vtable.namespace == "hr"
        assert vtable.table_name == "employees"
        assert vtable.table_type == TableType.UNDEFINED

    def test_model_validate_fails_on_missing_field(self):
        with pytest.raises(ValidationError):
            VTableModel.model_validate({"namespace": "hr", "table_name": "employees"})

    def test_model_validate_json_from_string(self):
        json_str = '{"catalog": "main", "namespace": "hr", "table_name": "employees"}'
        vtable = VTableModel.model_validate_json(json_str)
        assert vtable.catalog == "main"
        assert vtable.table_type == TableType.UNDEFINED


# ---------------------------------------------------------------------------
# Equality and identity
# ---------------------------------------------------------------------------

class TestVTableModelEquality:
    """Tests for equality and identity semantics."""

    def test_equal_instances_with_same_values(self):
        a = VTableModel(catalog="main", namespace="sales", table_name="orders")
        b = VTableModel(catalog="main", namespace="sales", table_name="orders")
        assert a == b

    def test_unequal_instances_with_different_table_name(self):
        a = VTableModel(catalog="main", namespace="sales", table_name="orders")
        b = VTableModel(catalog="main", namespace="sales", table_name="customers")
        assert a != b

    def test_unequal_instances_with_different_namespace(self):
        a = VTableModel(catalog="main", namespace="sales", table_name="orders")
        b = VTableModel(catalog="main", namespace="inventory", table_name="orders")
        assert a != b

    def test_unequal_instances_with_different_catalog(self):
        a = VTableModel(catalog="dev", namespace="sales", table_name="orders")
        b = VTableModel(catalog="prod", namespace="sales", table_name="orders")
        assert a != b

    def test_not_equal_to_plain_dict(self, basic_vtable):
        assert basic_vtable != {"catalog": "main", "namespace": "sales", "table_name": "orders"}


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

class TestVTableModelSchema:
    """Tests for JSON schema generation."""

    def test_model_json_schema_returns_dict(self):
        schema = VTableModel.model_json_schema()
        assert isinstance(schema, dict)

    def test_schema_has_title(self):
        schema = VTableModel.model_json_schema()
        assert "title" in schema

    def test_schema_has_all_properties(self):
        schema = VTableModel.model_json_schema()
        props = schema.get("properties", {})
        assert "catalog" in props
        assert "namespace" in props
        assert "table_name" in props
        assert "table_type" in props

    def test_schema_required_fields(self):
        schema = VTableModel.model_json_schema()
        required = schema.get("required", [])
        assert "catalog" in required
        assert "namespace" in required
        assert "table_name" in required


if __name__ == "__main__":
    TestVTableModelJsonSerialization().test_list_json_roundtrip(basic_vtable=VTableModel(catalog="main", namespace="sales", table_name="orders"), another_vtable=VTableModel(catalog="main", namespace="inventory", table_name="products"))
