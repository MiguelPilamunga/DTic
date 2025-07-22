import requests
import json
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Proxy(Base):
    __tablename__ = 'proxies'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    alive = Column(Boolean)
    alive_since = Column(Float)
    anonymity = Column(String(50))
    average_timeout = Column(Float)
    first_seen = Column(Float)
    ip_data = Column(Text)
    ip_data_last_update = Column(Integer)
    last_seen = Column(Float)
    port = Column(Integer)
    protocol = Column(String(20))
    proxy = Column(String(100))
    ssl = Column(Boolean)
    timeout = Column(Float)
    times_alive = Column(Integer)
    times_dead = Column(Integer)
    uptime = Column(Float)
    ip = Column(String(45))
    created_at = Column(DateTime, default=datetime.utcnow)

engine = create_engine('sqlite:///proxies.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def fetch_and_store_proxies():
    session = Session()
    
    try:
        session.query(Proxy).delete()
        session.commit()
        
        url = "https://api.proxyscrape.com/v4/free-proxy-list/get"
        params = {
            'request': 'get_proxies',
            'skip': 0,
            'proxy_format': 'protocolipport',
            'format': 'json',
            'limit': 15
        }
        
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
            'Origin': 'https://es.proxyscrape.com',
            'Referer': 'https://es.proxyscrape.com/'
        }
        
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        
        for proxy_data in data['proxies']:
            proxy = Proxy(
                alive=proxy_data['alive'],
                alive_since=proxy_data['alive_since'],
                anonymity=proxy_data['anonymity'],
                average_timeout=proxy_data['average_timeout'],
                first_seen=proxy_data['first_seen'],
                ip_data=json.dumps(proxy_data['ip_data']),
                ip_data_last_update=proxy_data['ip_data_last_update'],
                last_seen=proxy_data['last_seen'],
                port=proxy_data['port'],
                protocol=proxy_data['protocol'],
                proxy=proxy_data['proxy'],
                ssl=proxy_data['ssl'],
                timeout=proxy_data['timeout'],
                times_alive=proxy_data['times_alive'],
                times_dead=proxy_data['times_dead'],
                uptime=proxy_data['uptime'],
                ip=proxy_data['ip']
            )
            session.add(proxy)
        
        session.commit()
        print(f"Successfully stored {len(data['proxies'])} proxies")
        
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    fetch_and_store_proxies()