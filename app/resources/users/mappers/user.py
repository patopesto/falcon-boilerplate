from datetime import datetime
from typing import List, Union
from uuid import UUID

from app.data.mapper import Mapper
from ..models import UserModel

USERS = [
    {
        "id": UUID("a6b2cb86-c689-40bb-9d5a-44b9bc096d89"),
        "created_at": datetime(2020, 5, 9, 16, 20, 40, 560920),
        "first_name": "Alain",
        "last_name": "Belanger",
        "email": "alain.belanger@example.com",
    },
    {
        "id": UUID("8307e8d2-e225-4ee3-8606-f7f2d01fdaf1"),
        "created_at": datetime(2020, 5, 9, 16, 21, 1, 326478),
        "first_name": "Sylvie",
        "last_name": "Boucher",
        "email": "sylvie.boucher@example.com",
    },
]


class UserMapper(Mapper):
    def __init__(self):
        global USERS
        self.users = USERS

    def create(self, user: UserModel) -> UserModel:
        exists = self._find_by_email_or_id(user.email, user.id)
        if exists:
            raise ValueError

        self.users.append(user.to_dict())

        return self.get(user.id)

    def get(self, user_id: Union[str, UUID]) -> Union[UserModel, None]:
        user_id = self._hex_str_to_uuid(user_id)

        for user in self.users:
            if user["id"] == user_id:
                return UserModel(**user)

    def get_all(self) -> Union[List[UserModel], None]:
        if len(self.users) < 1:
            return []

        users = []
        for user in self.users:
            o = UserModel(**user)
            if getattr(o, "deleted_at") and o.deleted_at is not None:
                continue
            else:
                users.append(o)

        return users

    def save(self, user: UserModel) -> UserModel:
        pos = self._get_index(user.id)
        if pos is not None:
            self.users[pos] = user.to_dict()

        return user

    def find_by_email(self, email: str) -> Union[UserModel, None]:
        for user in self.users:
            if user["email"] == email:
                return UserModel(**user)

    def _get_index(self, user_id: Union[str, UUID]):
        user_id = self._hex_str_to_uuid(user_id)

        for idx, user in enumerate(self.users):
            if user["id"] == user_id:
                return idx

    def _find_by_email_or_id(
        self, email: str, user_id: Union[str, UUID]
    ) -> Union[UserModel, None]:
        user_id = self._hex_str_to_uuid(user_id)

        for user in self.users:
            if user["email"] == email or user["id"] == user_id:
                return UserModel(**user)

    @staticmethod
    def _hex_str_to_uuid(user_id: Union[str, UUID]) -> UUID:
        if isinstance(user_id, str):
            return UUID(user_id)
        return user_id
