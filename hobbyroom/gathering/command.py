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


class UpdatePost(BaseModel):
    title: str | None = None
    content: str | None = None
    post_id: UUID | None = None
    gathering_id: UUID | None = None
    persona_id: UUID | None = None

    @property
    def has_entity_ids(self) -> bool:
        return (
            self.post_id is not None
            and self.gathering_id is not None
            and self.persona_id is not None
        )

    def add_entity_ids(self, post_id: UUID, persona: auth.Persona) -> None:
        self.post_id = post_id
        self.gathering_id = persona.gathering_id
        self.persona_id = persona.id
