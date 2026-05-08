"""
Test connections to all external services.
Run with: uv run python shared/test_connections.py
"""

import os
from dotenv import load_dotenv

load_dotenv()


def test_alpaca():
    """Test Alpaca paper trading API."""
    import requests

    url = "https://paper-api.alpaca.markets/v2/account"
    headers = {
        "APCA-API-KEY-ID": os.getenv("ALPACA_API_KEY"),
        "APCA-API-SECRET-KEY": os.getenv("ALPACA_SECRET_KEY"),
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print(f"✅ Alpaca OK — Account status: {data.get('status')}")
        return True
    else:
        print(f"❌ Alpaca FAILED — Status {response.status_code}: {response.text}")
        return False


def test_fred():
    """Test FRED API."""
    import requests

    api_key = os.getenv("FRED_API_KEY")
    url = (
        f"https://api.stlouisfed.org/fred/series?"
        f"series_id=GDP&api_key={api_key}&file_type=json"
    )
    response = requests.get(url)

    if response.status_code == 200:
        print(f"✅ FRED OK — API key valid")
        return True
    else:
        print(f"❌ FRED FAILED — Status {response.status_code}: {response.text}")
        return False


def test_postgres():
    """Test PostgreSQL connection."""
    import psycopg2

    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        print(f"✅ PostgreSQL OK — {version[:50]}...")
        return True
    except Exception as e:
        print(f"❌ PostgreSQL FAILED — {e}")
        return False


if __name__ == "__main__":
    print("Testing connections...\n")
    alpaca_ok = test_alpaca()
    fred_ok = test_fred()
    postgres_ok = test_postgres()
    print()
    if all([alpaca_ok, fred_ok, postgres_ok]):
        print("🎉 All connections working!")
    else:
        print("⚠️  Some connections failed. Check the errors above.")