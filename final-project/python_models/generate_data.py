import os
import sys
import random
import uuid
from datetime import datetime, timedelta
from decimal import Decimal
from faker import Faker
import json
from sqlalchemy.orm import Session
import ipaddress

# Clase personalizada para codificar objetos Decimal en JSON
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)  # Convertir Decimal a float para JSON
        return super(DecimalEncoder, self).default(obj)

# Función helper para convertir Decimals en diccionarios
def decimal_to_json_serializable(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: decimal_to_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [decimal_to_json_serializable(i) for i in obj]
    else:
        return obj

# Ajustar el path para importar los módulos
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from database import engine, SessionLocal, Base
from models import (
    User, Account, Alert, AuditLog, AutomatedJob, BacktestResult,
    FinancialInstrument, MarketCondition, MarketData, Portfolio,
    PortfolioAllocation, PortfolioHolding, PortfolioPerformance,
    Role, Strategy, StrategyConfig, StrategyPerformance, Subscription,
    SystemHealthMetric, TechnicalIndicator, Trade, TradeExecution,
    UserPreference, UserRole
)

# Inicializar Faker
fake = Faker()

# Constantes
NUM_RECORDS = 100
start_date = datetime(2024, 1, 1, tzinfo=datetime.now().astimezone().tzinfo)
end_date = datetime.now().astimezone()

# Función para generar fechas aleatorias entre un rango
def random_date(start=start_date, end=end_date):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)

# Función para generar un decimal aleatorio entre un rango
def random_decimal(min_value, max_value, precision=2):
    # Asegurarnos de que estamos trabajando con valores del mismo tipo
    if isinstance(min_value, Decimal):
        min_value = float(min_value)
    if isinstance(max_value, Decimal):
        max_value = float(max_value)
    
    value = random.uniform(min_value, max_value)
    return Decimal(str(round(value, precision)))

# Función para generar datos de usuarios
def create_users(db, num_users=NUM_RECORDS):
    users = []
    user_types = ["REGULAR", "PREMIUM", "ADMIN", "SUPPORT", "ANALYST"]
    account_statuses = ["ACTIVE", "INACTIVE", "SUSPENDED", "CLOSED"]
    
    for _ in range(num_users):
        user = User(
            user_id=uuid.uuid4(),
            username=fake.user_name(),
            email=fake.email(),
            password_hash=fake.sha256(),
            full_name=fake.name(),
            created_at=random_date(),
            last_login=random_date(),
            user_type=random.choice(user_types),
            account_status=random.choice(account_statuses),
            verification_status=random.choice([True, False]),
            profile_picture_url=fake.image_url() if random.random() > 0.5 else None,
            two_factor_enabled=random.choice([True, False]),
            failed_login_attempts=random.randint(0, 5),
            locked_until=random_date() if random.random() > 0.9 else None,
            password_changed_at=random_date() if random.random() > 0.7 else None,
            email_verified_at=random_date() if random.random() > 0.3 else None,
            last_ip_address=str(ipaddress.IPv4Address(random.randint(0, 2**32 - 1))),
            timezone=random.choice(["UTC", "America/New_York", "Europe/London", "Asia/Tokyo"])
        )
        users.append(user)
    
    db.add_all(users)
    db.commit()
    print(f"Created {len(users)} users")
    return users

# Función para crear roles
def create_roles(db, num_roles=5):
    roles = []
    role_names = ["Admin", "User", "Analyst", "Support", "Manager"]
    permissions = [
        {"read": True, "write": True, "delete": True, "admin": True},
        {"read": True, "write": True, "delete": False, "admin": False},
        {"read": True, "write": True, "delete": True, "admin": False},
        {"read": True, "write": False, "delete": False, "admin": False},
        {"read": True, "write": True, "delete": False, "admin": True}
    ]
    
    for i in range(num_roles):
        role = Role(
            role_id=uuid.uuid4(),
            name=role_names[i],
            description=fake.paragraph(),
            permissions=permissions[i],
            is_system_role=i == 0,
            created_at=random_date()
        )
        roles.append(role)
    
    db.add_all(roles)
    db.commit()
    print(f"Created {len(roles)} roles")
    return roles

# Función para asignar roles a usuarios
def create_user_roles(db, users, roles):
    user_roles = []
    
    # Asegurar que cada usuario tenga al menos un rol
    for user in users:
        role = random.choice(roles)
        assigner = random.choice(users)
        
        user_role = UserRole(
            user_id=user.user_id,
            role_id=role.role_id,
            assigned_at=random_date(),
            assigned_by=assigner.user_id
        )
        user_roles.append(user_role)
    
    # Asignar roles adicionales aleatoriamente
    for _ in range(NUM_RECORDS // 2):
        user = random.choice(users)
        role = random.choice(roles)
        assigner = random.choice(users)
        
        # Evitar duplicados
        if not any(ur.user_id == user.user_id and ur.role_id == role.role_id for ur in user_roles):
            user_role = UserRole(
                user_id=user.user_id,
                role_id=role.role_id,
                assigned_at=random_date(),
                assigned_by=assigner.user_id
            )
            user_roles.append(user_role)
    
    db.add_all(user_roles)
    db.commit()
    print(f"Created {len(user_roles)} user roles")
    return user_roles

# Función para crear instrumentos financieros
def create_financial_instruments(db, num_instruments=NUM_RECORDS):
    instruments = []
    instrument_types = ["FOREX", "STOCK", "CRYPTO", "FUTURES", "OPTIONS", "COMMODITY", "INDEX", "BOND", "ETF"]
    exchanges = ["NYSE", "NASDAQ", "LSE", "TSE", "SSE", "BINANCE", "COINBASE", "KRAKEN", "BITMEX"]
    currencies = ["USD", "EUR", "JPY", "GBP", "CHF", "AUD", "CAD", "NZD", "CNY"]
    sectors = ["Technology", "Finance", "Healthcare", "Energy", "Consumer", "Industrial", "Materials", "Utilities", "Real Estate"]
    countries = ["US", "UK", "JP", "DE", "FR", "CH", "AU", "CA", "CN"]
    
    for i in range(num_instruments):
        instrument_type = random.choice(instrument_types)
        
        # Generar símbolos específicos por tipo
        if instrument_type == "FOREX":
            symbol = f"{random.choice(currencies)}/{random.choice(currencies)}"
            name = f"{symbol} Forex Pair"
        elif instrument_type == "STOCK":
            symbol = "".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(3, 5))
            name = f"{fake.company()} Inc."
        elif instrument_type == "CRYPTO":
            symbol = "".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(3, 6))
            name = f"{symbol} Coin"
        else:
            symbol = "".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for _ in range(3, 6))
            name = f"{fake.company()} {instrument_type}"
        
        instrument = FinancialInstrument(
            instrument_id=uuid.uuid4(),
            symbol=symbol,
            name=name,
            type=instrument_type,
            exchange=random.choice(exchanges),
            currency=random.choice(currencies),
            is_active=random.random() > 0.1,
            description=fake.text(),
            sector=random.choice(sectors),
            country=random.choice(countries),
            lot_size=Decimal(str(10 ** random.randint(-8, 3))),
            min_tick=Decimal(str(10 ** random.randint(-8, -2))),
            trading_hours={
                "open": "09:30",
                "close": "16:00",
                "timezone": "America/New_York"
            } if instrument_type != "CRYPTO" else {"24/7": True},
            margin_requirements=random_decimal(0.01, 0.50, 2) if instrument_type in ["FOREX", "FUTURES", "OPTIONS"] else None,
            isin="".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for _ in range(12)) if random.random() > 0.5 else None,
            cusip="".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for _ in range(9)) if random.random() > 0.5 else None,
            bloomberg_symbol=f"{symbol} {random.choice(exchanges)}" if random.random() > 0.5 else None,
            reuters_symbol=f"{symbol}.{random.choice(['O', 'N', 'L'])}" if random.random() > 0.5 else None,
            market_cap=random.randint(1000000, 1000000000000) if instrument_type == "STOCK" else None,
            average_volume=random.randint(10000, 10000000) if instrument_type in ["STOCK", "ETF"] else None,
            beta=random_decimal(0.5, 2.5, 4) if instrument_type in ["STOCK", "ETF"] else None,
            dividend_yield=random_decimal(0, 0.1, 2) if instrument_type in ["STOCK", "ETF"] else None,
            created_at=random_date(start_date, start_date + timedelta(days=30)),
            updated_at=random_date(),
            delisted_at=random_date() if random.random() > 0.95 else None
        )
        instruments.append(instrument)
    
    db.add_all(instruments)
    db.commit()
    print(f"Created {len(instruments)} financial instruments")
    return instruments

