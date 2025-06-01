from pydantic import BaseModel


class CreateResponseDTO(BaseModel):
    id: int
