from unittest.mock import patch, MagicMock, AsyncMock
import pytest

from app.service import PlaneService
from tests.fixtures import some_plane_data_frame


@pytest.mark.asyncio
@patch("app.service.plane_repository", new_callable=AsyncMock)
async def test_get_latest_planes_positions(plane_repository_mock):
    # given
    frames_generator = MagicMock()
    service = PlaneService(frames_generator)

    # and
    frame = some_plane_data_frame()

    frames_generator.planes_ids = {frame.icao}
    plane_repository_mock.get_last_planes_positions.return_value = [frame]

    # when
    result = await service.get_latest_planes_positions()

    # then
    assert result == [frame]

    # and
    plane_repository_mock.get_last_planes_positions.assert_called_with([frame.icao])


@pytest.mark.asyncio
@patch("app.service.plane_repository", new_callable=AsyncMock)
async def test_validate_icaos_of_latest_planes_positions(plane_repository_mock):
    # given
    frames_generator = MagicMock()
    service = PlaneService(frames_generator)

    # and
    frame = some_plane_data_frame()

    frames_generator.planes_ids = set()
    plane_repository_mock.get_last_planes_positions.return_value = [frame]

    # then
    with pytest.raises(ValueError):
        await service.get_latest_planes_positions()


@pytest.mark.asyncio
@patch("app.service.plane_repository", new_callable=AsyncMock)
async def test_get_plane_history(plane_repository_mock):
    # given
    frames_generator = MagicMock()
    service = PlaneService(frames_generator)

    # and
    frame = some_plane_data_frame()
    plane_repository_mock.get_frames_for_plane.return_value = [frame]

    # when
    result = await service.get_plane_history(frame.icao)

    # then
    assert result == [frame]
