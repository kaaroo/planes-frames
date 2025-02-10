import pytest

from app.models import validate_icao


def test_validate_icao_success():
    # expect no exception
    validate_icao("ABCD")


@pytest.mark.parametrize(
    "icao",
    ["ABC", "ABC1", "aBCD", "", "ABC!"]
)
def test_validate_icao_failure(icao):
    # expect
    with pytest.raises(ValueError):
        validate_icao(icao)
