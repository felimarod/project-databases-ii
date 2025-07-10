/**
 * Utilidades para generar datos aleatorios para las entidades
 */

/**
 * Genera un número aleatorio entre min y max (inclusive)
 */
export function getRandomNumber(min: number, max: number, decimals: number = 2): number {
  const random = Math.random() * (max - min) + min;
  return Number(random.toFixed(decimals));
}

/**
 * Genera una fecha aleatoria entre dos fechas
 */
export function getRandomDate(start: Date, end: Date = new Date()): Date {
  return new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime()));
}

/**
 * Genera un elemento aleatorio de un array
 */
export function getRandomItem<T>(array: T[]): T {
  return array[Math.floor(Math.random() * array.length)];
}

/**
 * Genera un conjunto aleatorio de elementos de un array
 */
export function getRandomItems<T>(array: T[], count: number): T[] {
  const shuffled = [...array].sort(() => 0.5 - Math.random());
  return shuffled.slice(0, count);
}

/**
 * Genera un ID alfanumérico aleatorio
 */
export function getRandomId(length: number = 24): string {
  const chars = 'abcdef0123456789';
  let result = '';
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

/**
 * Genera un array de n elementos llamando a un generador
 */
export function generateArray<T>(count: number, generator: () => T): T[] {
  return Array.from({ length: count }, generator);
}

// Datos comunes para reutilizar
export const instruments = [
  'EUR/USD', 'USD/JPY', 'GBP/USD', 'AUD/USD', 'USD/CAD',
  'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA',
  'BTC/USD', 'ETH/USD', 'SOL/USD', 'ADA/USD'
];

export const timeframes = ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w'];

export const sources = ['NYSE', 'NASDAQ', 'LSE', 'BINANCE', 'COINBASE', 'INTERNAL_MODEL', 'BLOOMBERG'];

export const categories = ['TECHNICAL', 'FUNDAMENTAL', 'NEWS', 'SENTIMENT', 'MARKET_STRUCTURE'];

export const priorities = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'];

export const statuses = ['OPEN', 'IN_PROGRESS', 'RESOLVED', 'CLOSED', 'PENDING'];

export const types = ['QUESTION', 'PROBLEM', 'REQUEST', 'COMPLAINT', 'FEEDBACK'];

export const departments = ['SUPPORT', 'TRADING', 'ANALYTICS', 'DEVELOPMENT', 'OPERATIONS'];

export const marketConditions = ['BULLISH', 'BEARISH', 'SIDEWAYS', 'VOLATILE', 'TRENDING', 'RANGING'];
