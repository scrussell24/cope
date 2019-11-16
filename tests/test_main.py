from ape import Ape


def test_ape_constructor():
    ape = Ape()
    assert isinstance(ape, Ape)
