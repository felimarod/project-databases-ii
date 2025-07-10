import dotenv from 'dotenv';
import { Price } from './core/entities';
import Database from './core/services/db';
import Api from './api';

// Cargar variables de entorno
dotenv.config();

async function main() {
  try {
    // Obtener instancia de la base de datos y conectar
    const database = Database.getInstance();
    const db = await database.connect();
    
    console.log("Conectado a MongoDB");
    console.log("Base de datos:", db.databaseName);
    
    // Listar colecciones disponibles
    const collections = await db.listCollections().toArray();
    console.log("Colecciones disponibles:", collections.map(c => c.name).join(", "));
    
    // // Ejemplo: Inicializar colecciones basadas en los modelos
    console.log("Inicializando colecciones basadas en los modelos definidos...");
    
    // 1. Market Data Time Series Collections
    const pricesCollection = db.collection<Price>('prices');
    const indicatorsCollection = db.collection('indicators');
    const marketDataCollection = db.collection('market_data');
    
    // 2. Analytics Collections
    // Market Analysis
    const liquidityMetricsCollection = db.collection('liquidity_metrics');
    const marketAnalysisCollection = db.collection('market_analysis');
    const predictionsCollection = db.collection('predictions');
    const technicalSignalsCollection = db.collection('technical_signals');
    const volatilityAnalysisCollection = db.collection('volatility_analysis');
    
    // Strategy Performance
    const executionQualityCollection = db.collection('execution_quality');
    const riskMetricsCollection = db.collection('risk_metrics');
    const strategyPerformanceCollection = db.collection('strategy_performance');
    
    // 3. Support System Collections
    // Agents
    const agentsCollection = db.collection('agents');
    const performanceMetricsCollection = db.collection('agent_performance_metrics');
    
    // Support Requests
    const supportRequestsCollection = db.collection('support_requests');
    const responsesCollection = db.collection('support_responses');
    const slaMetricsCollection = db.collection('sla_metrics');
    const userAttachmentsCollection = db.collection('user_attachments');
    
    // Trading Alerts
    const tradingAlertsCollection = db.collection('trading_alerts');
    const marketDataSnapshotCollection = db.collection('market_data_snapshots');
    const triggerConditionsCollection = db.collection('trigger_conditions');
    
    console.log("Colecciones inicializadas correctamente");
    
    // Ejemplo: Insertar un documento de prueba
    // const testDoc: Price = {
    //     open: 1,
    //     close: 2,
    //     high: 3,
    //     low: 4,
    //     ask: 5,
    //     bid: 6,
    // };
    
    // console.log("Estructura de la colección 'prices':", testDoc);
    // const result = await pricesCollection.insertOne(testDoc);
    // console.log(`Documento insertado: ${JSON.stringify(result)}`);

    // await pricesCollection.find({}).toArray().then(docs => {
    //   console.log("Documentos en la colección 'prices':", docs);
    // });
    
    // Cerrar la conexión cuando termine
    process.on('SIGINT', async () => {
      await database.disconnect();
      process.exit(0);
    });
    
    
    // Iniciar la API
    const api = new Api(3000);
    api.start();
    
    console.log("Aplicación ejecutándose. Presiona Ctrl+C para salir.");
    
  } catch (error) {
    console.error("Error en la aplicación:", error);
    process.exit(1);
  }
}

// Ejecutar la función principal
main().catch(console.error);
