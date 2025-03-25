from pydantic import BaseModel, Field
from typing import List, Literal
from datetime import datetime


class CommandeProduitCreate(BaseModel):
    produit_id: str
    quantite: int = Field(..., ge=1)

class CommandeCreate(BaseModel):
    produits: List[CommandeProduitCreate]

class CommandeProduit(BaseModel):
    produit_id: str
    quantite: int

    class Config:
        orm_mode = True

class Commande(BaseModel):
    id: str
    total: float
    statut: str
    date_commande: datetime
    produits: List[CommandeProduit]

    class Config:
        orm_mode = True

class UpdateStatutCommande(BaseModel):
    statut: Literal["en attente", "en cours", "expédiée", "annulée"]
