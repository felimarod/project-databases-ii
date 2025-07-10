from sqlalchemy import Column, String, Integer, Numeric, Boolean, ForeignKey, Text, TIMESTAMP, ARRAY, BigInteger
from sqlalchemy.dialects.postgresql import UUID, JSONB, INET
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
import uuid

from database import Base

# Definición de tipos ENUM
class AccountTypeEnum(enum.Enum):
    STANDARD = "STANDARD"
    MARGIN = "MARGIN"
    DEMO = "DEMO"
    CORPORATE = "CORPORATE"
    VIP = "VIP"

class AccountStatusEnum(enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"
    CLOSED = "CLOSED"

class AlertTypeEnum(enum.Enum):
    PRICE = "PRICE"
    TREND = "TREND"
    NEWS = "NEWS"
    TECHNICAL = "TECHNICAL"
    FUNDAMENTAL = "FUNDAMENTAL"
    SYSTEM = "SYSTEM"

class TimeframeEnum(enum.Enum):
    M1 = "M1"
    M5 = "M5"
    M15 = "M15"
    M30 = "M30"
    H1 = "H1"
    H4 = "H4"
    D1 = "D1"
    W1 = "W1"
    MN = "MN"

class PriorityEnum(enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"
    CRITICAL = "CRITICAL"

class InstrumentTypeEnum(enum.Enum):
    FOREX = "FOREX"
    STOCK = "STOCK"
    CRYPTO = "CRYPTO"
    FUTURES = "FUTURES"
    OPTIONS = "OPTIONS"
    COMMODITY = "COMMODITY"
    INDEX = "INDEX"
    BOND = "BOND"
    ETF = "ETF"

class TrendDirectionEnum(enum.Enum):
    UPWARD = "UPWARD"
    DOWNWARD = "DOWNWARD"
    SIDEWAYS = "SIDEWAYS"
    REVERSAL_UP = "REVERSAL_UP"
    REVERSAL_DOWN = "REVERSAL_DOWN"

class MarketConditionEnum(enum.Enum):
    BULL = "BULL"
    BEAR = "BEAR"
    VOLATILE = "VOLATILE"
    RANGING = "RANGING"
    TRENDING = "TRENDING"
    BREAKOUT = "BREAKOUT"
    CORRECTION = "CORRECTION"

class RiskLevelEnum(enum.Enum):
    VERY_LOW = "VERY_LOW"
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"

class ExecutionStatusEnum(enum.Enum):
    PENDING = "PENDING"
    FILLED = "FILLED"
    PARTIAL = "PARTIAL"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"

class TradeDirectionEnum(enum.Enum):
    BUY = "BUY"
    SELL = "SELL"

class TradeStatusEnum(enum.Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    CANCELLED = "CANCELLED"
    PENDING = "PENDING"

class ThemeEnum(enum.Enum):
    LIGHT = "LIGHT"
    DARK = "DARK"
    SYSTEM = "SYSTEM"

class UserTypeEnum(enum.Enum):
    REGULAR = "REGULAR"
    PREMIUM = "PREMIUM"
    ADMIN = "ADMIN"
    SUPPORT = "SUPPORT"
    ANALYST = "ANALYST"

class SubscriptionLevelEnum(enum.Enum):
    FREE = "FREE"
    BASIC = "BASIC"
    PREMIUM = "PREMIUM"
    PROFESSIONAL = "PROFESSIONAL"
    ENTERPRISE = "ENTERPRISE"

# Definición de modelos
class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    last_login = Column(TIMESTAMP(timezone=True))
    user_type = Column(String, nullable=False)
    account_status = Column(String, nullable=False)
    verification_status = Column(Boolean, nullable=False)
    profile_picture_url = Column(String(255))
    two_factor_enabled = Column(Boolean, nullable=False, default=False)
    failed_login_attempts = Column(Integer, nullable=False, default=0)
    locked_until = Column(TIMESTAMP(timezone=True))
    password_changed_at = Column(TIMESTAMP(timezone=True))
    email_verified_at = Column(TIMESTAMP(timezone=True))
    last_ip_address = Column(INET)
    timezone = Column(String(50))

    accounts = relationship("Account", back_populates="user")
    alerts = relationship("Alert", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")
    portfolios = relationship("Portfolio", back_populates="user")
    strategy_configs = relationship("StrategyConfig", foreign_keys="StrategyConfig.user_id", back_populates="user")
    subscriptions = relationship("Subscription", back_populates="user")
    trades = relationship("Trade", back_populates="user")
    user_preferences = relationship("UserPreference", back_populates="user")
    user_roles = relationship("UserRole", foreign_keys="UserRole.user_id", back_populates="user")


class Account(Base):
    __tablename__ = "accounts"

    account_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    account_number = Column(String(50), nullable=False)
    account_type = Column(String, nullable=False)
    currency_code = Column(String(3), nullable=False)
    balance = Column(Numeric(15, 2), nullable=False)
    available_balance = Column(Numeric(15, 2), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    last_updated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    status = Column(String, nullable=False)
    broker_account_id = Column(String(100))
    leverage_ratio = Column(Numeric(10, 2))
    margin_call_level = Column(Numeric(5, 2))
    stop_out_level = Column(Numeric(5, 2))
    credit_limit = Column(Numeric(15, 2))

    user = relationship("User", back_populates="accounts")
    trades = relationship("Trade", back_populates="account")


class Alert(Base):
    __tablename__ = "alerts"

    alert_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    strategy_id = Column(UUID(as_uuid=True), ForeignKey("strategies.strategy_id"))
    data_id = Column(UUID(as_uuid=True), ForeignKey("market_data.data_id"))
    instrument_id = Column(UUID(as_uuid=True), ForeignKey("financial_instruments.instrument_id"))
    alert_type = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    generated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    sent_at = Column(TIMESTAMP(timezone=True))
    is_read = Column(Boolean, nullable=False)
    confidence_score = Column(Numeric(5, 2))
    timeframe = Column(String)
    priority = Column(String, nullable=False)
    expiration_time = Column(TIMESTAMP(timezone=True))
    trigger_conditions = Column(JSONB)
    recommended_action = Column(String(100))
    risk_assessment = Column(String(500))
    market_context = Column(Text)
    delivery_channels = Column(ARRAY(String))
    delivery_status = Column(JSONB)
    delivery_attempts = Column(Integer)
    last_delivery_attempt = Column(TIMESTAMP(timezone=True))
    category = Column(String(50))
    subcategory = Column(String(50))
    sentiment = Column(String(20))
    acknowledged_at = Column(TIMESTAMP(timezone=True))
    action_taken = Column(String(100))
    outcome_notes = Column(Text)

    user = relationship("User", back_populates="alerts")
    strategy = relationship("Strategy", back_populates="alerts")
    market_data = relationship("MarketData", back_populates="alerts")
    instrument = relationship("FinancialInstrument", back_populates="alerts")


class AuditLog(Base):
    __tablename__ = "audit_log"

    audit_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    table_name = Column(String(100), nullable=False)
    operation = Column(String(10), nullable=False)
    record_id = Column(UUID(as_uuid=True), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    old_values = Column(JSONB)
    new_values = Column(JSONB)
    changed_fields = Column(ARRAY(Text))
    ip_address = Column(INET)
    user_agent = Column(Text)
    session_id = Column(String(255))
    application_name = Column(String(100))
    business_context = Column(Text)
    risk_level = Column(String(20))
    compliance_flags = Column(JSONB)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    user = relationship("User", back_populates="audit_logs")


class AutomatedJob(Base):
    __tablename__ = "automated_jobs"

    job_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_name = Column(String(100), nullable=False)
    job_description = Column(Text)
    job_function = Column(String(200), nullable=False)
    schedule_expression = Column(String(100), nullable=False)
    is_enabled = Column(Boolean, nullable=False)
    last_execution = Column(TIMESTAMP(timezone=True))
    last_status = Column(String(20))
    last_error_message = Column(Text)
    execution_count = Column(BigInteger, nullable=False)
    avg_execution_time_ms = Column(Numeric(10, 2))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())


class BacktestResult(Base):
    __tablename__ = "backtest_results"

    backtest_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id = Column(UUID(as_uuid=True), ForeignKey("strategies.strategy_id"), nullable=False)
    config_id = Column(UUID(as_uuid=True), ForeignKey("strategy_configs.config_id"), nullable=False)
    period_start = Column(TIMESTAMP(timezone=True), nullable=False)
    period_end = Column(TIMESTAMP(timezone=True), nullable=False)
    initial_capital = Column(Numeric(18, 2), nullable=False)
    final_capital = Column(Numeric(18, 2), nullable=False)
    total_profit_loss = Column(Numeric(18, 2), nullable=False)
    win_rate = Column(Numeric(5, 2), nullable=False)
    max_drawdown = Column(Numeric(5, 2), nullable=False)
    sharpe_ratio = Column(Numeric(10, 4), nullable=False)
    total_trades = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    detailed_results = Column(JSONB)
    equity_curve = Column(JSONB)
    monthly_returns = Column(JSONB)
    instruments_tested = Column(ARRAY(UUID(as_uuid=True)))
    market_conditions = Column(ARRAY(String))
    sortino_ratio = Column(Numeric(10, 4))
    calmar_ratio = Column(Numeric(10, 4))
    sterling_ratio = Column(Numeric(10, 4))
    omega_ratio = Column(Numeric(10, 4))
    kappa_ratio = Column(Numeric(10, 4))
    volatility = Column(Numeric(10, 4))
    downside_volatility = Column(Numeric(10, 4))
    var_95 = Column(Numeric(18, 2))
    var_99 = Column(Numeric(18, 2))
    expected_shortfall = Column(Numeric(18, 2))
    maximum_drawdown_duration_days = Column(Integer)
    recovery_factor = Column(Numeric(10, 4))
    winning_trades = Column(Integer)
    losing_trades = Column(Integer)
    avg_win = Column(Numeric(18, 2))
    avg_loss = Column(Numeric(18, 2))
    largest_win = Column(Numeric(18, 2))
    largest_loss = Column(Numeric(18, 2))
    profit_factor = Column(Numeric(10, 4))
    payoff_ratio = Column(Numeric(10, 4))
    total_commissions = Column(Numeric(18, 2))
    total_slippage = Column(Numeric(18, 2))
    market_impact_cost = Column(Numeric(18, 2))
    benchmark_instrument_id = Column(UUID(as_uuid=True), ForeignKey("financial_instruments.instrument_id"))
    benchmark_return = Column(Numeric(10, 4))
    excess_return = Column(Numeric(10, 4))
    tracking_error = Column(Numeric(10, 4))
    information_ratio = Column(Numeric(10, 4))
    backtest_name = Column(String(200))
    backtest_description = Column(Text)
    data_quality_score = Column(Numeric(3, 2))
    execution_time_seconds = Column(Numeric(10, 3))
    cpu_time_used = Column(Numeric(10, 3))
    memory_used_mb = Column(Integer)
    out_of_sample_performance = Column(JSONB)
    walk_forward_results = Column(JSONB)
    monte_carlo_confidence = Column(Numeric(5, 2))
    overfitting_score = Column(Numeric(5, 2))

    strategy = relationship("Strategy", back_populates="backtest_results")
    config = relationship("StrategyConfig", back_populates="backtest_results")
    benchmark_instrument = relationship("FinancialInstrument", foreign_keys=[benchmark_instrument_id])


class FinancialInstrument(Base):
    __tablename__ = "financial_instruments"

    instrument_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbol = Column(String(20), nullable=False)
    name = Column(String(100), nullable=False)
    type = Column(String, nullable=False)
    exchange = Column(String(50), nullable=False)
    currency = Column(String(10), nullable=False)
    is_active = Column(Boolean, nullable=False)
    description = Column(Text)
    sector = Column(String(100))
    country = Column(String(100))
    lot_size = Column(Numeric(18, 8))
    min_tick = Column(Numeric(18, 8))
    trading_hours = Column(JSONB)
    margin_requirements = Column(Numeric(5, 2))
    isin = Column(String(12))
    cusip = Column(String(9))
    bloomberg_symbol = Column(String(50))
    reuters_symbol = Column(String(50))
    market_cap = Column(BigInteger)
    average_volume = Column(BigInteger)
    beta = Column(Numeric(8, 4))
    dividend_yield = Column(Numeric(5, 2))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    delisted_at = Column(TIMESTAMP(timezone=True))

    alerts = relationship("Alert", back_populates="instrument")
    market_conditions = relationship("MarketCondition", back_populates="instrument")
    market_data = relationship("MarketData", back_populates="instrument")
    portfolio_holdings = relationship("PortfolioHolding", back_populates="instrument")
    strategy_performance = relationship("StrategyPerformance", back_populates="instrument")
    technical_indicators = relationship("TechnicalIndicator", back_populates="instrument")
    trades = relationship("Trade", back_populates="instrument")


class MarketCondition(Base):
    __tablename__ = "market_conditions"

    condition_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False)
    description = Column(Text)
    parameters = Column(JSONB)
    start_date = Column(TIMESTAMP(timezone=True), nullable=False)
    end_date = Column(TIMESTAMP(timezone=True))
    instrument_id = Column(UUID(as_uuid=True), ForeignKey("financial_instruments.instrument_id"), nullable=False)
    volatility_level = Column(Numeric(5, 2))
    trend_direction = Column(String)
    indicators_state = Column(JSONB)
    market_condition = Column(String, nullable=False)
    strength_score = Column(Numeric(5, 2))
    duration_hours = Column(Integer)
    detected_by = Column(String(100))
    detection_method = Column(String(100))
    confidence_score = Column(Numeric(5, 2))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    instrument = relationship("FinancialInstrument", back_populates="market_conditions")


class MarketData(Base):
    __tablename__ = "market_data"

    data_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    instrument_id = Column(UUID(as_uuid=True), ForeignKey("financial_instruments.instrument_id"), nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False)
    open_price = Column(Numeric(18, 8), nullable=False)
    high_price = Column(Numeric(18, 8), nullable=False)
    low_price = Column(Numeric(18, 8), nullable=False)
    close_price = Column(Numeric(18, 8), nullable=False)
    volume = Column(Numeric(18, 8), nullable=False)
    timeframe = Column(String, nullable=False)
    data_source = Column(String(50), nullable=False)
    adjusted_close = Column(Numeric(18, 8))
    bid = Column(Numeric(18, 8))
    ask = Column(Numeric(18, 8))
    spread = Column(Numeric(18, 8))
    vwap = Column(Numeric(18, 8))
    number_of_trades = Column(Integer)
    partition_key = Column(String(50))
    data_quality_score = Column(Numeric(3, 2))
    is_adjusted = Column(Boolean)
    has_gaps = Column(Boolean)
    ingested_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    instrument = relationship("FinancialInstrument", back_populates="market_data")
    alerts = relationship("Alert", back_populates="market_data")
    strategy_performance = relationship("StrategyPerformance", back_populates="market_data")
    technical_indicators = relationship("TechnicalIndicator", back_populates="market_data")
    trades = relationship("Trade", back_populates="market_data")


class Portfolio(Base):
    __tablename__ = "portfolios"

    portfolio_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    initial_capital = Column(Numeric(18, 2), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    is_active = Column(Boolean, nullable=False)
    currency = Column(String(3), nullable=False)
    risk_profile = Column(String, nullable=False)
    target_return = Column(Numeric(5, 2))
    max_drawdown_limit = Column(Numeric(5, 2))
    rebalancing_frequency = Column(String(20))
    parent_portfolio_id = Column(UUID(as_uuid=True), ForeignKey("portfolios.portfolio_id"))
    auto_rebalance = Column(Boolean)
    rebalance_threshold = Column(Numeric(5, 2))
    management_fee = Column(Numeric(5, 4))
    performance_fee = Column(Numeric(5, 2))
    max_position_size = Column(Numeric(5, 2))
    max_sector_allocation = Column(Numeric(5, 2))
    max_correlation_threshold = Column(Numeric(5, 2))
    investment_style = Column(String(50))
    investment_horizon = Column(String(20))
    benchmark_instrument_id = Column(UUID(as_uuid=True), ForeignKey("financial_instruments.instrument_id"))
    status = Column(String(20))
    inception_date = Column(TIMESTAMP(timezone=True))
    closure_date = Column(TIMESTAMP(timezone=True))
    updated_at = Column(TIMESTAMP(timezone=True))

    user = relationship("User", back_populates="portfolios")
    parent_portfolio = relationship("Portfolio", remote_side=[portfolio_id])
    child_portfolios = relationship("Portfolio")
    benchmark_instrument = relationship("FinancialInstrument")
    portfolio_allocations = relationship("PortfolioAllocation", back_populates="portfolio")
    portfolio_holdings = relationship("PortfolioHolding", back_populates="portfolio")
    portfolio_performance = relationship("PortfolioPerformance", back_populates="portfolio")


class PortfolioAllocation(Base):
    __tablename__ = "portfolio_allocations"

    allocation_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id = Column(UUID(as_uuid=True), ForeignKey("portfolios.portfolio_id"), nullable=False)
    strategy_id = Column(UUID(as_uuid=True), ForeignKey("strategies.strategy_id"))
    config_id = Column(UUID(as_uuid=True), ForeignKey("strategy_configs.config_id"))
    allocation_percentage = Column(Numeric(5, 2), nullable=False)
    allocation_amount = Column(Numeric(18, 2), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    is_active = Column(Boolean, nullable=False)
    notes = Column(Text)
    performance_contribution = Column(Numeric(5, 2))
    allocation_type = Column(String(20))
    min_allocation = Column(Numeric(5, 2))
    max_allocation = Column(Numeric(5, 2))
    target_volatility = Column(Numeric(5, 2))
    rebalance_tolerance = Column(Numeric(5, 2))
    last_rebalanced_at = Column(TIMESTAMP(timezone=True))
    rebalance_frequency = Column(String(20))
    inception_date = Column(TIMESTAMP(timezone=True))
    inception_value = Column(Numeric(18, 2))
    current_value = Column(Numeric(18, 2))
    unrealized_pnl = Column(Numeric(18, 2))
    realized_pnl = Column(Numeric(18, 2))

    portfolio = relationship("Portfolio", back_populates="portfolio_allocations")
    strategy = relationship("Strategy")
    config = relationship("StrategyConfig")


class PortfolioHolding(Base):
    __tablename__ = "portfolio_holdings"

    holding_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id = Column(UUID(as_uuid=True), ForeignKey("portfolios.portfolio_id"), nullable=False)
    instrument_id = Column(UUID(as_uuid=True), ForeignKey("financial_instruments.instrument_id"), nullable=False)
    strategy_id = Column(UUID(as_uuid=True), ForeignKey("strategies.strategy_id"))
    quantity = Column(Numeric(18, 8), nullable=False)
    average_cost = Column(Numeric(18, 8), nullable=False)
    current_price = Column(Numeric(18, 8), nullable=False)
    market_value = Column(Numeric(18, 2), nullable=False)
    unrealized_pnl = Column(Numeric(18, 2), nullable=False)
    unrealized_pnl_percentage = Column(Numeric(10, 4), nullable=False)
    weight_percentage = Column(Numeric(5, 2), nullable=False)
    first_purchase_date = Column(TIMESTAMP(timezone=True), nullable=False)
    last_transaction_date = Column(TIMESTAMP(timezone=True), nullable=False)
    days_held = Column(Integer)
    position_beta = Column(Numeric(8, 4))
    position_volatility = Column(Numeric(8, 4))
    var_contribution = Column(Numeric(18, 2))
    target_weight = Column(Numeric(5, 2))
    deviation_from_target = Column(Numeric(5, 2))
    rebalance_needed = Column(Boolean)
    as_of_date = Column(TIMESTAMP(timezone=True), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    portfolio = relationship("Portfolio", back_populates="portfolio_holdings")
    instrument = relationship("FinancialInstrument", back_populates="portfolio_holdings")
    strategy = relationship("Strategy")


class PortfolioPerformance(Base):
    __tablename__ = "portfolio_performance"

    performance_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    portfolio_id = Column(UUID(as_uuid=True), ForeignKey("portfolios.portfolio_id"), nullable=False)
    period_start = Column(TIMESTAMP(timezone=True), nullable=False)
    period_end = Column(TIMESTAMP(timezone=True), nullable=False)
    current_value = Column(Numeric(18, 2), nullable=False)
    profit_loss = Column(Numeric(18, 2), nullable=False)
    return_percentage = Column(Numeric(10, 4), nullable=False)
    sharpe_ratio = Column(Numeric(10, 4))
    max_drawdown = Column(Numeric(5, 2))
    volatility = Column(Numeric(10, 4))
    alpha = Column(Numeric(10, 4))
    beta = Column(Numeric(10, 4))
    calmar_ratio = Column(Numeric(10, 4))
    sortino_ratio = Column(Numeric(10, 4))
    market_correlation = Column(Numeric(5, 2))
    treynor_ratio = Column(Numeric(10, 4))
    information_ratio = Column(Numeric(10, 4))
    tracking_error = Column(Numeric(10, 4))
    up_capture_ratio = Column(Numeric(10, 4))
    down_capture_ratio = Column(Numeric(10, 4))
    win_rate = Column(Numeric(5, 2))
    profit_factor = Column(Numeric(10, 4))
    var_95 = Column(Numeric(18, 2))
    var_99 = Column(Numeric(18, 2))
    expected_shortfall = Column(Numeric(18, 2))
    realized_gains = Column(Numeric(18, 2))
    unrealized_gains = Column(Numeric(18, 2))
    dividends_received = Column(Numeric(18, 2))
    fees_paid = Column(Numeric(18, 2))
    taxes_paid = Column(Numeric(18, 2))
    period_type = Column(String(20), nullable=False)
    trading_days = Column(Integer)
    number_of_trades = Column(Integer)
    average_trade_size = Column(Numeric(18, 2))
    largest_win = Column(Numeric(18, 2))
    largest_loss = Column(Numeric(18, 2))
    benchmark_return = Column(Numeric(10, 4))
    excess_return = Column(Numeric(10, 4))
    relative_performance = Column(Numeric(10, 4))
    maximum_leverage_used = Column(Numeric(10, 2))
    average_leverage = Column(Numeric(10, 2))
    risk_adjusted_return = Column(Numeric(10, 4))
    calculated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    portfolio = relationship("Portfolio", back_populates="portfolio_performance")


class Role(Base):
    __tablename__ = "roles"

    role_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False)
    description = Column(Text)
    permissions = Column(JSONB)
    is_system_role = Column(Boolean, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    user_roles = relationship("UserRole", back_populates="role")


class Strategy(Base):
    __tablename__ = "strategies"

    strategy_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    type = Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    is_active = Column(Boolean, nullable=False)
    default_parameters = Column(JSONB)
    version = Column(String(20))
    creator = Column(String(100))
    performance_summary = Column(JSONB)
    risk_level = Column(String, nullable=False)
    parent_strategy_id = Column(UUID(as_uuid=True), ForeignKey("strategies.strategy_id"))
    category = Column(String(50))
    subcategory = Column(String(50))
    min_capital_required = Column(Numeric(15, 2))
    max_drawdown_limit = Column(Numeric(5, 2))
    recommended_timeframes = Column(ARRAY(String))
    suitable_instruments = Column(ARRAY(String))
    algorithm_type = Column(String(50))
    complexity_score = Column(Integer)
    execution_frequency = Column(String(20))
    regulatory_approval = Column(Boolean)
    compliance_notes = Column(Text)
    last_audit_date = Column(TIMESTAMP(timezone=True))
    updated_at = Column(TIMESTAMP(timezone=True))
    deprecated_at = Column(TIMESTAMP(timezone=True))

    alerts = relationship("Alert", back_populates="strategy")
    backtest_results = relationship("BacktestResult", back_populates="strategy")
    strategy_configs = relationship("StrategyConfig", back_populates="strategy")
    strategy_performance = relationship("StrategyPerformance", back_populates="strategy")
    trades = relationship("Trade", back_populates="strategy")
    parent_strategy = relationship("Strategy", remote_side=[strategy_id])
    child_strategies = relationship("Strategy")


class StrategyConfig(Base):
    __tablename__ = "strategy_configs"

    config_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    strategy_id = Column(UUID(as_uuid=True), ForeignKey("strategies.strategy_id"), nullable=False)
    parameters = Column(JSONB, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    is_active = Column(Boolean, nullable=False)
    name = Column(String(100))
    description = Column(Text)
    performance_summary = Column(JSONB)
    is_favorite = Column(Boolean)
    risk_tolerance = Column(Numeric(5, 2))
    max_position_size = Column(Numeric(18, 8))
    stop_loss_percentage = Column(Numeric(5, 2))
    take_profit_percentage = Column(Numeric(5, 2))
    is_paper_trading = Column(Boolean)
    live_trading_approved = Column(Boolean)
    live_trading_approval_date = Column(TIMESTAMP(timezone=True))
    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))

    user = relationship("User", foreign_keys=[user_id], back_populates="strategy_configs")
    strategy = relationship("Strategy", back_populates="strategy_configs")
    approver = relationship("User", foreign_keys=[approved_by])
    backtest_results = relationship("BacktestResult", back_populates="config")
    strategy_performance = relationship("StrategyPerformance", back_populates="config")
    trades = relationship("Trade", back_populates="config")


class StrategyPerformance(Base):
    __tablename__ = "strategy_performance"

    performance_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id = Column(UUID(as_uuid=True), ForeignKey("strategies.strategy_id"), nullable=False)
    config_id = Column(UUID(as_uuid=True), ForeignKey("strategy_configs.config_id"))
    data_id = Column(UUID(as_uuid=True), ForeignKey("market_data.data_id"))
    instrument_id = Column(UUID(as_uuid=True), ForeignKey("financial_instruments.instrument_id"), nullable=False)
    period_start = Column(TIMESTAMP(timezone=True), nullable=False)
    period_end = Column(TIMESTAMP(timezone=True), nullable=False)
    timeframe = Column(String, nullable=False)
    win_rate = Column(Numeric(5, 2), nullable=False)
    profit_factor = Column(Numeric(10, 4), nullable=False)
    max_drawdown = Column(Numeric(5, 2), nullable=False)
    sharpe_ratio = Column(Numeric(10, 4), nullable=False)
    total_trades = Column(Integer, nullable=False)
    winning_trades = Column(Integer, nullable=False)
    losing_trades = Column(Integer, nullable=False)
    avg_profit_loss = Column(Numeric(18, 8), nullable=False)
    avg_win = Column(Numeric(18, 8), nullable=False)
    avg_loss = Column(Numeric(18, 8), nullable=False)
    market_condition = Column(String)
    sortino_ratio = Column(Numeric(10, 4))
    calmar_ratio = Column(Numeric(10, 4))
    sterling_ratio = Column(Numeric(10, 4))
    information_ratio = Column(Numeric(10, 4))
    treynor_ratio = Column(Numeric(10, 4))
    largest_win = Column(Numeric(18, 8))
    largest_loss = Column(Numeric(18, 8))
    avg_trade_duration_hours = Column(Numeric(10, 2))
    median_trade_duration_hours = Column(Numeric(10, 2))
    consecutive_wins = Column(Integer)
    consecutive_losses = Column(Integer)
    max_consecutive_wins = Column(Integer)
    max_consecutive_losses = Column(Integer)
    value_at_risk_95 = Column(Numeric(18, 8))
    expected_shortfall = Column(Numeric(18, 8))
    maximum_adverse_excursion = Column(Numeric(18, 8))
    maximum_favorable_excursion = Column(Numeric(18, 8))
    total_return = Column(Numeric(10, 4))
    annualized_return = Column(Numeric(10, 4))
    monthly_returns = Column(JSONB)
    return_volatility = Column(Numeric(10, 4))
    downside_deviation = Column(Numeric(10, 4))
    avg_position_size = Column(Numeric(18, 8))
    max_position_size = Column(Numeric(18, 8))
    position_size_volatility = Column(Numeric(10, 4))
    kelly_criterion = Column(Numeric(5, 2))
    calculated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    calculation_version = Column(String(20))

    strategy = relationship("Strategy", back_populates="strategy_performance")
    config = relationship("StrategyConfig", back_populates="strategy_performance")
    market_data = relationship("MarketData", back_populates="strategy_performance")
    instrument = relationship("FinancialInstrument", back_populates="strategy_performance")


class Subscription(Base):
    __tablename__ = "subscriptions"

    subscription_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    subscription_level = Column(String, nullable=False)
    start_date = Column(TIMESTAMP(timezone=True), nullable=False)
    end_date = Column(TIMESTAMP(timezone=True), nullable=False)
    monthly_fee = Column(Numeric(10, 2), nullable=False)
    is_active = Column(Boolean, nullable=False)
    auto_renew = Column(Boolean, nullable=False)
    payment_method_id = Column(String(100))
    last_payment_date = Column(TIMESTAMP(timezone=True))
    next_payment_date = Column(TIMESTAMP(timezone=True))
    trial_period_days = Column(Integer)
    discount_percentage = Column(Numeric(5, 2))
    promotional_code = Column(String(50))
    billing_cycle = Column(String(20))
    grace_period_days = Column(Integer)

    user = relationship("User", back_populates="subscriptions")


class SystemHealthMetric(Base):
    __tablename__ = "system_health_metrics"

    metric_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Numeric(15, 4), nullable=False)
    metric_unit = Column(String(20), nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    component = Column(String(50), nullable=False)
    severity = Column(String(20))
    metric_metadata = Column(JSONB)
    expires_at = Column(TIMESTAMP(timezone=True))


class TechnicalIndicator(Base):
    __tablename__ = "technical_indicators"

    indicator_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    data_id = Column(UUID(as_uuid=True), ForeignKey("market_data.data_id"), nullable=False)
    instrument_id = Column(UUID(as_uuid=True), ForeignKey("financial_instruments.instrument_id"), nullable=False)
    indicator_type = Column(String(50), nullable=False)
    parameters = Column(JSONB)
    values = Column(JSONB, nullable=False)
    calculated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    timeframe = Column(String, nullable=False)
    validity_period = Column(TIMESTAMP(timezone=True))
    signal_strength = Column(Numeric(5, 2))
    partition_key = Column(String(50))
    calculation_method = Column(String(100))
    data_points_used = Column(Integer)
    confidence_level = Column(Numeric(5, 2))

    market_data = relationship("MarketData", back_populates="technical_indicators")
    instrument = relationship("FinancialInstrument", back_populates="technical_indicators")


class Trade(Base):
    __tablename__ = "trades"

    trade_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    instrument_id = Column(UUID(as_uuid=True), ForeignKey("financial_instruments.instrument_id"), nullable=False)
    data_id = Column(UUID(as_uuid=True), ForeignKey("market_data.data_id"))
    strategy_id = Column(UUID(as_uuid=True), ForeignKey("strategies.strategy_id"))
    config_id = Column(UUID(as_uuid=True), ForeignKey("strategy_configs.config_id"))
    direction = Column(String, nullable=False)
    volume = Column(Numeric(18, 8), nullable=False)
    entry_price = Column(Numeric(18, 8), nullable=False)
    exit_price = Column(Numeric(18, 8))
    stop_loss = Column(Numeric(18, 8))
    take_profit = Column(Numeric(18, 8))
    entry_time = Column(TIMESTAMP(timezone=True), nullable=False)
    exit_time = Column(TIMESTAMP(timezone=True))
    profit_loss = Column(Numeric(18, 8))
    profit_loss_percentage = Column(Numeric(10, 4))
    commission = Column(Numeric(18, 8))
    status = Column(String, nullable=False)
    notes = Column(Text)
    tags = Column(ARRAY(String))
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.account_id"), nullable=False)
    order_type = Column(String(20))
    time_in_force = Column(String(20))
    leverage_used = Column(Numeric(10, 2))
    margin_used = Column(Numeric(18, 8))
    risk_reward_ratio = Column(Numeric(10, 4))
    max_risk_amount = Column(Numeric(18, 8))
    position_size_percentage = Column(Numeric(5, 2))
    entry_reason = Column(Text)
    exit_reason = Column(Text)
    market_condition_at_entry = Column(String)
    volatility_at_entry = Column(Numeric(8, 4))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    user = relationship("User", back_populates="trades")
    instrument = relationship("FinancialInstrument", back_populates="trades")
    market_data = relationship("MarketData", back_populates="trades")
    strategy = relationship("Strategy", back_populates="trades")
    config = relationship("StrategyConfig", back_populates="trades")
    account = relationship("Account", back_populates="trades")
    trade_executions = relationship("TradeExecution", back_populates="trade")


class TradeExecution(Base):
    __tablename__ = "trade_executions"

    execution_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trade_id = Column(UUID(as_uuid=True), ForeignKey("trades.trade_id"), nullable=False)
    broker_reference = Column(String(100))
    execution_status = Column(String, nullable=False)
    execution_time = Column(TIMESTAMP(timezone=True), nullable=False)
    executed_price = Column(Numeric(18, 8), nullable=False)
    executed_volume = Column(Numeric(18, 8), nullable=False)
    execution_details = Column(JSONB)
    latency_ms = Column(Integer)
    broker_commission = Column(Numeric(18, 8))
    slippage = Column(Numeric(18, 8))
    execution_venue = Column(String(100))
    execution_algorithm = Column(String(50))
    market_impact = Column(Numeric(18, 8))
    implementation_shortfall = Column(Numeric(18, 8))
    order_route = Column(Text)
    execution_quality_score = Column(Numeric(5, 2))
    price_improvement = Column(Numeric(18, 8))
    mifid_transaction_id = Column(String(100))
    regulatory_flags = Column(JSONB)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

    trade = relationship("Trade", back_populates="trade_executions")


class UserPreference(Base):
    __tablename__ = "user_preferences"

    preference_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)
    theme = Column(String, nullable=False)
    notification_settings = Column(JSONB)
    default_timeframe = Column(String)
    default_indicators = Column(JSONB)
    ui_layout = Column(JSONB)
    alert_preferences = Column(JSONB)
    language = Column(String(10))
    currency_preference = Column(String(3))

    user = relationship("User", back_populates="user_preferences")


class UserRole(Base):
    __tablename__ = "user_roles"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), primary_key=True)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.role_id"), primary_key=True)
    assigned_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    assigned_by = Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False)

    user = relationship("User", foreign_keys=[user_id], back_populates="user_roles")
    role = relationship("Role", back_populates="user_roles")
    assigner = relationship("User", foreign_keys=[assigned_by])
