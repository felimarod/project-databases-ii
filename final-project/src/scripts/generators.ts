import {
  getRandomNumber,
  getRandomDate,
  getRandomItem,
  getRandomItems,
  getRandomId,
  generateArray,
  instruments,
  timeframes,
  sources,
  categories,
  priorities,
  statuses,
  types,
  departments,
  marketConditions
} from './utils';

// Interfaces
import { Price } from '../core/entities/market-data-time-series-collection/prices.model';
import { Indicator } from '../core/entities/market-data-time-series-collection/indicator.model';
import { MarketData } from '../core/entities/market-data-time-series-collection/market-data.model';
import { MarketCondition } from '../core/entities/market-data-time-series-collection/market-condition';

import { LiquidityMetric } from '../core/entities/analytics-collections/martket-analysis/liquidity-metrics.model';
import { MarketAnalysis } from '../core/entities/analytics-collections/martket-analysis/market-analysis.model';
import { Prediction } from '../core/entities/analytics-collections/martket-analysis/predictions.model';
import { TechnicalSignal } from '../core/entities/analytics-collections/martket-analysis/technical-signals.model';
import { VolatilityAnalysis } from '../core/entities/analytics-collections/martket-analysis/volatility-analysis.model';

import { ExecutionQuality } from '../core/entities/analytics-collections/strategy-performance/execution-quality.model';
import { RiskMetrics } from '../core/entities/analytics-collections/strategy-performance/risk-metrics.model';
import { StrategyPerformance } from '../core/entities/analytics-collections/strategy-performance/strategy-performance.model';

import { Agent } from '../core/entities/support-system-collections/agents/agent.model';
import { PerformanceMetrics } from '../core/entities/support-system-collections/agents/performance-metrics.model';
import { SupportRequest } from '../core/entities/support-system-collections/support-requests/support-request.model';
import { Response as SupportResponse } from '../core/entities/support-system-collections/support-requests/responses.model';
import { SlaMetrics } from '../core/entities/support-system-collections/support-requests/sla-metrics.model';
import { UserAttachment } from '../core/entities/support-system-collections/support-requests/user-attachments.model';

import { TradingAlert } from '../core/entities/support-system-collections/trading-alerts/trading-alerts.model';
import { MarketDataSnapshot } from '../core/entities/support-system-collections/trading-alerts/market-data-snapshot.model';
import { TriggerCondition } from '../core/entities/support-system-collections/trading-alerts/trigger-conditions.model';

// Market Data Time Series Collections
export function generatePrices(count: number): Price[] {
  return generateArray(count, () => ({
    open: getRandomNumber(50, 200),
    high: getRandomNumber(50, 200),
    low: getRandomNumber(50, 200),
    close: getRandomNumber(50, 200),
    bid: getRandomNumber(50, 200),
    ask: getRandomNumber(50, 200)
  }));
}

export function generateIndicators(count: number): Indicator[] {
  return generateArray(count, () => ({
    sma_20: getRandomNumber(100, 200),
    ema_12: getRandomNumber(100, 200),
    ema_26: getRandomNumber(100, 200),
    rsi: getRandomNumber(0, 100),
    macd: getRandomNumber(-10, 10),
    bollinger_upper: getRandomNumber(150, 250),
    bollinger_lower: getRandomNumber(50, 150),
    atr: getRandomNumber(0, 10, 4)
  }));
}

export function generateMarketData(count: number): MarketData[] {
  const startDate = new Date('2023-01-01');
  const endDate = new Date();
  
  return generateArray(count, () => {
    const pricesCount = Math.floor(Math.random() * 5) + 1;
    const indicatorsCount = Math.floor(Math.random() * 3) + 1;
    
    const market_condition: MarketCondition = {
      volatility_regime: getRandomItem(['low', 'medium', 'high']),
      trend_direction: getRandomItem(['uptrend', 'downtrend', 'sideways']),
      liquidity_level: getRandomItem(['high', 'medium', 'low'])
    };
    
    return {
      _id: getRandomId(),
      instrument: getRandomItem(instruments),
      timestamp: getRandomDate(startDate, endDate),
      source: getRandomItem(sources),
      volume: getRandomNumber(1000, 10000000),
      spread: getRandomNumber(0.01, 2, 4),
      tick_count: Math.floor(getRandomNumber(100, 10000)),
      prices: generatePrices(pricesCount),
      indicators: generateIndicators(indicatorsCount),
      market_condition
    };
  });
}

// Analytics Collections - Market Analysis
export function generateLiquidityMetrics(count: number): LiquidityMetric[] {
  return generateArray(count, () => ({
    bid_ask_spread: getRandomNumber(0.01, 1, 4),
    market_depth: getRandomNumber(1000, 100000),
    trading_volume: getRandomNumber(10000, 1000000)
  }));
}

