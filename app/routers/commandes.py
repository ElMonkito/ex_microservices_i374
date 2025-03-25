import traceback

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import List


from app import schemas, models
from app.database import SessionLocal
router = APIRouter(prefix="/commandes", tags=["Commandes"])

# Dependency pour DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Commande)
def creer_commande(commande: schemas.CommandeCreate, db: Session = Depends(get_db)):
    try:
        nouvelle_commande = models.Commande(
            id=str(uuid4()),
            total=0.0,
            statut="en attente"
        )
        db.add(nouvelle_commande)
        db.commit()
        db.refresh(nouvelle_commande)

        total_commande = 0

        for produit in commande.produits:
            produit_commande = models.CommandeProduit(
                id=str(uuid4()),
                commande_id=nouvelle_commande.id,
                produit_id=produit.produit_id,
                quantite=produit.quantite
            )
            db.add(produit_commande)
            total_commande += 10.0 * produit.quantite

        nouvelle_commande.total = total_commande
        db.commit()
        db.refresh(nouvelle_commande)

        return nouvelle_commande

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[schemas.Commande])
def get_commandes(db: Session = Depends(get_db)):
    commandes = db.query(models.Commande).all()
    return commandes

@router.put("/{commande_id}", response_model=schemas.Commande)
def mettre_a_jour_statut(commande_id: str, update: schemas.UpdateStatutCommande, db: Session = Depends(get_db)):
    commande = db.query(models.Commande).filter(models.Commande.id == commande_id).first()

    if not commande:
        raise HTTPException(status_code=404, detail="Commande non trouvée")

    commande.statut = update.statut
    db.commit()
    db.refresh(commande)

    return commande
