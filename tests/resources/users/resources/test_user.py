import falcon
import pytest
from mock import patch

from app.resources.users.mappers import UserMapper
from .. import user1
from . import skip_missing_dep


@skip_missing_dep
@pytest.mark.parametrize("user", (user1(),))
def test_get_user(client, user):
    with patch.object(UserMapper, "get", return_value=user):
        result = client.simulate_get("/users/1")

        assert result.status == falcon.HTTP_OK
        assert result.json["id"] == user.id
        assert result.json["first_name"] == user.first_name
        assert result.json["last_name"] == user.last_name
        assert result.json["email"] == user.email


@skip_missing_dep
@pytest.mark.parametrize("user", (user1(),))
def test_delete_user(client, user):
    with patch.object(UserMapper, "get", return_value=user):
        result = client.simulate_delete("/users/1")

        assert result.status == falcon.HTTP_NO_CONTENT

        result = client.simulate_delete("/users/1")

        assert result.status == falcon.HTTP_GONE
        assert user.deleted_at != ""


@skip_missing_dep
@pytest.mark.parametrize("user", (user1(),))
def test_edit_user(client, user):
    doc = {"last_name": "changed"}
    with patch.object(UserMapper, "get", return_value=user):
        result = client.simulate_put("/users/1", json=doc)

        assert result.status == falcon.HTTP_OK
        assert result.json["last_name"] == doc["last_name"]
        assert result.json["updated_at"] != ""