from uuid import UUID

import bcrypt
from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    email: EmailStr
    password: str

    @property
    def hashed_password(self) -> str:
        return bcrypt.hashpw(
            password=self.password.encode(), salt=bcrypt.gensalt()
        ).decode()


class CreatePersona(BaseModel):
    name: str
    user_id: UUID | None = None
