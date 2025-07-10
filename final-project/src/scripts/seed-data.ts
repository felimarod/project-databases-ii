import { MongoClient, ObjectId } from 'mongodb';
import * as dotenv from 'dotenv';
import {
  generatePrices,
  generateIndicators,
  generateMarketData,
  generateLiquidityMetrics,
  generateMarketAnalysis,
  generatePredictions,
  generateTechnicalSignals,
  generateVolatilityAnalysis,
  generateStrategyPerformance,
  generateRiskMetrics,
  generateExecutionQuality,
  generateAgents,
  generatePerformanceMetrics,
  generateSupportRequests,
  generateResponses,
  generateSlaMetrics,
  generateUserAttachments,
  generateTradingAlerts,
  generateMarketDataSnapshots,
  generateTriggerConditions
} from './generators';

// Cargar variables de entorno
dotenv.config();

// Número de documentos a insertar para cada colección
const COUNT = 100;

async function main() {
  console.log('Iniciando generación de datos...');
  
  const uri = process.env.MONGODB_URI || 'mongodb://localhost:27017/trading_analytics_db';
  const client = new MongoClient(uri);
  
  try {
    await client.connect();
    console.log('Conectado a MongoDB');
    
    const db = client.db();
    console.log(`Base de datos: ${db.databaseName}`);
    
    // Limpiar colecciones existentes
    console.log('Eliminando datos existentes...');
    await Promise.all([
      db.collection('prices').deleteMany({}),
      db.collection('indicators').deleteMany({}),
      db.collection('market_data').deleteMany({}),
      
      db.collection('liquidity_metrics').deleteMany({}),
      db.collection('market_analysis').deleteMany({}),
      db.collection('predictions').deleteMany({}),
      db.collection('technical_signals').deleteMany({}),
      db.collection('volatility_analysis').deleteMany({}),
      
      db.collection('strategy_performance').deleteMany({}),
      db.collection('risk_metrics').deleteMany({}),
      db.collection('execution_quality').deleteMany({}),
      
      db.collection('agents').deleteMany({}),
      db.collection('agent_performance_metrics').deleteMany({}),
      
      db.collection('support_requests').deleteMany({}),
      db.collection('support_responses').deleteMany({}),
      db.collection('sla_metrics').deleteMany({}),
      db.collection('user_attachments').deleteMany({}),
      
      db.collection('trading_alerts').deleteMany({}),
      db.collection('market_data_snapshots').deleteMany({}),
      db.collection('trigger_conditions').deleteMany({})
    ]);
    
    // Market Data Time Series Collections
    console.log(`Generando ${COUNT} documentos para cada colección...`);
    
    const prices = generatePrices(COUNT);
    const indicators = generateIndicators(COUNT);
    const marketData = generateMarketData(COUNT);
    
    // Analytics Collections - Market Analysis
    const liquidityMetrics = generateLiquidityMetrics(COUNT);
    const marketAnalysis = generateMarketAnalysis(COUNT);
    const predictions = generatePredictions(COUNT);
    const technicalSignals = generateTechnicalSignals(COUNT);
    const volatilityAnalysis = generateVolatilityAnalysis(COUNT);
    
    // Analytics Collections - Strategy Performance
    const strategyPerformance = generateStrategyPerformance(COUNT);
    const riskMetrics = generateRiskMetrics(COUNT);
    const executionQuality = generateExecutionQuality(COUNT);
    
    // Support System Collections - Agents
    const agents = generateAgents(COUNT);
    const performanceMetrics = generatePerformanceMetrics(COUNT);
    
    // Support System Collections - Support Requests
    const supportRequests = generateSupportRequests(COUNT);
    const responses = generateResponses(COUNT);
    const slaMetrics = generateSlaMetrics(COUNT);
    const userAttachments = generateUserAttachments(COUNT);
    
    // Support System Collections - Trading Alerts
    const tradingAlerts = generateTradingAlerts(COUNT);
    const marketDataSnapshots = generateMarketDataSnapshots(COUNT);
    const triggerConditions = generateTriggerConditions(COUNT);
    
    // Insertar todos los datos generados
    console.log('Insertando datos en MongoDB...');
    
    // Convertir los IDs de string a ObjectId para las entidades que lo necesitan
  const convertedMarketData = marketData.map(doc => ({
    ...doc,
    _id: new ObjectId(doc._id)
  }));
  
  const convertedMarketAnalysis = marketAnalysis.map(doc => ({
    ...doc,
    _id: new ObjectId(doc._id)
  }));
  
  const convertedStrategyPerformance = strategyPerformance.map(doc => ({
    ...doc,
    _id: new ObjectId(doc._id)
  }));
  
  const convertedAgents = agents.map(doc => ({
    ...doc,
    _id: new ObjectId(doc._id)
  }));
  
  const convertedSupportRequests = supportRequests.map(doc => ({
    ...doc,
    _id: new ObjectId(doc._id)
  }));
  
  const convertedTradingAlerts = tradingAlerts.map(doc => ({
    ...doc,
    _id: new ObjectId(doc._id)
  }));

  const results = await Promise.all([
      db.collection('prices').insertMany(prices),
      db.collection('indicators').insertMany(indicators),
      db.collection('market_data').insertMany(convertedMarketData),
      
      db.collection('liquidity_metrics').insertMany(liquidityMetrics),
      db.collection('market_analysis').insertMany(convertedMarketAnalysis),
      db.collection('predictions').insertMany(predictions),
      db.collection('technical_signals').insertMany(technicalSignals),
      db.collection('volatility_analysis').insertMany(volatilityAnalysis),
      
      db.collection('strategy_performance').insertMany(convertedStrategyPerformance),
      db.collection('risk_metrics').insertMany(riskMetrics),
      db.collection('execution_quality').insertMany(executionQuality),
      
      db.collection('agents').insertMany(convertedAgents),
      db.collection('agent_performance_metrics').insertMany(performanceMetrics),
      
      db.collection('support_requests').insertMany(convertedSupportRequests),
      db.collection('support_responses').insertMany(responses),
      db.collection('sla_metrics').insertMany(slaMetrics),
      db.collection('user_attachments').insertMany(userAttachments),
      
      db.collection('trading_alerts').insertMany(convertedTradingAlerts),
      db.collection('market_data_snapshots').insertMany(marketDataSnapshots),
      db.collection('trigger_conditions').insertMany(triggerConditions)
    ]);
    
    console.log('Datos insertados correctamente:');
    results.forEach((result, index) => {
      const collectionNames = [
        'prices', 'indicators', 'market_data',
        'liquidity_metrics', 'market_analysis', 'predictions', 'technical_signals', 'volatility_analysis',
        'strategy_performance', 'risk_metrics', 'execution_quality',
        'agents', 'agent_performance_metrics',
        'support_requests', 'support_responses', 'sla_metrics', 'user_attachments',
        'trading_alerts', 'market_data_snapshots', 'trigger_conditions'
      ];
      console.log(`${collectionNames[index]}: ${result.insertedCount} documentos`);
    });
    
  } catch (error) {
    console.error('Error durante la generación de datos:', error);
  } finally {
    await client.close();
    console.log('Conexión a MongoDB cerrada');
  }
}

main().catch(console.error);
