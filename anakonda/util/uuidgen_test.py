import pytest
from uuid import UUID
from .uuidgen import uuidgen
def test_uuidgen():
    result = uuidgen()
    assert type(result) is str
    assert len(result) == 32
    assert result.isalnum() is True 
    try:
        UUID(result)
    except:
        assert False