export function generateMarketAnalysis(count: number): MarketAnalysis[] {
  const startDate = new Date('2023-01-01');
  const endDate = new Date();
  
  return generateArray(count, () => {
    const technicalSignalsCount = Math.floor(Math.random() * 3) + 1;
    const predictionsCount = Math.floor(Math.random() * 5) + 1;
    
    return {
      _id: getRandomId(),
      instrument: getRandomItem(instruments),
      analysis_date: getRandomDate(startDate, endDate),
      timeframe: getRandomItem(timeframes),
      technical_signals: generateTechnicalSignals(technicalSignalsCount),
      volatility_analysis: generateVolatilityAnalysis(1)[0],
      liquidity_metrics: generateLiquidityMetrics(1)[0],
      predictions: generatePredictions(predictionsCount)
    };
  });
}

export function generatePredictions(count: number): Prediction[] {
  return generateArray(count, () => ({
    price_direction: getRandomItem(['up', 'down', 'neutral']),
    confidence_level: getRandomNumber(0, 1, 4),
    time_horizon: getRandomItem(['short-term', 'medium-term', 'long-term'])
  }));
}

export function generateTechnicalSignals(count: number): TechnicalSignal[] {
  return generateArray(count, () => {
    const supportLevels = Array.from({ length: Math.floor(Math.random() * 3) + 1 }, 
      () => getRandomNumber(50, 150));
    const resistanceLevels = Array.from({ length: Math.floor(Math.random() * 3) + 1 }, 
      () => getRandomNumber(150, 250));
      
    return {
      trend_direction: getRandomItem(['up', 'down', 'neutral']),
      momentum: getRandomItem(['strong', 'weak', 'neutral']),
      support_levels: supportLevels,
      resistance_levels: resistanceLevels
    };
  });
}

export function generateVolatilityAnalysis(count: number): VolatilityAnalysis[] {
  return generateArray(count, () => ({
    current_volatility: getRandomNumber(0, 100, 4),
    volatility_percentile: getRandomNumber(0, 1, 4),
    volatility_regime: getRandomItem(['low', 'medium', 'high'])
  }));
}

// Analytics Collections - Strategy Performance
export function generateStrategyPerformance(count: number): StrategyPerformance[] {
  const startDate = new Date('2023-01-01');
  const endDate = new Date();
  
  return generateArray(count, () => ({
    _id: getRandomId(),
    strategy_id: getRandomId(),
    date: getRandomDate(startDate, endDate),
    daily_pnl: getRandomNumber(-10000, 10000, 2),
    trades_count: Math.floor(getRandomNumber(1, 100)),
    win_rate: getRandomNumber(0, 1, 4),
    avg_trade_duration: getRandomNumber(30, 3600),
    max_drawdown: getRandomNumber(0, 0.5, 4),
    sharpe_ratio: getRandomNumber(-3, 5, 4),
    volatility: getRandomNumber(0, 0.5, 4),
    market_conditions: getRandomItems(marketConditions, Math.floor(Math.random() * 3) + 1)
  }));
}

export function generateRiskMetrics(count: number): RiskMetrics[] {
  return generateArray(count, () => ({
    var_95: getRandomNumber(0, 0.2, 4),
    expected_shortfall: getRandomNumber(0, 0.3, 4),
    beta: getRandomNumber(-2, 2, 4)
  }));
}

export function generateExecutionQuality(count: number): ExecutionQuality[] {
  return generateArray(count, () => ({
    avg_slippage: getRandomNumber(0, 10, 4),
    avg_execution_time: getRandomNumber(10, 1000, 2),
    fill_rate: getRandomNumber(0.5, 1, 4)
  }));
}

// Support System Collections - Agents
export function generateAgents(count: number): Agent[] {
  const startDate = new Date('2020-01-01');
  const endDate = new Date('2023-01-01');
  
  const names = ['Alex', 'Jamie', 'Jordan', 'Taylor', 'Morgan', 'Casey', 'Riley', 'Quinn', 'Sam', 'Cameron'];
  const lastNames = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Miller', 'Davis', 'Garcia', 'Rodriguez', 'Wilson'];
  
  return generateArray(count, () => {
    const name = `${getRandomItem(names)} ${getRandomItem(lastNames)}`;
    const email = `${name.toLowerCase().replace(' ', '.')}@tradingcompany.com`;
    
    return {
      _id: getRandomId(),
      agent_id: `AG${Math.floor(Math.random() * 10000).toString().padStart(4, '0')}`,
      name,
      email,
      department: getRandomItem(departments),
      status: getRandomItem(['active', 'inactive', 'training']),
      specializations: getRandomItems(categories, Math.floor(Math.random() * 3) + 1),
      created_at: getRandomDate(startDate, endDate),
      performance_metrics: generatePerformanceMetrics(1)[0]
    };
  });
}

