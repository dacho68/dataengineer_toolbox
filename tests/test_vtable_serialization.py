"""
Unit tests for serialization and deserialization of VTableModel lists from/to JSON.
"""

import json
import pytest
from pydantic import TypeAdapter, ValidationError

from dataeng_toolbox.model import VTableModel, TableType


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_LIST_ADAPTER = TypeAdapter(list[VTableModel])


def _make_vtable(
    catalog: str = "main",
    namespace: str = "sales",
    table_name: str = "orders",
    table_type: TableType = TableType.UNDEFINED,
) -> VTableModel:
    return VTableModel(
        catalog=catalog,
        namespace=namespace,
        table_name=table_name,
        table_type=table_type,
    )


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def vtable_list() -> list[VTableModel]:
    return [
        _make_vtable("main", "sales", "orders", TableType.MANAGED),
        _make_vtable("main", "inventory", "products", TableType.EXTERNAL),
        _make_vtable("dev", "hr", "employees", TableType.UNDEFINED),
    ]


@pytest.fixture
def vtable_list_json(vtable_list) -> str:
    """JSON string produced by serialising ``vtable_list``."""
    return json.dumps([v.model_dump(mode="json") for v in vtable_list])


# ---------------------------------------------------------------------------
# Serialization  (list → JSON)
# ---------------------------------------------------------------------------


class TestVTableListSerialization:
    """Serialize a list of VTableModel instances to JSON."""

    def test_dumps_returns_string(self, vtable_list):
        result = json.dumps([v.model_dump(mode="json") for v in vtable_list])
        assert isinstance(result, str)

    def test_dumps_is_valid_json(self, vtable_list):
        result = json.dumps([v.model_dump(mode="json") for v in vtable_list])
        parsed = json.loads(result)
        assert isinstance(parsed, list)

    def test_dumps_length_preserved(self, vtable_list):
        result = json.loads(json.dumps([v.model_dump(mode="json") for v in vtable_list]))
        assert len(result) == len(vtable_list)

    def test_dumps_table_type_serialized_as_int(self, vtable_list):
        """TableType enum values must be stored as integers, not strings."""
        raw = json.loads(json.dumps([v.model_dump(mode="json") for v in vtable_list]))
        for item in raw:
            assert isinstance(item["table_type"], int)

    def test_model_dump_json_method(self, vtable_list):
        """Each model's own model_dump_json() produces valid JSON with table_type as int."""
        for vtable in vtable_list:
            raw = json.loads(vtable.model_dump_json())
            assert isinstance(raw["table_type"], int)

    def test_type_adapter_dump_json(self, vtable_list):
        """TypeAdapter can dump the whole list in one call."""
        json_str = _LIST_ADAPTER.dump_json(vtable_list)
        assert isinstance(json_str, bytes)
        parsed = json.loads(json_str)
        assert len(parsed) == len(vtable_list)


# ---------------------------------------------------------------------------
# Deserialization  (JSON → list)
# ---------------------------------------------------------------------------


