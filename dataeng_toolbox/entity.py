from dataeng_toolbox.model import ScdType, Context, VTableModel


class BaseEntity(object):
    """Base class for all entities."""
    def __init__(self, context: Context,  scd_type: ScdType) -> None:
        self._scd_type = scd_type
        self._context = context


class SilverEntity(BaseEntity):
    def __init__(self, context: Context, scd_type: ScdType) -> None:
        super().__init__(context, scd_type)
        self._context = context


    def _get_dependencies(self) -> list[VTableModel]:
        """Get the list of dependency entities for the bronze entity."""
        return []
    
    def _load_dependencies(self) -> None:
        """Load dependencies for the bronze entity."""
        dependencies = self._get_dependencies()
        for dependency in dependencies:
            pass  # Implement loading logic here    