export function generatePerformanceMetrics(count: number): PerformanceMetrics[] {
  return generateArray(count, () => ({
    avg_response_time: getRandomNumber(1, 60),
    resolution_rate: getRandomNumber(0.5, 1, 2),
    customer_rating: getRandomNumber(1, 5, 1),
    tickets_handled: Math.floor(getRandomNumber(10, 500))
  }));
}

// Support System Collections - Support Requests
export function generateSupportRequests(count: number): SupportRequest[] {
  const startDate = new Date('2023-01-01');
  const endDate = new Date();
  
  const subjects = [
    'Problema con la plataforma',
    'Error al ejecutar operación',
    'Consulta sobre comisiones',
    'Problema de conexión',
    'Solicitud de información',
    'Problema con depósito',
    'Consulta sobre retiros',
    'Reporte de error en gráficos',
    'Solicitud de característica',
    'Problema de autenticación'
  ];
  
  const descriptions = [
    'Estoy experimentando problemas para acceder a la plataforma. Me aparece un error después de iniciar sesión.',
    'Cuando intento realizar una operación de compra, el sistema muestra un error de ejecución.',
    'Me gustaría obtener información detallada sobre las comisiones aplicadas a mis operaciones recientes.',
    'Estoy teniendo problemas de conexión intermitentes con la plataforma durante las horas de mercado.',
    'Necesito información sobre cómo configurar alertas de precio para determinados instrumentos.',
    'Mi depósito realizado hace 2 días aún no se refleja en mi cuenta.',
    'Me gustaría saber cuál es el tiempo estimado para procesar mi solicitud de retiro.',
    'Los gráficos de velas no se cargan correctamente para algunos pares de divisas.',
    'Me gustaría sugerir una nueva característica para la plataforma: alertas personalizadas basadas en indicadores.',
    'No puedo acceder a mi cuenta a pesar de ingresar las credenciales correctamente.'
  ];
  
  return generateArray(count, () => {
    const created_at = getRandomDate(startDate, endDate);
    let updated_at = new Date(created_at);
    updated_at.setHours(updated_at.getHours() + Math.floor(Math.random() * 48));
    
    let resolved_at = null;
    const isResolved = Math.random() > 0.3;
    
    if (isResolved) {
      resolved_at = new Date(updated_at);
      resolved_at.setHours(resolved_at.getHours() + Math.floor(Math.random() * 24));
    }
    
    const subjectIndex = Math.floor(Math.random() * subjects.length);
    const responseCount = Math.floor(Math.random() * 5) + 1;
    const attachmentCount = Math.floor(Math.random() * 3);
    
    return {
      _id: getRandomId(),
      ticket_id: `TICK-${Math.floor(Math.random() * 100000)}`,
      user_id: `user_${Math.floor(Math.random() * 1000)}`,
      type: getRandomItem(types),
      category: getRandomItem(categories),
      priority: getRandomItem(priorities),
      status: getRandomItem(statuses),
      subject: subjects[subjectIndex],
      description: descriptions[subjectIndex],
      created_at,
      updated_at,
      resolved_at,
      tags: getRandomItems(categories, Math.floor(Math.random() * 3) + 1),
      escalation_level: Math.floor(Math.random() * 3),
      user_attachments: generateUserAttachments(attachmentCount),
      responses: generateResponses(responseCount),
      sla_metrics: generateSlaMetrics(1)[0]
    };
  });
}

