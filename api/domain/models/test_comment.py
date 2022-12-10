import pytest
from Comment import Comment, comment_factory


def test_comment_factory():
    author_username = "marco"
    text = "comment"
    roadmap_id = "1"

    comment = comment_factory(author_username, roadmap_id, text)

    assert comment.author_username == "marco"
    assert comment.text == "comment"
    assert comment.roadmap_id == "1"