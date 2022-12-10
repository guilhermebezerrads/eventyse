import pytest
from Roadmap import Roadmap, roadmap_factory


def test_roadmap_factory():
    author_username = "marco"
    title = "roadmap"
    description = "desc"
    coordinates = [[0, 0]]
    tags = ["tag1", "tag2"]

    roadmap = roadmap_factory(author_username, title, description, coordinates, tags)

    assert roadmap.likes == 0
    assert roadmap.dislikes == 0
    assert roadmap.author_username == "marco"
    assert roadmap.title == "roadmap"
    assert roadmap.description == "desc"
    assert roadmap.coordinates == [[0, 0]]
    assert roadmap.tags == ["tag1", "tag2"]