# Función para crear datos de mercado
def create_market_data(db, instruments, num_records=NUM_RECORDS*5):
    market_data_records = []
    timeframes = ["M1", "M5", "M15", "M30", "H1", "H4", "D1", "W1", "MN"]
    data_sources = ["EXCHANGE", "BROKER", "THIRD_PARTY", "CONSOLIDATED", "PROPRIETARY"]
    
    # Para cada instrumento, crear varias entradas de datos
    for instrument in instruments:
        # Determinar el precio base basado en el tipo de instrumento
        if instrument.type == "FOREX":
            base_price = random_decimal(0.5, 2, 5)
        elif instrument.type == "CRYPTO":
            base_price = random_decimal(100, 50000, 2)
        elif instrument.type == "STOCK":
            base_price = random_decimal(10, 1000, 2)
        else:
            base_price = random_decimal(50, 5000, 2)
        
        # Generar datos para diferentes timeframes
        for timeframe in random.sample(timeframes, 3):  # Seleccionar 3 timeframes aleatorios
            # Generar varias entradas para ese timeframe
            entries_per_timeframe = max(1, num_records // (len(instruments) * 3))
            
            for i in range(entries_per_timeframe):
                # Calcular timestamp basado en timeframe
                if timeframe == "M1":
                    timestamp = random_date() - timedelta(minutes=i)
                elif timeframe == "M5":
                    timestamp = random_date() - timedelta(minutes=5*i)
                elif timeframe == "M15":
                    timestamp = random_date() - timedelta(minutes=15*i)
                elif timeframe == "M30":
                    timestamp = random_date() - timedelta(minutes=30*i)
                elif timeframe == "H1":
                    timestamp = random_date() - timedelta(hours=i)
                elif timeframe == "H4":
                    timestamp = random_date() - timedelta(hours=4*i)
                elif timeframe == "D1":
                    timestamp = random_date() - timedelta(days=i)
                elif timeframe == "W1":
                    timestamp = random_date() - timedelta(weeks=i)
                else:  # MN
                    timestamp = random_date() - timedelta(days=30*i)
                
                # Añadir variación al precio base
                volatility = random_decimal(0.001, 0.05, 3)
                close_price = base_price * (1 + random_decimal(-volatility, volatility, 8))
                high_price = close_price * (1 + random_decimal(0, volatility*2, 8))
                low_price = close_price * (1 - random_decimal(0, volatility*2, 8))
                open_price = close_price * (1 + random_decimal(-volatility, volatility, 8))
                
                # Asegurar que high sea el mayor y low el menor
                if open_price > high_price:
                    open_price, high_price = high_price, open_price
                if close_price > high_price:
                    close_price, high_price = high_price, close_price
                if open_price < low_price:
                    open_price, low_price = low_price, open_price
                if close_price < low_price:
                    close_price, low_price = low_price, close_price
                
                volume = Decimal(str(random.randint(100, 1000000)))
                
                market_data = MarketData(
                    data_id=uuid.uuid4(),
                    instrument_id=instrument.instrument_id,
                    timestamp=timestamp,
                    open_price=open_price,
                    high_price=high_price,
                    low_price=low_price,
                    close_price=close_price,
                    volume=volume,
                    timeframe=timeframe,
                    data_source=random.choice(data_sources),
                    adjusted_close=close_price * (1 - random_decimal(0, 0.01, 8)) if random.random() > 0.8 else None,
                    bid=close_price * (1 - random_decimal(0, 0.0005, 8)),
                    ask=close_price * (1 + random_decimal(0, 0.0005, 8)),
                    spread=random_decimal(0.0001, 0.01, 8),
                    vwap=close_price * (1 + random_decimal(-0.001, 0.001, 8)),
                    number_of_trades=random.randint(10, 10000),
                    partition_key=f"{instrument.symbol}_{timeframe}",
                    data_quality_score=random_decimal(0.7, 1.0, 2),
                    is_adjusted=random.choice([True, False]),
                    has_gaps=random.choice([True, False]),
                    ingested_at=timestamp + timedelta(seconds=random.randint(1, 60))
                )
                market_data_records.append(market_data)
    
    db.add_all(market_data_records)
    db.commit()
    print(f"Created {len(market_data_records)} market data records")
    return market_data_records

# Función para crear cuentas
def create_accounts(db, users, num_accounts=NUM_RECORDS):
    accounts = []
    account_types = ["STANDARD", "MARGIN", "DEMO", "CORPORATE", "VIP"]
    account_statuses = ["ACTIVE", "INACTIVE", "SUSPENDED", "CLOSED"]
    currencies = ["USD", "EUR", "JPY", "GBP", "CHF", "AUD", "CAD", "NZD", "CNY"]
    
    for _ in range(num_accounts):
        user = random.choice(users)
        balance = random_decimal(1000, 100000, 2)
        
        account = Account(
            account_id=uuid.uuid4(),
            user_id=user.user_id,
            account_number=f"ACC{random.randint(100000, 999999)}",
            account_type=random.choice(account_types),
            currency_code=random.choice(currencies),
            balance=balance,
            available_balance=balance * random_decimal(0.9, 1.0, 2),
            created_at=random_date(),
            last_updated=random_date(),
            status=random.choice(account_statuses),
            broker_account_id=f"BR{random.randint(100000, 999999)}" if random.random() > 0.3 else None,
            leverage_ratio=random.choice([1, 2, 5, 10, 20, 50, 100]),
            margin_call_level=random_decimal(50, 80, 2),
            stop_out_level=random_decimal(20, 40, 2),
            credit_limit=random_decimal(0, 10000, 2) if random.random() > 0.7 else None
        )
        accounts.append(account)
    
    db.add_all(accounts)
    db.commit()
    print(f"Created {len(accounts)} accounts")
    return accounts

# Función para crear estrategias
def create_strategies(db, num_strategies=NUM_RECORDS):
    strategies = []
    strategy_types = ["TREND_FOLLOWING", "MEAN_REVERSION", "BREAKOUT", "MOMENTUM", "SCALPING", "ARBITRAGE", "GRID", "MARTINGALE", "HEDGING"]
    risk_levels = ["VERY_LOW", "LOW", "MODERATE", "HIGH", "VERY_HIGH"]
    timeframes = ["M1", "M5", "M15", "M30", "H1", "H4", "D1", "W1", "MN"]
    instrument_types = ["FOREX", "STOCK", "CRYPTO", "FUTURES", "OPTIONS", "COMMODITY", "INDEX", "BOND", "ETF"]
    algorithm_types = ["STATISTICAL", "MACHINE_LEARNING", "NEURAL_NETWORK", "RULE_BASED", "FUZZY_LOGIC", "GENETIC"]
    
    # Crear algunas estrategias para usar como padres
    parent_strategies = []
    for i in range(5):
        parent = Strategy(
            strategy_id=uuid.uuid4(),
            name=f"{fake.word().capitalize()} Strategy Base {i+1}",
            description=fake.paragraph(),
            type=random.choice(strategy_types),
            created_at=random_date(start_date, start_date + timedelta(days=30)),
            is_active=True,
            default_parameters={
                "rsi_period": random.randint(7, 21),
                "ma_fast": random.randint(5, 20),
                "ma_slow": random.randint(21, 50),
                "stop_loss_pct": random_decimal(0.5, 5.0, 2),
                "take_profit_pct": random_decimal(1.0, 10.0, 2),
                "risk_per_trade_pct": random_decimal(0.5, 2.0, 2)
            },
            version="1.0.0",
            creator=fake.name(),
            performance_summary={
                "win_rate": random_decimal(40.0, 70.0, 2),
                "profit_factor": random_decimal(1.0, 3.0, 2),
                "sharpe_ratio": random_decimal(0.5, 2.5, 2),
                "max_drawdown": random_decimal(5.0, 30.0, 2)
            },
            risk_level=random.choice(risk_levels),
            category=random.choice(["TECHNICAL", "FUNDAMENTAL", "HYBRID"]),
            subcategory=random.choice(["INTRADAY", "SWING", "POSITION", "ALGORITHMIC"]),
            min_capital_required=random_decimal(1000, 50000, 2),
            max_drawdown_limit=random_decimal(10.0, 30.0, 2),
            recommended_timeframes=random.sample(timeframes, random.randint(1, 5)),
            suitable_instruments=random.sample(instrument_types, random.randint(1, 5)),
            algorithm_type=random.choice(algorithm_types),
            complexity_score=random.randint(1, 10),
            execution_frequency=random.choice(["HIGH", "MEDIUM", "LOW"]),
            regulatory_approval=random.choice([True, False]),
            compliance_notes=fake.paragraph() if random.random() > 0.7 else None,
            last_audit_date=random_date() if random.random() > 0.5 else None,
            updated_at=random_date(),
            deprecated_at=None
        )
        parent_strategies.append(parent)
    
    db.add_all(parent_strategies)
    db.commit()
    strategies.extend(parent_strategies)
    
    # Crear el resto de las estrategias
    for i in range(num_strategies - len(parent_strategies)):
        has_parent = random.random() > 0.7
        parent_id = random.choice(parent_strategies).strategy_id if has_parent else None
        version = "1.0.0"
        if has_parent:
            version = f"1.{random.randint(1, 9)}.{random.randint(0, 9)}"
        
        strategy = Strategy(
            strategy_id=uuid.uuid4(),
            name=f"{fake.word().capitalize()} {fake.word().capitalize()} Strategy",
            description=fake.paragraph(),
            type=random.choice(strategy_types),
            created_at=random_date(),
            is_active=random.random() > 0.2,
            default_parameters={
                "rsi_period": random.randint(7, 21),
                "ma_fast": random.randint(5, 20),
                "ma_slow": random.randint(21, 50),
                "stop_loss_pct": random_decimal(0.5, 5.0, 2),
                "take_profit_pct": random_decimal(1.0, 10.0, 2),
                "risk_per_trade_pct": random_decimal(0.5, 2.0, 2)
            },
            version=version,
            creator=fake.name(),
            performance_summary={
                "win_rate": random_decimal(40.0, 70.0, 2),
                "profit_factor": random_decimal(1.0, 3.0, 2),
                "sharpe_ratio": random_decimal(0.5, 2.5, 2),
                "max_drawdown": random_decimal(5.0, 30.0, 2)
            },
            risk_level=random.choice(risk_levels),
            parent_strategy_id=parent_id,
            category=random.choice(["TECHNICAL", "FUNDAMENTAL", "HYBRID"]),
            subcategory=random.choice(["INTRADAY", "SWING", "POSITION", "ALGORITHMIC"]),
            min_capital_required=random_decimal(1000, 50000, 2),
            max_drawdown_limit=random_decimal(10.0, 30.0, 2),
            recommended_timeframes=random.sample(timeframes, random.randint(1, 5)),
            suitable_instruments=random.sample(instrument_types, random.randint(1, 5)),
            algorithm_type=random.choice(algorithm_types),
            complexity_score=random.randint(1, 10),
            execution_frequency=random.choice(["HIGH", "MEDIUM", "LOW"]),
            regulatory_approval=random.choice([True, False]),
            compliance_notes=fake.paragraph() if random.random() > 0.7 else None,
            last_audit_date=random_date() if random.random() > 0.5 else None,
            updated_at=random_date(),
            deprecated_at=random_date() if random.random() > 0.9 else None
        )
        strategies.append(strategy)
    
    db.add_all(strategies[len(parent_strategies):])
    db.commit()
    print(f"Created {len(strategies)} strategies")
    return strategies

# Función para crear configuraciones de estrategia
def create_strategy_configs(db, users, strategies, num_configs=NUM_RECORDS*2):
    strategy_configs = []
    
    for _ in range(num_configs):
        user = random.choice(users)
        strategy = random.choice(strategies)
        
        # Generar parámetros basados en los valores predeterminados con algunas variaciones
        base_params = strategy.default_parameters
        params = {}
        if base_params:
            for key, value in base_params.items():
                if isinstance(value, (int, float)):
                    # Añadir variación a los valores numéricos
                    variation = random.uniform(0.8, 1.2)
                    if isinstance(value, int):
                        params[key] = max(1, int(value * variation))
                    else:
                        params[key] = round(value * variation, 2)
                else:
                    params[key] = value
        
        # Añadir algunos parámetros adicionales
        params["enabled"] = random.choice([True, False])
        params["filter_news"] = random.choice([True, False])
        params["max_trades_per_day"] = random.randint(1, 20)
        
        # Crear configuración
        config = StrategyConfig(
            config_id=uuid.uuid4(),
            user_id=user.user_id,
            strategy_id=strategy.strategy_id,
            parameters=params,
            created_at=random_date(),
            updated_at=random_date(),
            is_active=random.random() > 0.2,
            name=f"{strategy.name} - {user.username} Config",
            description=fake.paragraph() if random.random() > 0.5 else None,
            performance_summary={
                "win_rate": random_decimal(40.0, 70.0, 2),
                "profit_factor": random_decimal(1.0, 3.0, 2),
                "sharpe_ratio": random_decimal(0.5, 2.5, 2),
                "max_drawdown": random_decimal(5.0, 30.0, 2)
            } if random.random() > 0.5 else None,
            is_favorite=random.choice([True, False]),
            risk_tolerance=random_decimal(1.0, 9.0, 2),
            max_position_size=random_decimal(0.01, 10.0, 8),
            stop_loss_percentage=random_decimal(1.0, 5.0, 2),
            take_profit_percentage=random_decimal(2.0, 10.0, 2),
            is_paper_trading=random.choice([True, False]),
            live_trading_approved=random.choice([True, False]),
            live_trading_approval_date=random_date() if random.random() > 0.7 else None,
            approved_by=random.choice(users).user_id if random.random() > 0.7 else None
        )
        strategy_configs.append(config)
    
    db.add_all(strategy_configs)
    db.commit()
    print(f"Created {len(strategy_configs)} strategy configurations")
    return strategy_configs

# Función para crear carteras
def create_portfolios(db, users, instruments, num_portfolios=NUM_RECORDS):
    portfolios = []
    risk_levels = ["VERY_LOW", "LOW", "MODERATE", "HIGH", "VERY_HIGH"]
    currencies = ["USD", "EUR", "JPY", "GBP", "CHF", "AUD", "CAD", "NZD", "CNY"]
    rebalancing_frequencies = ["DAILY", "WEEKLY", "MONTHLY", "QUARTERLY", "YEARLY"]
    investment_styles = ["CONSERVATIVE", "BALANCED", "GROWTH", "AGGRESSIVE", "INCOME"]
    investment_horizons = ["SHORT_TERM", "MEDIUM_TERM", "LONG_TERM"]
    
    # Crear primero algunas carteras principales
    parent_portfolios = []
    for i in range(10):
        user = random.choice(users)
        parent = Portfolio(
            portfolio_id=uuid.uuid4(),
            user_id=user.user_id,
            name=f"Main Portfolio {i+1}",
            description=fake.paragraph(),
            initial_capital=random_decimal(10000, 1000000, 2),
            created_at=random_date(start_date, start_date + timedelta(days=30)),
            is_active=True,
            currency=random.choice(currencies),
            risk_profile=random.choice(risk_levels),
            target_return=random_decimal(5.0, 20.0, 2),
            max_drawdown_limit=random_decimal(10.0, 30.0, 2),
            rebalancing_frequency=random.choice(rebalancing_frequencies),
            parent_portfolio_id=None,
            auto_rebalance=random.choice([True, False]),
            rebalance_threshold=random_decimal(2.0, 10.0, 2),
            management_fee=random_decimal(0.0, 2.0, 4),
            performance_fee=random_decimal(0.0, 20.0, 2),
            max_position_size=random_decimal(5.0, 20.0, 2),
            max_sector_allocation=random_decimal(20.0, 40.0, 2),
            max_correlation_threshold=random_decimal(0.5, 0.9, 2),
            investment_style=random.choice(investment_styles),
            investment_horizon=random.choice(investment_horizons),
            benchmark_instrument_id=random.choice(instruments).instrument_id,
            status="ACTIVE",
            inception_date=random_date(start_date, start_date + timedelta(days=30)),
            closure_date=None,
            updated_at=random_date()
        )
        parent_portfolios.append(parent)
    
    db.add_all(parent_portfolios)
    db.commit()
    portfolios.extend(parent_portfolios)
    
    # Crear el resto de las carteras
    for i in range(num_portfolios - len(parent_portfolios)):
        user = random.choice(users)
        has_parent = random.random() > 0.7
        parent_id = random.choice(parent_portfolios).portfolio_id if has_parent else None
        
        portfolio = Portfolio(
            portfolio_id=uuid.uuid4(),
            user_id=user.user_id,
            name=f"{fake.word().capitalize()} Portfolio",
            description=fake.paragraph(),
            initial_capital=random_decimal(1000, 100000, 2),
            created_at=random_date(),
            is_active=random.random() > 0.2,
            currency=random.choice(currencies),
            risk_profile=random.choice(risk_levels),
            target_return=random_decimal(5.0, 20.0, 2),
            max_drawdown_limit=random_decimal(10.0, 30.0, 2),
            rebalancing_frequency=random.choice(rebalancing_frequencies),
            parent_portfolio_id=parent_id,
            auto_rebalance=random.choice([True, False]),
            rebalance_threshold=random_decimal(2.0, 10.0, 2),
            management_fee=random_decimal(0.0, 2.0, 4),
            performance_fee=random_decimal(0.0, 20.0, 2),
            max_position_size=random_decimal(5.0, 20.0, 2),
            max_sector_allocation=random_decimal(20.0, 40.0, 2),
            max_correlation_threshold=random_decimal(0.5, 0.9, 2),
            investment_style=random.choice(investment_styles),
            investment_horizon=random.choice(investment_horizons),
            benchmark_instrument_id=random.choice(instruments).instrument_id,
            status=random.choice(["ACTIVE", "PENDING", "CLOSED", "ARCHIVED"]),
            inception_date=random_date(),
            closure_date=random_date() if random.random() > 0.8 else None,
            updated_at=random_date()
        )
        portfolios.append(portfolio)
    
    db.add_all(portfolios[len(parent_portfolios):])
    db.commit()
    print(f"Created {len(portfolios)} portfolios")
    return portfolios

# Función para crear operaciones
def create_trades(db, users, accounts, instruments, strategies, strategy_configs, market_data, num_trades=NUM_RECORDS*3):
    trades = []
    directions = ["BUY", "SELL"]
    statuses = ["OPEN", "CLOSED", "CANCELLED", "PENDING"]
    order_types = ["MARKET", "LIMIT", "STOP", "STOP_LIMIT"]
    time_in_force = ["GTC", "IOC", "FOK", "DAY"]
    market_conditions = ["BULL", "BEAR", "VOLATILE", "RANGING", "TRENDING", "BREAKOUT", "CORRECTION"]
    
    for _ in range(num_trades):
        user = random.choice(users)
        account = next((acc for acc in accounts if acc.user_id == user.user_id), random.choice(accounts))
        instrument = random.choice(instruments)
        strategy = random.choice(strategies) if random.random() > 0.3 else None
        
        # Solo usar configuraciones para la estrategia seleccionada, si hay una
        applicable_configs = []
        if strategy:
            applicable_configs = [cfg for cfg in strategy_configs 
                                 if cfg.strategy_id == strategy.strategy_id and cfg.user_id == user.user_id]
        config = random.choice(applicable_configs) if applicable_configs else None
        
        # Seleccionar un dato de mercado para el instrumento
        instrument_data = [md for md in market_data if md.instrument_id == instrument.instrument_id]
        data = random.choice(instrument_data) if instrument_data else None
        
        direction = random.choice(directions)
        status = random.choice(statuses)
        entry_time = random_date()
        
        # Determinar si la operación está cerrada
        is_closed = status == "CLOSED"
        exit_time = random_date(entry_time, entry_time + timedelta(days=30)) if is_closed else None
        
        # Generar precios de entrada, salida, stop loss y take profit
        base_price = float(data.close_price) if data else random_decimal(10, 1000, 2)
        entry_price = base_price
        
        if direction == "BUY":
            stop_loss = entry_price * (1 - random_decimal(0.01, 0.05, 8)) if random.random() > 0.2 else None
            take_profit = entry_price * (1 + random_decimal(0.02, 0.1, 8)) if random.random() > 0.2 else None
            
            if is_closed:
                # Para operaciones cerradas, generar un precio de salida realista
                if random.random() > 0.5:  # Ganadora
                    exit_price = entry_price * (1 + random_decimal(0.005, 0.08, 8))
                else:  # Perdedora
                    exit_price = entry_price * (1 - random_decimal(0.005, 0.04, 8))
            else:
                exit_price = None
        else:  # SELL
            stop_loss = entry_price * (1 + random_decimal(0.01, 0.05, 8)) if random.random() > 0.2 else None
            take_profit = entry_price * (1 - random_decimal(0.02, 0.1, 8)) if random.random() > 0.2 else None
            
            if is_closed:
                if random.random() > 0.5:  # Ganadora
                    exit_price = entry_price * (1 - random_decimal(0.005, 0.08, 8))
                else:  # Perdedora
                    exit_price = entry_price * (1 + random_decimal(0.005, 0.04, 8))
            else:
                exit_price = None
        
        # Calcular P&L si la operación está cerrada
        volume = random_decimal(0.01, 10.0, 8)
        commission = volume * entry_price * random_decimal(0.0001, 0.002, 8)
        
        if is_closed and exit_price:
            if direction == "BUY":
                profit_loss = (exit_price - entry_price) * volume - commission
                profit_loss_percentage = (exit_price / entry_price - 1) * 100
            else:
                profit_loss = (entry_price - exit_price) * volume - commission
                profit_loss_percentage = (entry_price / exit_price - 1) * 100
        else:
            profit_loss = None
            profit_loss_percentage = None
        
        trade = Trade(
            trade_id=uuid.uuid4(),
            user_id=user.user_id,
            instrument_id=instrument.instrument_id,
            data_id=data.data_id if data else None,
            strategy_id=strategy.strategy_id if strategy else None,
            config_id=config.config_id if config else None,
            direction=direction,
            volume=volume,
            entry_price=entry_price,
            exit_price=exit_price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            entry_time=entry_time,
            exit_time=exit_time,
            profit_loss=profit_loss,
            profit_loss_percentage=profit_loss_percentage,
            commission=commission,
            status=status,
            notes=fake.paragraph() if random.random() > 0.7 else None,
            tags=random.sample(["TREND", "BREAKOUT", "PULLBACK", "REVERSAL", "NEWS", "EARNINGS", "TECHNICAL"], 
                              random.randint(0, 3)) if random.random() > 0.5 else None,
            account_id=account.account_id,
            order_type=random.choice(order_types),
            time_in_force=random.choice(time_in_force),
            leverage_used=random.choice([1, 2, 5, 10, 20, 50, 100]) if random.random() > 0.5 else None,
            margin_used=volume * entry_price / (account.leverage_ratio if account.leverage_ratio else 1) if account.account_type == "MARGIN" else None,
            risk_reward_ratio=random_decimal(0.5, 3.0, 2) if stop_loss and take_profit else None,
            max_risk_amount=volume * abs(entry_price - stop_loss) if stop_loss else None,
            position_size_percentage=random_decimal(1.0, 10.0, 2),
            entry_reason=fake.paragraph() if random.random() > 0.5 else None,
            exit_reason=fake.paragraph() if is_closed and random.random() > 0.5 else None,
            market_condition_at_entry=random.choice(market_conditions),
            volatility_at_entry=random_decimal(0.5, 5.0, 4),
            created_at=entry_time,
            updated_at=exit_time if exit_time else entry_time
        )
        trades.append(trade)
    
    db.add_all(trades)
    db.commit()
    print(f"Created {len(trades)} trades")
    return trades

# Función para crear alertas
def create_alerts(db, users, strategies, market_data, instruments, num_alerts=NUM_RECORDS):
    alerts = []
    alert_types = ["PRICE", "TREND", "NEWS", "TECHNICAL", "FUNDAMENTAL", "SYSTEM"]
    priorities = ["LOW", "MEDIUM", "HIGH", "URGENT", "CRITICAL"]
    timeframes = ["M1", "M5", "M15", "M30", "H1", "H4", "D1", "W1", "MN"]
    
    for _ in range(num_alerts):
        user = random.choice(users)
        strategy = random.choice(strategies) if random.random() > 0.3 else None
        data = random.choice(market_data) if random.random() > 0.3 else None
        instrument = random.choice(instruments) if random.random() > 0.3 else None
        
        generated_at = random_date()
        sent_at = generated_at + timedelta(seconds=random.randint(1, 3600)) if random.random() > 0.2 else None
        is_read = random.random() > 0.5
        delivery_attempts = random.randint(1, 5) if sent_at else 0
        
        alert = Alert(
            alert_id=uuid.uuid4(),
            user_id=user.user_id,
            strategy_id=strategy.strategy_id if strategy else None,
            data_id=data.data_id if data else None,
            instrument_id=instrument.instrument_id if instrument else None,
            alert_type=random.choice(alert_types),
            message=fake.paragraph(),
            generated_at=generated_at,
            sent_at=sent_at,
            is_read=is_read,
            confidence_score=random_decimal(50, 99, 2) if random.random() > 0.3 else None,
            timeframe=random.choice(timeframes) if random.random() > 0.3 else None,
            priority=random.choice(priorities),
            expiration_time=generated_at + timedelta(days=random.randint(1, 30)) if random.random() > 0.7 else None,
            trigger_conditions={"price": str(random_decimal(10, 1000, 2)), "condition": "above"} if random.random() > 0.5 else None,
            recommended_action=fake.sentence() if random.random() > 0.6 else None,
            risk_assessment=fake.paragraph() if random.random() > 0.7 else None,
            market_context=fake.paragraph() if random.random() > 0.7 else None,
            delivery_channels=random.sample(["email", "sms", "push", "app"], random.randint(1, 4)) if random.random() > 0.5 else None,
            delivery_status={"email": "sent", "sms": "failed"} if sent_at else None,
            delivery_attempts=delivery_attempts,
            last_delivery_attempt=sent_at if delivery_attempts > 0 else None,
            category=fake.word() if random.random() > 0.5 else None,
            subcategory=fake.word() if random.random() > 0.5 else None,
            sentiment=random.choice(["positive", "neutral", "negative"]) if random.random() > 0.6 else None,
            acknowledged_at=generated_at + timedelta(hours=random.randint(1, 24)) if is_read and random.random() > 0.5 else None,
            action_taken=fake.sentence() if is_read and random.random() > 0.7 else None,
            outcome_notes=fake.paragraph() if is_read and random.random() > 0.7 else None
        )
        alerts.append(alert)
    
    db.add_all(alerts)
    db.commit()
    print(f"Created {len(alerts)} alerts")
    return alerts

# Función para crear registros de auditoría
def create_audit_logs(db, users, num_logs=NUM_RECORDS):
    audit_logs = []
    tables = ["users", "accounts", "trades", "portfolios", "strategies"]
    operations = ["INSERT", "UPDATE", "DELETE"]
    
    for _ in range(num_logs):
        user = random.choice(users)
        operation = random.choice(operations)
        table_name = random.choice(tables)
        timestamp = random_date()
        old_values = None
        new_values = None
        
        if operation == "INSERT":
            new_values = {"id": str(uuid.uuid4()), "created_at": str(timestamp)}
        elif operation == "UPDATE":
            old_values = {"value": "old_value", "updated_at": str(timestamp - timedelta(days=1))}
            new_values = {"value": "new_value", "updated_at": str(timestamp)}
        elif operation == "DELETE":
            old_values = {"id": str(uuid.uuid4()), "deleted_at": None}
            new_values = {"id": str(uuid.uuid4()), "deleted_at": str(timestamp)}
        
        audit_log = AuditLog(
            audit_id=uuid.uuid4(),
            table_name=table_name,
            operation=operation,
            record_id=uuid.uuid4(),
            user_id=user.user_id,
            timestamp=timestamp,
            old_values=old_values,
            new_values=new_values,
            changed_fields=["value", "updated_at"] if operation == "UPDATE" else None,
            ip_address=str(ipaddress.IPv4Address(random.randint(0, 2**32 - 1))),
            user_agent=f"Mozilla/5.0 {fake.user_agent()}",
            session_id=str(uuid.uuid4()),
            application_name="Trading Platform",
            business_context=fake.sentence() if random.random() > 0.7 else None,
            risk_level=random.choice(["LOW", "MEDIUM", "HIGH"]) if random.random() > 0.5 else None,
            compliance_flags={"regulatory_required": random.choice([True, False])} if random.random() > 0.7 else None,
            created_at=timestamp
        )
        audit_logs.append(audit_log)
    
    db.add_all(audit_logs)
    db.commit()
    print(f"Created {len(audit_logs)} audit logs")
    return audit_logs

# Función para crear condiciones de mercado
def create_market_conditions(db, instruments, num_conditions=NUM_RECORDS):
    market_conditions_list = []
    market_condition_types = ["BULL", "BEAR", "VOLATILE", "RANGING", "TRENDING", "BREAKOUT", "CORRECTION"]
    trend_directions = ["UPWARD", "DOWNWARD", "SIDEWAYS", "REVERSAL_UP", "REVERSAL_DOWN"]
    
    for _ in range(num_conditions):
        instrument = random.choice(instruments)
        start_date = random_date()
        end_date = start_date + timedelta(days=random.randint(1, 30)) if random.random() > 0.3 else None
        market_condition = random.choice(market_condition_types)
        trend_direction = random.choice(trend_directions) if random.random() > 0.2 else None
        
        market_condition_record = MarketCondition(
            condition_id=uuid.uuid4(),
            name=f"{market_condition} {instrument.symbol}",
            description=fake.paragraph() if random.random() > 0.5 else None,
            parameters={"threshold": random.uniform(0.1, 0.9), "window_size": random.randint(14, 200)} if random.random() > 0.5 else None,
            start_date=start_date,
            end_date=end_date,
            instrument_id=instrument.instrument_id,
            volatility_level=random_decimal(0.1, 5.0, 2) if random.random() > 0.2 else None,
            trend_direction=trend_direction,
            indicators_state={"rsi": random.randint(0, 100), "macd": random.uniform(-2, 2)} if random.random() > 0.5 else None,
            market_condition=market_condition,
            strength_score=random_decimal(50, 100, 2) if random.random() > 0.3 else None,
            duration_hours=random.randint(1, 720) if end_date else None,
            detected_by=random.choice(["algorithm", "analyst", "system"]) if random.random() > 0.5 else None,
            detection_method=random.choice(["pattern_recognition", "technical_analysis", "machine_learning"]) if random.random() > 0.5 else None,
            confidence_score=random_decimal(50, 100, 2) if random.random() > 0.3 else None,
            created_at=random_date()
        )
        market_conditions_list.append(market_condition_record)
    
    db.add_all(market_conditions_list)
    db.commit()
    print(f"Created {len(market_conditions_list)} market conditions")
    return market_conditions_list

# Función para crear asignaciones de portfolio
def create_portfolio_allocations(db, portfolios, strategies, strategy_configs, num_allocations=NUM_RECORDS*2):
    allocations = []
    allocation_types = ["CORE", "SATELLITE", "TACTICAL", "STRATEGIC"]
    
    for _ in range(num_allocations):
        portfolio = random.choice(portfolios)
        strategy = random.choice(strategies) if random.random() > 0.2 else None
        config = random.choice([c for c in strategy_configs if c.strategy_id == strategy.strategy_id]) if strategy and random.random() > 0.3 else None
        
        allocation_percentage = random_decimal(1, 100, 2)
        allocation_amount = portfolio.initial_capital * allocation_percentage / 100
        
        portfolio_allocation = PortfolioAllocation(
            allocation_id=uuid.uuid4(),
            portfolio_id=portfolio.portfolio_id,
            strategy_id=strategy.strategy_id if strategy else None,
            config_id=config.config_id if config else None,
            allocation_percentage=allocation_percentage,
            allocation_amount=allocation_amount,
            updated_at=random_date(),
            is_active=random.random() > 0.1,
            notes=fake.paragraph() if random.random() > 0.7 else None,
            performance_contribution=random_decimal(-10, 30, 2) if random.random() > 0.5 else None,
            allocation_type=random.choice(allocation_types) if random.random() > 0.3 else None,
            min_allocation=random_decimal(1, 50, 2) if random.random() > 0.5 else None,
            max_allocation=random_decimal(51, 100, 2) if random.random() > 0.5 else None,
            target_volatility=random_decimal(1, 20, 2) if random.random() > 0.5 else None,
            rebalance_tolerance=random_decimal(1, 5, 2) if random.random() > 0.5 else None,
            last_rebalanced_at=random_date() if random.random() > 0.5 else None,
            rebalance_frequency=random.choice(["DAILY", "WEEKLY", "MONTHLY", "QUARTERLY"]) if random.random() > 0.5 else None,
            inception_date=random_date(),
            inception_value=allocation_amount,
            current_value=allocation_amount * random_decimal(0.8, 1.3, 2),
            unrealized_pnl=allocation_amount * random_decimal(-0.2, 0.3, 2),
            realized_pnl=allocation_amount * random_decimal(-0.1, 0.2, 2) if random.random() > 0.5 else None
        )
        allocations.append(portfolio_allocation)
    
    db.add_all(allocations)
    db.commit()
    print(f"Created {len(allocations)} portfolio allocations")
    return allocations

# Función para crear posiciones de portfolio
def create_portfolio_holdings(db, portfolios, instruments, strategies, num_holdings=NUM_RECORDS*3):
    holdings = []
    
    for _ in range(num_holdings):
        portfolio = random.choice(portfolios)
        instrument = random.choice(instruments)
        strategy = random.choice(strategies) if random.random() > 0.3 else None
        
        quantity = random_decimal(1, 1000, 8)
        average_cost = random_decimal(10, 1000, 8)
        current_price = average_cost * random_decimal(0.7, 1.3, 8)
        market_value = quantity * current_price
        unrealized_pnl = market_value - (quantity * average_cost)
        unrealized_pnl_percentage = unrealized_pnl / (quantity * average_cost) * 100
        weight_percentage = random_decimal(1, 100, 2)
        first_purchase_date = random_date()
        last_transaction_date = first_purchase_date + timedelta(days=random.randint(1, 365))
        days_held = (datetime.now().astimezone() - first_purchase_date).days
        
        portfolio_holding = PortfolioHolding(
            holding_id=uuid.uuid4(),
            portfolio_id=portfolio.portfolio_id,
            instrument_id=instrument.instrument_id,
            strategy_id=strategy.strategy_id if strategy else None,
            quantity=quantity,
            average_cost=average_cost,
            current_price=current_price,
            market_value=market_value,
            unrealized_pnl=unrealized_pnl,
            unrealized_pnl_percentage=unrealized_pnl_percentage,
            weight_percentage=weight_percentage,
            first_purchase_date=first_purchase_date,
            last_transaction_date=last_transaction_date,
            days_held=days_held,
            position_beta=random_decimal(0.5, 1.5, 4) if random.random() > 0.5 else None,
            position_volatility=random_decimal(0.1, 5.0, 4) if random.random() > 0.5 else None,
            var_contribution=market_value * random_decimal(0.01, 0.1, 2) if random.random() > 0.5 else None,
            target_weight=random_decimal(1, 100, 2) if random.random() > 0.5 else None,
            deviation_from_target=random_decimal(-10, 10, 2) if random.random() > 0.5 else None,
            rebalance_needed=random.choice([True, False]) if random.random() > 0.5 else None,
            as_of_date=datetime.now().astimezone(),
            created_at=first_purchase_date,
            updated_at=datetime.now().astimezone()
        )
        holdings.append(portfolio_holding)
    
    db.add_all(holdings)
    db.commit()
    print(f"Created {len(holdings)} portfolio holdings")
    return holdings

# Función para crear rendimiento de portfolios
def create_portfolio_performance(db, portfolios, num_performances=NUM_RECORDS*3):
    performances = []
    period_types = ["DAILY", "WEEKLY", "MONTHLY", "QUARTERLY", "YEARLY"]
    
    for _ in range(num_performances):
        portfolio = random.choice(portfolios)
        period_type = random.choice(period_types)
        period_start = random_date()
        
        if period_type == "DAILY":
            period_end = period_start + timedelta(days=1)
        elif period_type == "WEEKLY":
            period_end = period_start + timedelta(weeks=1)
        elif period_type == "MONTHLY":
            period_end = period_start + timedelta(days=30)
        elif period_type == "QUARTERLY":
            period_end = period_start + timedelta(days=90)
        else:  # YEARLY
            period_end = period_start + timedelta(days=365)
            
        current_value = portfolio.initial_capital * random_decimal(0.8, 1.5, 2)
        profit_loss = current_value - portfolio.initial_capital
        return_percentage = (profit_loss / portfolio.initial_capital) * 100
        
        portfolio_performance = PortfolioPerformance(
            performance_id=uuid.uuid4(),
            portfolio_id=portfolio.portfolio_id,
            period_start=period_start,
            period_end=period_end,
            current_value=current_value,
            profit_loss=profit_loss,
            return_percentage=return_percentage,
            sharpe_ratio=random_decimal(-2, 4, 4) if random.random() > 0.3 else None,
            max_drawdown=random_decimal(0, 50, 2) if random.random() > 0.3 else None,
            volatility=random_decimal(0.1, 30, 4) if random.random() > 0.3 else None,
            alpha=random_decimal(-5, 5, 4) if random.random() > 0.5 else None,
            beta=random_decimal(0.5, 1.5, 4) if random.random() > 0.5 else None,
            calmar_ratio=random_decimal(-2, 4, 4) if random.random() > 0.5 else None,
            sortino_ratio=random_decimal(-2, 4, 4) if random.random() > 0.5 else None,
            market_correlation=random_decimal(-1, 1, 2) if random.random() > 0.5 else None,
            treynor_ratio=random_decimal(-2, 4, 4) if random.random() > 0.5 else None,
            information_ratio=random_decimal(-2, 4, 4) if random.random() > 0.5 else None,
            tracking_error=random_decimal(0, 10, 4) if random.random() > 0.5 else None,
            up_capture_ratio=random_decimal(0, 150, 4) if random.random() > 0.5 else None,
            down_capture_ratio=random_decimal(0, 150, 4) if random.random() > 0.5 else None,
            win_rate=random_decimal(0, 100, 2) if random.random() > 0.5 else None,
            profit_factor=random_decimal(0, 3, 4) if random.random() > 0.5 else None,
            var_95=current_value * random_decimal(0.01, 0.1, 2) if random.random() > 0.5 else None,
            var_99=current_value * random_decimal(0.03, 0.2, 2) if random.random() > 0.5 else None,
            expected_shortfall=current_value * random_decimal(0.05, 0.3, 2) if random.random() > 0.5 else None,
            realized_gains=profit_loss * random_decimal(0.5, 0.8, 2) if profit_loss > 0 else 0,
            unrealized_gains=profit_loss * random_decimal(0.2, 0.5, 2) if profit_loss > 0 else 0,
            dividends_received=current_value * random_decimal(0.01, 0.05, 2) if random.random() > 0.7 else None,
            fees_paid=current_value * random_decimal(0.001, 0.01, 2) if random.random() > 0.5 else None,
            taxes_paid=current_value * random_decimal(0.001, 0.05, 2) if random.random() > 0.7 else None,
            period_type=period_type,
            trading_days=random.randint(1, 252) if random.random() > 0.5 else None,
            number_of_trades=random.randint(0, 100) if random.random() > 0.5 else None,
            average_trade_size=random_decimal(100, 10000, 2) if random.random() > 0.5 else None,
            largest_win=random_decimal(100, 5000, 2) if random.random() > 0.5 else None,
            largest_loss=random_decimal(-5000, -100, 2) if random.random() > 0.5 else None,
            benchmark_return=random_decimal(-10, 20, 4) if random.random() > 0.5 else None,
            excess_return=return_percentage - random_decimal(-10, 20, 4) if random.random() > 0.5 else None,
            relative_performance=random_decimal(-10, 10, 4) if random.random() > 0.5 else None,
            maximum_leverage_used=random_decimal(1, 5, 2) if random.random() > 0.7 else None,
            average_leverage=random_decimal(1, 3, 2) if random.random() > 0.7 else None,
            risk_adjusted_return=return_percentage / (random_decimal(5, 20, 4) if random.random() > 0.5 else 10),
            calculated_at=datetime.now().astimezone()
        )
        performances.append(portfolio_performance)
    
    db.add_all(performances)
    db.commit()
    print(f"Created {len(performances)} portfolio performances")
    return performances

# Función para crear rendimiento de estrategias
def create_strategy_performance(db, strategies, strategy_configs, market_data, instruments, num_performances=NUM_RECORDS*2):
    performances = []
    market_conditions = ["BULL", "BEAR", "VOLATILE", "RANGING", "TRENDING", "BREAKOUT", "CORRECTION"]
    timeframes = ["M1", "M5", "M15", "M30", "H1", "H4", "D1", "W1", "MN"]
    
    for _ in range(num_performances):
        strategy = random.choice(strategies)
        config = random.choice([c for c in strategy_configs if c.strategy_id == strategy.strategy_id]) if strategy_configs else None
        data = random.choice(market_data) if random.random() > 0.5 else None
        instrument = random.choice(instruments)
        timeframe = random.choice(timeframes)
        
        period_start = random_date()
        period_end = period_start + timedelta(days=random.randint(30, 365))
        win_rate = random_decimal(20, 80, 2)
        profit_factor = random_decimal(0.5, 3.0, 4)
        max_drawdown = random_decimal(1, 40, 2)
        sharpe_ratio = random_decimal(-1, 3, 4)
        total_trades = random.randint(50, 500)
        winning_trades = int(total_trades * win_rate / 100)
        losing_trades = total_trades - winning_trades
        
        strategy_performance = StrategyPerformance(
            performance_id=uuid.uuid4(),
            strategy_id=strategy.strategy_id,
            config_id=config.config_id if config else None,
            data_id=data.data_id if data else None,
            instrument_id=instrument.instrument_id,
            period_start=period_start,
            period_end=period_end,
            timeframe=timeframe,
            win_rate=win_rate,
            profit_factor=profit_factor,
            max_drawdown=max_drawdown,
            sharpe_ratio=sharpe_ratio,
            total_trades=total_trades,
            winning_trades=winning_trades,
            losing_trades=losing_trades,
            avg_profit_loss=random_decimal(-10, 50, 8),
            avg_win=random_decimal(10, 100, 8),
            avg_loss=random_decimal(-100, -10, 8),
            market_condition=random.choice(market_conditions) if random.random() > 0.5 else None,
            sortino_ratio=random_decimal(-1, 3, 4) if random.random() > 0.5 else None,
            calmar_ratio=random_decimal(-1, 3, 4) if random.random() > 0.5 else None,
            sterling_ratio=random_decimal(-1, 3, 4) if random.random() > 0.5 else None,
            information_ratio=random_decimal(-1, 3, 4) if random.random() > 0.5 else None,
            treynor_ratio=random_decimal(-1, 3, 4) if random.random() > 0.5 else None,
            largest_win=random_decimal(100, 1000, 8) if random.random() > 0.5 else None,
            largest_loss=random_decimal(-1000, -100, 8) if random.random() > 0.5 else None,
            avg_trade_duration_hours=random_decimal(0.1, 72, 2) if random.random() > 0.5 else None,
            median_trade_duration_hours=random_decimal(0.1, 48, 2) if random.random() > 0.5 else None,
            consecutive_wins=random.randint(1, 10) if random.random() > 0.5 else None,
            consecutive_losses=random.randint(1, 10) if random.random() > 0.5 else None,
            max_consecutive_wins=random.randint(3, 15) if random.random() > 0.5 else None,
            max_consecutive_losses=random.randint(3, 15) if random.random() > 0.5 else None,
            value_at_risk_95=random_decimal(100, 1000, 8) if random.random() > 0.5 else None,
            expected_shortfall=random_decimal(150, 1500, 8) if random.random() > 0.5 else None,
            maximum_adverse_excursion=random_decimal(100, 1000, 8) if random.random() > 0.5 else None,
            maximum_favorable_excursion=random_decimal(100, 1000, 8) if random.random() > 0.5 else None,
            total_return=random_decimal(-20, 100, 4) if random.random() > 0.5 else None,
            annualized_return=random_decimal(-10, 50, 4) if random.random() > 0.5 else None,
            monthly_returns={"1": 0.02, "2": -0.01, "3": 0.03} if random.random() > 0.5 else None,  # Valores float están bien para JSON
            return_volatility=random_decimal(1, 30, 4) if random.random() > 0.5 else None,
            downside_deviation=random_decimal(1, 20, 4) if random.random() > 0.5 else None,
            avg_position_size=random_decimal(100, 10000, 8) if random.random() > 0.5 else None,
            max_position_size=random_decimal(1000, 20000, 8) if random.random() > 0.5 else None,
            position_size_volatility=random_decimal(1, 20, 4) if random.random() > 0.5 else None,
            kelly_criterion=random_decimal(0.1, 0.5, 2) if random.random() > 0.5 else None,
            calculated_at=datetime.now().astimezone(),
            calculation_version="1.0" if random.random() > 0.5 else None
        )
        performances.append(strategy_performance)
    
    db.add_all(performances)
    db.commit()
    print(f"Created {len(performances)} strategy performances")
    return performances

# Función para crear suscripciones
def create_subscriptions(db, users, num_subscriptions=NUM_RECORDS):
    subscriptions = []
    subscription_levels = ["FREE", "BASIC", "PREMIUM", "PROFESSIONAL", "ENTERPRISE"]
    billing_cycles = ["MONTHLY", "QUARTERLY", "ANNUAL"]
    
    monthly_fees = {
        "FREE": Decimal("0"),
        "BASIC": Decimal("9.99"),
        "PREMIUM": Decimal("29.99"),
        "PROFESSIONAL": Decimal("99.99"),
        "ENTERPRISE": Decimal("499.99")
    }
    
    for _ in range(num_subscriptions):
        user = random.choice(users)
        level = random.choice(subscription_levels)
        billing_cycle = random.choice(billing_cycles)
        
        start_date = random_date()
        duration_days = 30 if billing_cycle == "MONTHLY" else (90 if billing_cycle == "QUARTERLY" else 365)
        end_date = start_date + timedelta(days=duration_days)
        
        monthly_fee = monthly_fees[level]
        discount_percentage = random_decimal(0, 25, 2) if random.random() > 0.7 else None
        
        if discount_percentage:
            monthly_fee = monthly_fee * (1 - discount_percentage/100)
            
        is_active = end_date > datetime.now().astimezone()
        auto_renew = random.random() > 0.3
        
        subscription = Subscription(
            subscription_id=uuid.uuid4(),
            user_id=user.user_id,
            subscription_level=level,
            start_date=start_date,
            end_date=end_date,
            monthly_fee=monthly_fee,
            is_active=is_active,
            auto_renew=auto_renew,
            payment_method_id=f"pm_{fake.sha1()}" if monthly_fee > 0 else None,
            last_payment_date=start_date if monthly_fee > 0 else None,
            next_payment_date=end_date if monthly_fee > 0 and auto_renew else None,
            trial_period_days=random.randint(7, 30) if random.random() > 0.8 else None,
            discount_percentage=discount_percentage,
            promotional_code=f"PROMO{fake.bothify('??##')}" if discount_percentage else None,
            billing_cycle=billing_cycle,
            grace_period_days=random.randint(3, 7) if random.random() > 0.7 else None
        )
        subscriptions.append(subscription)
    
    db.add_all(subscriptions)
    db.commit()
    print(f"Created {len(subscriptions)} subscriptions")
    return subscriptions

# Función para crear métricas de salud del sistema
def create_system_health_metrics(db, num_metrics=NUM_RECORDS*3):
    metrics = []
    metric_names = ["CPU_USAGE", "MEMORY_USAGE", "DATABASE_CONNECTIONS", "API_LATENCY", "QUEUE_LENGTH", "ERROR_RATE"]
    units = ["PERCENT", "MB", "COUNT", "MS", "COUNT", "PERCENT"]
    components = ["API_SERVER", "DATABASE", "QUEUE", "CACHE", "WORKER", "WEBSOCKET"]
    severities = ["NORMAL", "WARNING", "CRITICAL"]
    
    for _ in range(num_metrics):
        metric_index = random.randint(0, len(metric_names) - 1)
        metric_name = metric_names[metric_index]
        unit = units[metric_index]
        component = random.choice(components)
        timestamp = random_date(start=datetime.now().astimezone() - timedelta(days=30), end=datetime.now().astimezone())
        
        if unit == "PERCENT":
            value = random_decimal(0, 100, 2)
        elif unit == "MB":
            value = random_decimal(100, 8192, 2)
        elif unit == "COUNT":
            value = random_decimal(0, 1000, 0)
        elif unit == "MS":
            value = random_decimal(1, 2000, 2)
        else:
            value = random_decimal(0, 100, 2)
            
        if metric_name == "CPU_USAGE":
            severity = "CRITICAL" if value > 90 else ("WARNING" if value > 70 else "NORMAL")
        elif metric_name == "MEMORY_USAGE":
            severity = "CRITICAL" if value > 7000 else ("WARNING" if value > 5000 else "NORMAL")
        elif metric_name == "API_LATENCY":
            severity = "CRITICAL" if value > 500 else ("WARNING" if value > 200 else "NORMAL")
        else:
            severity = random.choice(severities)
            
        metric = SystemHealthMetric(
            metric_id=uuid.uuid4(),
            metric_name=metric_name,
            metric_value=value,
            metric_unit=unit,
            timestamp=timestamp,
            component=component,
            severity=severity if random.random() > 0.3 else None,
            metric_metadata={"source": "monitoring", "environment": random.choice(["development", "staging", "production"])} if random.random() > 0.5 else None,
            expires_at=timestamp + timedelta(days=random.randint(30, 90)) if random.random() > 0.7 else None
        )
        metrics.append(metric)
    
    db.add_all(metrics)
    db.commit()
    print(f"Created {len(metrics)} system health metrics")
    return metrics

# Función para crear indicadores técnicos
def create_technical_indicators(db, market_data, instruments, num_indicators=NUM_RECORDS*3):
    indicators = []
    indicator_types = ["RSI", "MACD", "BOLLINGER_BANDS", "SMA", "EMA", "STOCHASTIC", "ADX", "ATR", "ICHIMOKU", "FIBONACCI"]
    timeframes = ["M1", "M5", "M15", "M30", "H1", "H4", "D1", "W1", "MN"]
    calculation_methods = ["TRADITIONAL", "SMOOTHED", "WEIGHTED", "EXPONENTIAL", "ADAPTIVE"]
    
    for _ in range(num_indicators):
        data = random.choice(market_data)
        instrument = next((i for i in instruments if i.instrument_id == data.instrument_id), random.choice(instruments))
        indicator_type = random.choice(indicator_types)
        timeframe = random.choice(timeframes)
        
        if indicator_type == "RSI":
            params = {"period": random.randint(7, 21)}
            values = {"value": random.randint(0, 100), "signal_line": random.randint(20, 80)}
        elif indicator_type == "MACD":
            params = {"fast_period": random.randint(8, 12), "slow_period": random.randint(21, 26), "signal_period": random.randint(7, 9)}
            # Convertir Decimal a float para JSON
            macd_line = float(random_decimal(-2, 2, 4))
            signal_line = float(random_decimal(-2, 2, 4))
            histogram = float(random_decimal(-1, 1, 4))
            values = {"macd_line": macd_line, "signal_line": signal_line, "histogram": histogram}
        elif indicator_type == "BOLLINGER_BANDS":
            params = {"period": random.randint(14, 30), "std_dev": float(random.choice([1.5, 2, 2.5, 3]))}
            close_price = float(data.close_price)
            values = {
                "upper_band": float(random_decimal(close_price * 1.01, close_price * 1.05, 8)),
                "middle_band": float(data.close_price),
                "lower_band": float(random_decimal(close_price * 0.95, close_price * 0.99, 8))
            }
        else:
            params = {"period": random.randint(5, 200)}
            # Convertir a float para multiplicaciones
            low_price = float(data.low_price)
            high_price = float(data.high_price)
            values = {"value": float(random_decimal(low_price * 0.9, high_price * 1.1, 8))}
            
        # Convertir todos los parámetros y valores a formatos serializables en JSON
        params = decimal_to_json_serializable(params)
        values = decimal_to_json_serializable(values)
        
        indicator = TechnicalIndicator(
            indicator_id=uuid.uuid4(),
            data_id=data.data_id,
            instrument_id=instrument.instrument_id,
            indicator_type=indicator_type,
            parameters=params,
            values=values,
            calculated_at=datetime.now().astimezone(),
            timeframe=timeframe,
            validity_period=datetime.now().astimezone() + timedelta(days=random.randint(1, 30)) if random.random() > 0.7 else None,
            signal_strength=random_decimal(0, 100, 2) if random.random() > 0.5 else None,
            partition_key=f"{instrument.symbol}_{timeframe}" if random.random() > 0.5 else None,
            calculation_method=random.choice(calculation_methods) if random.random() > 0.5 else None,
            data_points_used=random.randint(50, 1000) if random.random() > 0.5 else None,
            confidence_level=random_decimal(50, 99, 2) if random.random() > 0.5 else None
        )
        indicators.append(indicator)
    
    db.add_all(indicators)
    db.commit()
    print(f"Created {len(indicators)} technical indicators")
    return indicators

# Función para crear ejecuciones de trades
def create_trade_executions(db, trades, num_executions=NUM_RECORDS*2):
    executions = []
    execution_statuses = ["PENDING", "FILLED", "PARTIAL", "REJECTED", "CANCELLED"]
    execution_venues = ["NYSE", "NASDAQ", "LSE", "BINANCE", "COINBASE", "FTX", "INTERACTIVE_BROKERS", "TD_AMERITRADE"]
    execution_algorithms = ["TWAP", "VWAP", "DARK_POOL", "SNIPER", "ICEBERG", "POV", "IMPLEMENTATION_SHORTFALL"]
    
    for _ in range(num_executions):
        trade = random.choice(trades)
        status = random.choice(execution_statuses)
        execution_time = trade.entry_time + timedelta(milliseconds=random.randint(50, 5000))
        
        executed_price = trade.entry_price * random_decimal(0.995, 1.005, 8)
        
        # Para órdenes parcialmente ejecutadas, usar una fracción del volumen
        executed_volume = trade.volume if status != "PARTIAL" else trade.volume * random_decimal(0.1, 0.9, 8)
        
        execution = TradeExecution(
            execution_id=uuid.uuid4(),
            trade_id=trade.trade_id,
            broker_reference=f"BR-{fake.bothify('??####')}" if random.random() > 0.3 else None,
            execution_status=status,
                       execution_time=execution_time,
            executed_price=executed_price,
            executed_volume=executed_volume,
            execution_details={"order_id": str(uuid.uuid4()), "exchange_order_id": fake.bothify("EX-########")} if random.random() > 0.5 else None,
            latency_ms=random.randint(5, 500),
            broker_commission=executed_price * executed_volume * random_decimal(0.0001, 0.0025, 8) if random.random() > 0.3 else None,
            slippage=abs(executed_price - trade.entry_price) if random.random() > 0.5 else None,
            execution_venue=random.choice(execution_venues) if random.random() > 0.3 else None,
            execution_algorithm=random.choice(execution_algorithms) if random.random() > 0.7 else None,
            market_impact=executed_price * random_decimal(0.0001, 0.001, 8) if random.random() > 0.7 else None,
            implementation_shortfall=executed_price * random_decimal(0.0001, 0.002, 8) if random.random() > 0.7 else None,
            order_route=f"{random.choice(execution_venues)} via {random.choice(['SOR', 'DMA', 'SMART'])}" if random.random() > 0.7 else None,
            execution_quality_score=random_decimal(1, 5, 2) if random.random() > 0.5 else None,
            price_improvement=executed_price * random_decimal(-0.001, 0.001, 8) if random.random() > 0.7 else None,
            mifid_transaction_id=f"MIFID-{fake.bothify('########')}" if random.random() > 0.8 else None,
            regulatory_flags={"reportable": random.choice([True, False]), "post_trade_transparency": random.choice([True, False])} if random.random() > 0.8 else None,
            created_at=execution_time
        )
        executions.append(execution)
    
    db.add_all(executions)
    db.commit()
    print(f"Created {len(executions)} trade executions")
    return executions

# Función para crear preferencias de usuario
def create_user_preferences(db, users, num_preferences=NUM_RECORDS):
    preferences = []
    themes = ["LIGHT", "DARK", "SYSTEM"]
    timeframes = ["M1", "M5", "M15", "M30", "H1", "H4", "D1", "W1", "MN"]
    languages = ["es", "en", "fr", "de", "it", "pt", "ru", "zh", "ja"]
    currencies = ["USD", "EUR", "GBP", "JPY", "CHF", "CAD", "AUD", "CNY"]
    
    for _ in range(min(num_preferences, len(users))):
        user = users[_]  # Asegurar que cada usuario tenga exactamente una preferencia
        
        indicators = {
            "favorites": random.sample(["RSI", "MACD", "BOLLINGER_BANDS", "SMA", "EMA", "STOCHASTIC"], random.randint(1, 6)),
            "settings": {
                "RSI": {"period": random.randint(7, 21)},
                "MACD": {"fast_period": random.randint(8, 12), "slow_period": random.randint(21, 26), "signal_period": random.randint(7, 9)},
                "BOLLINGER_BANDS": {"period": random.randint(14, 30), "std_dev": float(random.choice([1.5, 2, 2.5, 3]))}
            }
        }
        
        notification_settings = {
            "email": random.choice([True, False]),
            "push": random.choice([True, False]),
            "sms": random.choice([True, False]),
            "trade_alerts": random.choice([True, False]),
            "market_alerts": random.choice([True, False]),
            "system_alerts": random.choice([True, False]),
            "price_alerts": random.choice([True, False]),
            "frequency": random.choice(["real_time", "hourly", "daily", "weekly"])
        }
        
        ui_layout = {
            "sidebar": random.choice(["left", "right", "hidden"]),
            "chart_style": random.choice(["candles", "bars", "line", "heikin_ashi"]),
            "default_dashboard": random.choice(["overview", "trading", "analytics", "portfolio"]),
            "widgets": random.sample(["portfolio_overview", "watchlist", "recent_trades", "market_news", "economic_calendar", "performance_chart"], random.randint(2, 6))
        }
        
        alert_preferences = {
            "minimum_priority": random.choice(["LOW", "MEDIUM", "HIGH", "URGENT", "CRITICAL"]),
            "notification_channels": random.sample(["email", "push", "sms", "in_app"], random.randint(1, 4)),
            "quiet_hours": {"start": f"{random.randint(18, 23)}:00", "end": f"{random.randint(5, 9)}:00"} if random.random() > 0.5 else None
        }
        
        # Convertir todos los diccionarios a formatos serializables JSON
        indicators = decimal_to_json_serializable(indicators)
        notification_settings = decimal_to_json_serializable(notification_settings)
        ui_layout = decimal_to_json_serializable(ui_layout)
        alert_preferences = decimal_to_json_serializable(alert_preferences)
        
        user_preference = UserPreference(
            preference_id=uuid.uuid4(),
            user_id=user.user_id,
            theme=random.choice(themes),
            notification_settings=notification_settings,
            default_timeframe=random.choice(timeframes),
            default_indicators=indicators,
            ui_layout=ui_layout,
            alert_preferences=alert_preferences,
            language=random.choice(languages),
            currency_preference=random.choice(currencies)
        )
        preferences.append(user_preference)
    
    db.add_all(preferences)
    db.commit()
    print(f"Created {len(preferences)} user preferences")
    return preferences

# Función para crear trabajos automatizados
def create_automated_jobs(db, num_jobs=20):
    jobs = []
    job_functions = ["DATA_SYNC", "MARKET_ANALYSIS", "PORTFOLIO_REBALANCE", "STRATEGY_OPTIMIZATION", 
                     "RISK_ASSESSMENT", "REPORT_GENERATION", "ALERT_PROCESSING", "SYSTEM_MAINTENANCE"]
    schedule_expressions = ["* * * * *", "*/5 * * * *", "0 * * * *", "0 0 * * *", "0 0 * * 1", "0 0 1 * *"]
    statuses = ["SUCCESS", "FAILED", "SKIPPED", "RUNNING"]
    
    for _ in range(num_jobs):
        job_name = f"{random.choice(job_functions).lower().replace('_', '-')}-job-{_+1}"
        job_function = random.choice(job_functions)
        schedule = random.choice(schedule_expressions)
        is_enabled = random.random() > 0.2
        created_at = random_date(start=start_date, end=end_date - timedelta(days=30))
        updated_at = created_at + timedelta(days=random.randint(1, 30))
        last_execution = updated_at if is_enabled else None
        last_status = random.choice(statuses) if last_execution else None
        execution_count = random.randint(0, 1000) if is_enabled else 0
        
        job = AutomatedJob(
            job_id=uuid.uuid4(),
            job_name=job_name,
            job_description=fake.paragraph() if random.random() > 0.3 else None,
            job_function=job_function,
            schedule_expression=schedule,
            is_enabled=is_enabled,
            last_execution=last_execution,
            last_status=last_status,
            last_error_message=fake.sentence() if last_status == "FAILED" and random.random() > 0.5 else None,
            execution_count=execution_count,
            avg_execution_time_ms=random_decimal(100, 10000, 2) if execution_count > 0 else None,
            created_at=created_at,
            updated_at=updated_at
        )
        jobs.append(job)
    
    db.add_all(jobs)
    db.commit()
    print(f"Created {len(jobs)} automated jobs")
    return jobs

# Función principal
def main():
    # Crear todas las tablas
    Base.metadata.drop_all(engine)  # Borrar tablas si existen
    Base.metadata.create_all(engine)
    
    # Crear sesión
    db = SessionLocal()
    
    try:
        print("Generando datos para la base de datos...")
        print("Este proceso puede tardar varios minutos...")
        
        # Crear datos en orden dependiente (respetando las relaciones de clave foránea)
        print("\n1. Creando usuarios, roles y asignaciones...")
        users = create_users(db)
        roles = create_roles(db)
        user_roles = create_user_roles(db, users, roles)
        
        print("\n2. Creando instrumentos financieros y datos de mercado...")
        instruments = create_financial_instruments(db)
        market_data_records = create_market_data(db, instruments)
        market_conditions_list = create_market_conditions(db, instruments)
        
        # Ahora creamos indicadores técnicos con serialización JSON adecuada para campos Decimal
        technical_indicators_list = create_technical_indicators(db, market_data_records, instruments)
        
        print("\n3. Creando cuentas de trading...")
        accounts = create_accounts(db, users)
        
        print("\n4. Creando estrategias y configuraciones...")
        strategies = create_strategies(db)
        strategy_configs = create_strategy_configs(db, users, strategies)
        strategy_performances = create_strategy_performance(db, strategies, strategy_configs, market_data_records, instruments)
        
        print("\n5. Creando portfolios y análisis...")
        portfolios = create_portfolios(db, users, instruments)
        portfolio_allocations = create_portfolio_allocations(db, portfolios, strategies, strategy_configs)
        portfolio_holdings = create_portfolio_holdings(db, portfolios, instruments, strategies)
        portfolio_performances = create_portfolio_performance(db, portfolios)
        
        print("\n6. Creando trades y ejecuciones...")
        trades = create_trades(db, users, accounts, instruments, strategies, strategy_configs, market_data_records)
        trade_executions = create_trade_executions(db, trades)
        
        print("\n7. Creando preferencias, suscripciones y alertas...")
        user_preferences = create_user_preferences(db, users)
        subscriptions = create_subscriptions(db, users)
        alerts = create_alerts(db, users, strategies, market_data_records, instruments)
        
        print("\n8. Creando datos del sistema...")
        audit_logs = create_audit_logs(db, users)
        system_metrics = create_system_health_metrics(db)
        automated_jobs = create_automated_jobs(db)
        
        print("\nTodos los datos han sido creados con éxito.")
        print(f"Se generaron datos para {len(users)} usuarios y {len(instruments)} instrumentos financieros.")
        print(f"El sistema contiene {len(trades)} trades y {len(portfolios)} portfolios.")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    main()
