from uuid import UUID

from pydantic import BaseModel

from hobbyroom import exceptions
from hobbyroom import user as user_domain


class CreateGathering(BaseModel):
    name: str
    description: str
    persona_id: UUID

    def validate_persona_id(self, user: user_domain.User) -> None:
        persona = next(
            (persona for persona in user.personas if persona.id == self.persona_id),
            None,
        )
        if persona is None:
            raise exceptions.NotFoundError(
                "유효한 페르소나 정보가 사용자에게 없습니다."
            )
