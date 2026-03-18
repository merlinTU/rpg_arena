import pytest
from unittest.mock import MagicMock

from rpg_arena.service.camp_service import CampService

@pytest.fixture
def camp_service_setup():
    """
    Fixture to create CampService with a mocked RootService and CampActionService.
    """
    root_service_mock = MagicMock()
    root_service_mock.camp_action_service = MagicMock()

    service = CampService(root_service_mock)

    # Mock printer methods to prevent actual printing
    service.printer.print_at_open_menu = MagicMock()
    service.printer.print_at_open_item_manager = MagicMock()

    return service, root_service_mock

def test_open_camp(camp_service_setup):
    """
    Test that open_camp calls the printer and camp_action_service.
    """
    service, root_mock = camp_service_setup

    service.open_camp()

    # Assert printer method called
    service.printer.print_at_open_menu.assert_called_once()
    # Assert camp_action_service method called
    root_mock.camp_action_service.choose_camp_action.assert_called_once()

def test_open_item_manager(camp_service_setup):
    """
    Test that open_item_manager calls the printer and camp_action_service.
    """
    service, root_mock = camp_service_setup

    service.open_item_manager()

    # Assert printer method called
    service.printer.print_at_open_item_manager.assert_called_once()
    # Assert camp_action_service method called
    root_mock.camp_action_service.choose_item_manager_action.assert_called_once()