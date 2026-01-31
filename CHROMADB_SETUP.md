# ChromaDB Setup - Zero Configuration! 🎉

## Why ChromaDB?

✅ **No installation needed** - Just `pip install chromadb`  
✅ **No server setup** - Embedded database  
✅ **No configuration** - Works out of the box  
✅ **Persistent** - Data saved to disk automatically  
✅ **Fast** - Perfect for hackathons and demos  

## Setup (2 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

That's it! ChromaDB is installed.

### Step 2: Add Sample Data (Optional)
```bash
python seed_chromadb.py
```

This creates:
- 2 Owners
- 3 Trucks
- 3 Drivers
- 3 Vendors
- 2 Trips (1 deadheading)
- 4 Available Loads

### Step 3: Start Server
```bash
python main.py
```

Done! Your data is stored in `./chroma_data/` directory.

## How It Works

ChromaDB stores data as:
- **Collections**: Like tables (owners, drivers, trips, loads, etc.)
- **Documents**: Searchable text
- **Metadata**: JSON data for each record
- **IDs**: Unique identifiers

All data is automatically persisted to disk in `./chroma_data/`.

## Advantages Over PostgreSQL

| Feature | ChromaDB | PostgreSQL |
|---------|----------|------------|
| Setup Time | 0 minutes | 30+ minutes |
| Installation | pip install | Download & install server |
| Configuration | None | Connection strings, users, passwords |
| Portability | Copy folder | Dump & restore |
| Perfect for | Hackathons, demos, prototypes | Production systems |

## Data Location

All data is stored in: `./chroma_data/`

To backup: Just copy this folder  
To reset: Delete this folder  
To share: Zip and send  

## Testing

```bash
# Add sample data
python seed_chromadb.py

# Clear all data
python seed_chromadb.py --clear

# Test the API
python test_api.py
```

## Migration to Production

When you're ready for production, you can easily migrate to PostgreSQL:
1. Export data from ChromaDB
2. Import to PostgreSQL
3. Update connection string

But for hackathons and demos, ChromaDB is perfect! 🚀
