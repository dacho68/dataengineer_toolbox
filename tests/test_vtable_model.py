"""
Unit tests for VTableModel in dataeng_toolbox.model.
"""

import json
import pytest
from pydantic import ValidationError

from dataeng_toolbox.model import VTableModel, TableType, FileType


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def basic_vtable() -> VTableModel:
    return VTableModel(catalog="main", namespace="sales", name="orders")


@pytest.fixture
def another_vtable() -> VTableModel:
    return VTableModel(catalog="main", namespace="inventory", name="products")


# ---------------------------------------------------------------------------
# Instantiation
# ---------------------------------------------------------------------------

class TestVTableModelInstantiation:
    """Tests for valid and invalid construction."""

    def test_create_with_all_fields(self):
        vtable = VTableModel(catalog="main", namespace="sales", name="orders")
        assert vtable.catalog == "main"
        assert vtable.namespace == "sales"
        assert vtable.name == "orders"

    def test_create_via_keyword_args(self, basic_vtable):
        assert isinstance(basic_vtable, VTableModel)

    def test_missing_catalog_allowed(self):
        vtable = VTableModel(namespace="sales", name="orders")
        assert vtable.catalog is None

    def test_missing_namespace_allowed(self):
        vtable = VTableModel(catalog="main", name="orders")
        assert vtable.namespace is None

    def test_missing_name_raises(self):
        with pytest.raises(ValidationError):
            VTableModel(catalog="main", namespace="sales")  # type: ignore[call-arg]

    def test_all_fields_missing_raises(self):
        with pytest.raises(ValidationError):
            VTableModel()  # type: ignore[call-arg]

    def test_wrong_type_catalog_raises(self):
        with pytest.raises(ValidationError):
            VTableModel(catalog=123, namespace="sales", name="orders")  # type: ignore[arg-type]

    def test_wrong_type_namespace_raises(self):
        with pytest.raises(ValidationError):
            VTableModel(catalog="main", namespace=123, name="orders")  # type: ignore[arg-type]

    def test_wrong_type_name_raises(self):
        with pytest.raises(ValidationError):
            VTableModel(catalog="main", namespace="sales", name=["orders"])  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Field values
# ---------------------------------------------------------------------------

class TestVTableModelFields:
    """Tests verifying field storage and access."""

    def test_catalog_stored_correctly(self, basic_vtable):
        assert basic_vtable.catalog == "main"

    def test_namespace_stored_correctly(self, basic_vtable):
        assert basic_vtable.namespace == "sales"

    def test_name_stored_correctly(self, basic_vtable):
        assert basic_vtable.name == "orders"

    def test_empty_string_fields_allowed(self):
        vtable = VTableModel(catalog="", namespace="", name="")
        assert vtable.catalog == ""
        assert vtable.namespace == ""
        assert vtable.name == ""

    def test_fields_with_special_characters(self):
        vtable = VTableModel(
            catalog="my-catalog_01",
            namespace="my.namespace",
            name="table/name",
        )
        assert vtable.catalog == "my-catalog_01"
        assert vtable.namespace == "my.namespace"
        assert vtable.name == "table/name"


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

    def test_name_can_be_updated(self, basic_vtable):
        basic_vtable.name = "invoices"
        assert basic_vtable.name == "invoices"

    def test_invalid_assignment_raises_validation_error(self, basic_vtable):
        with pytest.raises(ValidationError):
            basic_vtable.catalog = 123  # type: ignore[assignment]


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
        assert set(result.keys()) == {"catalog", "namespace", "name", "file_path", "file_type", "table_type"}

    def test_model_dump_values_match(self, basic_vtable):
        result = basic_vtable.model_dump()
        assert result["catalog"] == "main"
        assert result["namespace"] == "sales"
        assert result["name"] == "orders"
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
        assert restored.name == basic_vtable.name
        assert restored.table_type == basic_vtable.table_type

    def test_dict_roundtrip_via_model_validate(self, basic_vtable):
        data = basic_vtable.model_dump()
        restored = VTableModel.model_validate(data)
        assert restored.catalog == basic_vtable.catalog
        assert restored.namespace == basic_vtable.namespace
        assert restored.name == basic_vtable.name
        assert restored.table_type == basic_vtable.table_type

    def test_list_json_roundtrip(self, basic_vtable, another_vtable):
        vtables = [basic_vtable, another_vtable]
        json_str = json.dumps([v.model_dump(mode="json") for v in vtables])
        restored = [VTableModel(**item) for item in json.loads(json_str)]

        assert len(restored) == 2
        for original, result in zip(vtables, restored):
            assert original.catalog == result.catalog
            assert original.namespace == result.namespace
            assert original.name == result.name
            assert original.table_type == result.table_type


