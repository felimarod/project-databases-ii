import { MongoClient, Db, ServerApiVersion } from 'mongodb';
import dotenv from 'dotenv';

dotenv.config();

class Database {
  private static instance: Database;
  private client: MongoClient;
  private db: Db | null = null;
  
  private constructor() {
    const uri = process.env.MONGO_URL || 'mongodb://localhost:27017/trading_analytics_db';
    this.client = new MongoClient(uri, {
      serverApi: {
        version: ServerApiVersion.v1,
        strict: true,
        deprecationErrors: true,
      }
    });
  }

  public static getInstance(): Database {
    if (!Database.instance) {
      Database.instance = new Database();
    }
    return Database.instance;
  }

  public async connect(): Promise<Db> {
    if (!this.db) {
      try {
        await this.client.connect();
        console.log("✅ Conexión a MongoDB establecida con éxito");
        
        this.db = this.client.db();
      } catch (error) {
        console.error("❌ Error al conectar a MongoDB:", error);
        throw error;
      }
    }
    return this.db;
  }

  public async disconnect(): Promise<void> {
    if (this.client) {
      await this.client.close();
      this.db = null;
      console.log("Conexión a MongoDB cerrada");
    }
  }
  
  public getDb(): Db {
    if (!this.db) {
      throw new Error("La base de datos no está conectada. Llame a connect() primero.");
    }
    return this.db;
  }
}

export default Database;