export function generateResponses(count: number): SupportResponse[] {
  const startDate = new Date('2023-01-01');
  const endDate = new Date();
  
  const contents = [
    'Gracias por contactarnos. Estamos revisando su caso y le responderemos a la brevedad.',
    'Hemos identificado el problema y estamos trabajando en una solución.',
    'El problema ha sido resuelto. Por favor, intente nuevamente y háganos saber si persiste.',
    'Para resolver este problema, necesitamos que verifique su cuenta siguiendo los pasos que le enviamos por correo.',
    'Su solicitud ha sido escalada a nuestro equipo de soporte técnico especializado.',
    'La funcionalidad solicitada está en nuestro roadmap y se implementará en los próximos meses.',
    'Hemos añadido los fondos a su cuenta. Puede verificarlo iniciando sesión.',
    'Le recomendamos reiniciar la aplicación y borrar la caché para resolver este problema.',
    'Nota interna: el usuario requiere verificación adicional antes de proceder.',
    'He actualizado su cuenta con los permisos necesarios. Ya debería poder acceder a esa funcionalidad.'
  ];

  const names = ['Alex', 'Jamie', 'Jordan', 'Taylor', 'Morgan', 'Casey', 'Riley', 'Quinn', 'Sam', 'Cameron'];
  const lastNames = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Miller', 'Davis', 'Garcia', 'Rodriguez', 'Wilson'];
  
  return generateArray(count, () => {
    const agent_name = `${getRandomItem(names)} ${getRandomItem(lastNames)}`;
    const timestamp = getRandomDate(startDate, endDate);
    
    return {
      response_id: getRandomId(),
      agent_id: `AG${Math.floor(Math.random() * 10000).toString().padStart(4, '0')}`,
      agent_name,
      message: getRandomItem(contents),
      response_type: getRandomItem(['text', 'image', 'file']),
      timestamp
    };
  });
}

export function generateSlaMetrics(count: number): SlaMetrics[] {
  return generateArray(count, () => ({
    first_response_time: getRandomNumber(1, 120),
    resolution_time: getRandomNumber(60, 4320),
    escalation_count: Math.floor(getRandomNumber(0, 3))
  }));
}

export function generateUserAttachments(count: number): UserAttachment[] {
  const startDate = new Date('2023-01-01');
  const endDate = new Date();
  
  const fileNames = ['screenshot.png', 'error_log.txt', 'account_statement.pdf', 'trade_history.csv', 'platform_settings.json'];
  const fileTypes = ['image/png', 'text/plain', 'application/pdf', 'text/csv', 'application/json'];
  
  return generateArray(count, () => {
    const fileIndex = Math.floor(Math.random() * fileNames.length);
    
    return {
      filename: fileNames[fileIndex],
      content_type: fileTypes[fileIndex],
      file_size: Math.floor(getRandomNumber(10, 5000)),
      uploaded_at: getRandomDate(startDate, endDate),
      url: `https://storage.example.com/attachments/${getRandomId()}/${fileNames[fileIndex]}`
    };
  });
}

// Support System Collections - Trading Alerts
export function generateTradingAlerts(count: number): TradingAlert[] {
  const startDate = new Date('2023-01-01');
  const endDate = new Date();
  
  const alertMessages = [
    'Precio por encima del umbral de resistencia',
    'Volumen inusualmente alto detectado',
    'Señal de tendencia alcista confirmada',
    'RSI en zona de sobreventa',
    'Patrón de vela Doji detectado',
    'Cruce de medias móviles detectado',
    'Divergencia RSI-Precio identificada',
    'Ruptura de canal de tendencia',
    'Nivel de soporte importante alcanzado',
    'Volatilidad aumentando significativamente'
  ];
  
  return generateArray(count, () => {
    const generated_at = getRandomDate(startDate, endDate);
    let sent_at = null;
    
    if (Math.random() > 0.2) {
      sent_at = new Date(generated_at);
      sent_at.setMinutes(sent_at.getMinutes() + Math.floor(Math.random() * 10));
    }
    
    const triggerCount = Math.floor(Math.random() * 3) + 1;
    
    return {
      _id: getRandomId(),
      user_id: `user_${Math.floor(Math.random() * 1000)}`,
      strategy_id: getRandomId(),
      instrument: getRandomItem(instruments),
      alert_type: getRandomItem(['price', 'volume', 'technical', 'pattern', 'news']),
      message: getRandomItem(alertMessages),
      confidence_score: Math.floor(getRandomNumber(50, 100)),
      generated_at,
      sent_at,
      is_read: Math.random() > 0.5,
      market_data_snapshot: generateMarketDataSnapshots(1)[0],
      trigger_conditions: generateTriggerConditions(triggerCount)
    };
  });
}

export function generateMarketDataSnapshots(count: number): MarketDataSnapshot[] {
  const startDate = new Date('2023-01-01');
  const endDate = new Date();
  
  return generateArray(count, () => ({
    price: getRandomNumber(50, 200),
    volume: getRandomNumber(1000, 1000000),
    indicators: {
      moving_average: getRandomNumber(50, 200),
      rsi: getRandomNumber(0, 100),
      macd: getRandomNumber(-10, 10)
    }
  }));
}

export function generateTriggerConditions(count: number): TriggerCondition[] {
  return generateArray(count, () => ({
    rsi_threshold: getRandomNumber(30, 70),
    price_change: getRandomNumber(-10, 10, 2),
    volume_spike: getRandomNumber(1.5, 5, 2)
  }));
}
