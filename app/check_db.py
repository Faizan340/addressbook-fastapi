from sqlalchemy import create_engine, text

DATABASE_URL = "sqlite:///./addresses.db"

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM addresses"))
    rows = result.fetchall()

    print(f"Total rows: {len(rows)}")
    for row in rows:
        print(row)
