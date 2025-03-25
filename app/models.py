from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Commande(Base):
    __tablename__ = "commandes"

    id = Column(String, primary_key=True, index=True)
    total = Column(DECIMAL(10, 2))
    statut = Column(String(50), default="en attente")
    date_commande = Column(DateTime(timezone=True), server_default=func.now())
    produits = relationship("CommandeProduit", back_populates="commande")

class CommandeProduit(Base):
    __tablename__ = "commandes_produits"

    id = Column(String, primary_key=True, index=True)
    commande_id = Column(String, ForeignKey("commandes.id"))
    produit_id = Column(String)
    quantite = Column(Integer)
    commande = relationship("Commande", back_populates="produits")