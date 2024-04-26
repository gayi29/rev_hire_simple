from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import sqlite3

# Initialize FastAPI app
app = FastAPI()

# SQLite database connection
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create a table to store data if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    description TEXT
                )''')
conn.commit()

# Pydantic model for item
class Item(BaseModel):
    name: str
    description: str

# Endpoint to add data to the database
@app.post("/items/")
async def create_item(item: Item):
    cursor.execute("INSERT INTO items (name, description) VALUES (?, ?)", (item.name, item.description))
    conn.commit()
    return {"message": "Item added successfully"}

# Endpoint to get all data from the database
@app.get("/items/")
async def get_items():
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    return {"items": items}

# Dependency to get database connection
def get_db():
    try:
        yield conn
    finally:
        conn.close()

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