class TestVTableListDeserialization:
    """Deserialize a JSON array back into a list of VTableModel instances."""

    def test_list_roundtrip_length(self, vtable_list, vtable_list_json):
        restored = [VTableModel(**item) for item in json.loads(vtable_list_json)]
        assert len(restored) == len(vtable_list)

    def test_list_roundtrip_types(self, vtable_list_json):
        restored = [VTableModel(**item) for item in json.loads(vtable_list_json)]
        assert all(isinstance(v, VTableModel) for v in restored)

    def test_list_roundtrip_field_values(self, vtable_list, vtable_list_json):
        restored = [VTableModel(**item) for item in json.loads(vtable_list_json)]
        for original, result in zip(vtable_list, restored):
            assert result.catalog == original.catalog
            assert result.namespace == original.namespace
            assert result.table_name == original.table_name
            assert result.table_type == original.table_type

    def test_type_adapter_roundtrip(self, vtable_list):
        """Full roundtrip via TypeAdapter dump/validate."""
        json_bytes = _LIST_ADAPTER.dump_json(vtable_list)
        restored = _LIST_ADAPTER.validate_json(json_bytes)
        assert len(restored) == len(vtable_list)
        for original, result in zip(vtable_list, restored):
            assert result == original

    def test_model_validate_json_from_string(self):
        json_str = (
            '[{"catalog":"main","namespace":"sales","table_name":"orders","table_type":1},'
            ' {"catalog":"dev","namespace":"hr","table_name":"employees","table_type":0}]'
        )
        restored = _LIST_ADAPTER.validate_json(json_str)
        assert len(restored) == 2
        assert restored[0].catalog == "main"
        assert restored[0].table_type == TableType.MANAGED
        assert restored[1].catalog == "dev"
        assert restored[1].table_type == TableType.UNDEFINED

    def test_deserialize_table_type_by_name_raises(self):
        """Pydantic V2 int-based enums only accept integer values, not string names."""
        json_str = (
            '[{"catalog":"main","namespace":"sales","table_name":"orders","table_type":"MANAGED"}]'
        )
        with pytest.raises(ValidationError):
            _LIST_ADAPTER.validate_json(json_str)

    def test_deserialize_missing_table_type_uses_default(self):
        """Omitting table_type should fall back to UNDEFINED."""
        json_str = '[{"catalog":"main","namespace":"sales","table_name":"orders"}]'
        restored = _LIST_ADAPTER.validate_json(json_str)
        assert restored[0].table_type == TableType.UNDEFINED

    def test_deserialize_empty_list(self):
        restored = _LIST_ADAPTER.validate_json("[]")
        assert restored == []

    def test_deserialize_invalid_table_type_raises(self):
        json_str = '[{"catalog":"main","namespace":"sales","table_name":"orders","table_type":99}]'
        with pytest.raises((ValidationError, ValueError)):
            _LIST_ADAPTER.validate_json(json_str)

    def test_deserialize_missing_required_field_raises(self):
        """Missing catalog should raise ValidationError."""
        json_str = '[{"namespace":"sales","table_name":"orders"}]'
        with pytest.raises(ValidationError):
            _LIST_ADAPTER.validate_json(json_str)

    def test_deserialize_wrong_type_for_catalog_raises(self):
        json_str = '[{"catalog":123,"namespace":"sales","table_name":"orders"}]'
        with pytest.raises(ValidationError):
            _LIST_ADAPTER.validate_json(json_str)


# ---------------------------------------------------------------------------
# Edge-cases
# ---------------------------------------------------------------------------


class TestVTableListEdgeCases:
    """Boundary and edge-case scenarios."""

    def test_single_item_list(self):
        vtable = _make_vtable()
        json_str = json.dumps([vtable.model_dump(mode="json")])
        restored = [VTableModel(**item) for item in json.loads(json_str)]
        assert len(restored) == 1
        assert restored[0] == vtable

    def test_large_list_roundtrip(self):
        table_types = [TableType.UNDEFINED, TableType.MANAGED, TableType.EXTERNAL]
        vtables = [
            _make_vtable(f"cat{i}", f"ns{i}", f"tbl{i}", table_types[i % 3])
            for i in range(100)
        ]
        json_str = _LIST_ADAPTER.dump_json(vtables)
        restored = _LIST_ADAPTER.validate_json(json_str)
        assert len(restored) == 100
        for original, result in zip(vtables, restored):
            assert result == original

    def test_all_table_type_values_roundtrip(self):
        vtables = [_make_vtable(table_type=tt) for tt in TableType]
        json_str = _LIST_ADAPTER.dump_json(vtables)
        restored = _LIST_ADAPTER.validate_json(json_str)
        for original, result in zip(vtables, restored):
            assert result.table_type == original.table_type

    def test_duplicate_entries_preserved(self):
        vtable = _make_vtable()
        vtables = [vtable, vtable, vtable]
        json_str = _LIST_ADAPTER.dump_json(vtables)
        restored = _LIST_ADAPTER.validate_json(json_str)
        assert len(restored) == 3
        assert all(v == vtable for v in restored)
