from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class NewsHeadline(Base):
    __tablename__ = 'news_headlines'

    id = Column(Integer, primary_key=True)
    source = Column(String(50), nullable=False)
    language = Column(String(20), nullable=False)
    headline = Column(Text, nullable=False)
    sentiment_score = Column(Integer)

class DatabaseHandler:
    def __init__(self, db_url='sqlite:///news_headlines.db'):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_headline(self, source, language, headline, sentiment_score):
        session = self.Session()
        new_headline = NewsHeadline(source=source, language=language, headline=headline, sentiment_score=sentiment_score)
        session.add(new_headline)
        session.commit()
        session.close()

    def get_headlines(self, source=None, language=None):
        session = self.Session()
        query = session.query(NewsHeadline)
        if source:
            query = query.filter(NewsHeadline.source == source)
        if language:
            query = query.filter(NewsHeadline.language == language)
        results = query.all()
        session.close()
        return results

    def clear_headlines(self):
        session = self.Session()
        session.query(NewsHeadline).delete()
        session.commit()
        session.close()