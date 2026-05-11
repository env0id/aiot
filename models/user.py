from sqlalchemy import Column, Integer, DateTime, String, Boolean, func, BigInteger
from services.language import LanguageService
from models.base import Base


class User(Base):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True)
  telegram_username = Column(String, nullable=True)
  telegram_id = Column(BigInteger, nullable=False, unique=True)
  full_name = Column(String, nullable=True)
  registered_at = Column(DateTime, default=func.now())
  can_receive_messages = Column(Boolean, default=True)
  language = Column(String, default=LanguageService.get_default_code())