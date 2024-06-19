from django.conf import settings
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Numeric, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, validates

Base = declarative_base()

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
session = sessionmaker(bind=engine)()


class Wallet(Base):
    __tablename__ = 'wallet'

    id = Column(Integer, primary_key=True)
    label = Column(String(255))
    balance = Column(Integer, default=0)

    transaction = relationship("Transaction", back_populates="wallet")
    __table_args__ = (
        Index('idx_wallet_label', 'label'),
    )

    @validates('balance')
    def validate_balance(self, key, balance):
        if balance < 0:
            raise ValueError("Wallet balance cannot be negative")
        return balance


class Transaction(Base):
    __tablename__ = 'transaction'

    id = Column(Integer, primary_key=True)
    wallet_id = Column(Integer, ForeignKey('wallet.id'))
    txid = Column(String(255), unique=True)
    amount = Column(Numeric(36, 18))

    wallet = relationship("Wallet", back_populates="transaction")

    __table_args__ = (
        Index('idx_transaction_wallet_id', 'txid'),
    )

    def save(self):
        self.wallet.balance += self.amount
        if self.wallet.balance < 0:
            raise ValueError("Wallet balance cannot be negative")

        session.add(self)
        session.add(self.wallet)
        session.commit()

    def delete(self):
        self.wallet.balance -= self.amount
        if self.wallet.balance < 0:
            raise ValueError("Wallet balance cannot be negative")

        session.delete(self)
        session.add(self.wallet)
        session.commit()