# ---------------------------------------------------------------------------
# Deserialization: model_validate
# ---------------------------------------------------------------------------

class TestVTableModelValidate:
    """Tests for construction via model_validate."""

    def test_model_validate_from_dict(self):
        data = {"catalog": "main", "namespace": "hr", "name": "employees"}
        vtable = VTableModel.model_validate(data)
        assert vtable.catalog == "main"
        assert vtable.namespace == "hr"
        assert vtable.name == "employees"
        assert vtable.table_type == TableType.UNDEFINED

    def test_model_validate_succeeds_with_optional_fields(self):
        vtable = VTableModel.model_validate({"name": "employees"})
        assert vtable.name == "employees"
        assert vtable.catalog is None
        assert vtable.namespace is None

    def test_model_validate_json_from_string(self):
        json_str = '{"catalog": "main", "namespace": "hr", "name": "employees"}'
        vtable = VTableModel.model_validate_json(json_str)
        assert vtable.catalog == "main"
        assert vtable.table_type == TableType.UNDEFINED


# ---------------------------------------------------------------------------
# Equality and identity
# ---------------------------------------------------------------------------

class TestVTableModelEquality:
    """Tests for equality and identity semantics."""

    def test_equal_instances_with_same_values(self):
        a = VTableModel(catalog="main", namespace="sales", name="orders")
        b = VTableModel(catalog="main", namespace="sales", name="orders")
        assert a == b

    def test_unequal_instances_with_different_table_name(self):
        a = VTableModel(catalog="main", namespace="sales", name="orders")
        b = VTableModel(catalog="main", namespace="sales", name="customers")
        assert a != b

    def test_unequal_instances_with_different_namespace(self):
        a = VTableModel(catalog="main", namespace="sales", name="orders")
        b = VTableModel(catalog="main", namespace="inventory", name="orders")
        assert a != b

    def test_unequal_instances_with_different_catalog(self):
        a = VTableModel(catalog="dev", namespace="sales", name="orders")
        b = VTableModel(catalog="prod", namespace="sales", name="orders")
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
        assert "name" in props
        assert "file_path" in props
        assert "file_type" in props
        assert "table_type" in props

    def test_schema_required_fields(self):
        schema = VTableModel.model_json_schema()
        required = schema.get("required", [])
        assert "name" in required
        # catalog, namespace and file_path are optional
        assert "catalog" not in required
        assert "namespace" not in required
        assert "file_path" not in required


# ---------------------------------------------------------------------------
# Business rules: EXTERNAL table validation
# ---------------------------------------------------------------------------

class TestVTableModelExternalValidation:
    """Tests for the EXTERNAL table -> DELTA file type constraint."""

    def test_external_with_delta_is_valid(self):
        vtable = VTableModel(
            catalog="main", namespace="sales", name="orders",
            table_type=TableType.EXTERNAL, file_type=FileType.DELTA
        )
        assert vtable.table_type == TableType.EXTERNAL
        assert vtable.file_type == FileType.DELTA

    def test_external_with_non_delta_raises(self):
        for ft in [FileType.CSV, FileType.PARQUET, FileType.JSON]:
            with pytest.raises(ValidationError):
                VTableModel(
                    catalog="main", namespace="sales", name="orders",
                    table_type=TableType.EXTERNAL, file_type=ft
                )

    def test_external_with_undefined_file_type_raises(self):
        with pytest.raises(ValidationError):
            VTableModel(
                catalog="main", namespace="sales", name="orders",
                table_type=TableType.EXTERNAL
                # file_type defaults to UNDEFINED
            )

    def test_managed_with_any_file_type_is_valid(self):
        for ft in [FileType.UNDEFINED, FileType.CSV, FileType.PARQUET, FileType.DELTA, FileType.JSON]:
            vtable = VTableModel(
                catalog="main", namespace="sales", name="orders",
                table_type=TableType.MANAGED, file_type=ft
            )
            assert vtable.table_type == TableType.MANAGED

    def test_assignment_external_with_non_delta_raises(self):
        vtable = VTableModel(
            catalog="main", namespace="sales", name="orders",
            table_type=TableType.EXTERNAL, file_type=FileType.DELTA
        )
        with pytest.raises(ValidationError):
            vtable.file_type = FileType.CSV


if __name__ == "__main__":
    TestVTableModelJsonSerialization().test_list_json_roundtrip(basic_vtable=VTableModel(catalog="main", namespace="sales", name="orders"), another_vtable=VTableModel(catalog="main", namespace="inventory", name="products"))
