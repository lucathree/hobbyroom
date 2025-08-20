from uuid import UUID

from pydantic import BaseModel

from hobbyroom import auth, exceptions


class InitialGatheringCommand(BaseModel):
    persona_id: UUID

    def validate_persona_id(self, user: auth.User) -> None:
        persona = user.find_persona(persona_id=self.persona_id)
        if persona is None:
            raise exceptions.NotFoundError(
                "유효한 페르소나 정보가 사용자에게 없습니다."
            )


class CreateGathering(InitialGatheringCommand):
    name: str
    description: str


class JoinGathering(InitialGatheringCommand):
    gathering_id: UUID


class CreatePost(BaseModel):
    title: str
    content: str
    gathering_id: UUID | None = None
    persona_id: UUID | None = None

    def add_affiliation_info(self, persona: auth.Persona) -> None:
        self.gathering_id = persona.gathering_id
        self.persona_id = persona.id
