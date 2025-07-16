from pydantic import BaseModel, EmailStr
import bcrypt


class CreateUser(BaseModel):
    email: EmailStr
    password: str

    @property
    def hashed_password(self) -> str:
        return bcrypt.hashpw(
            password=self.password.encode(), salt=bcrypt.gensalt()
        ).decode()
