from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class MovieReleaseDate(BaseModel):
    title: str = Field(..., description="Titulo do Filme")
    release_date: Optional[str] = Field(..., description="Data Estreia no Brasil, no formato DD/MM/YYYY, preenche como nulo se não tiver certeza")
    comment: str = Field(
        ..., description="Comentário sobre data de estreia - quão confiante está e data escrita em texto livre"
    )
    
    @field_validator('release_date')
    def validate_date_string(cls, value):
        format = "%d/%m/%Y"  # DD/MM/YYYY
        
        if value:
            try:
                return datetime.strptime(value, format)
            except ValueError:
                raise ValueError("Invalid date format, it should be d/m/Y or DD/MM/YYYY")
