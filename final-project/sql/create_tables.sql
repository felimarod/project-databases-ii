-- Script para crear la base de datos completa en PostgreSQL
-- Creado el 9 de julio de 2025

-- Tipos ENUM
CREATE TYPE account_type_enum AS ENUM ('STANDARD', 'MARGIN', 'DEMO', 'CORPORATE', 'VIP');
CREATE TYPE account_status_enum AS ENUM ('ACTIVE', 'INACTIVE', 'SUSPENDED', 'CLOSED');
CREATE TYPE alert_type_enum AS ENUM ('PRICE', 'TREND', 'NEWS', 'TECHNICAL', 'FUNDAMENTAL', 'SYSTEM');
CREATE TYPE timeframe_enum AS ENUM ('M1', 'M5', 'M15', 'M30', 'H1', 'H4', 'D1', 'W1', 'MN');
CREATE TYPE priority_enum AS ENUM ('LOW', 'MEDIUM', 'HIGH', 'URGENT', 'CRITICAL');
CREATE TYPE instrument_type_enum AS ENUM ('FOREX', 'STOCK', 'CRYPTO', 'FUTURES', 'OPTIONS', 'COMMODITY', 'INDEX', 'BOND', 'ETF');
CREATE TYPE trend_direction_enum AS ENUM ('UPWARD', 'DOWNWARD', 'SIDEWAYS', 'REVERSAL_UP', 'REVERSAL_DOWN');
CREATE TYPE market_condition_enum AS ENUM ('BULL', 'BEAR', 'VOLATILE', 'RANGING', 'TRENDING', 'BREAKOUT', 'CORRECTION');
CREATE TYPE risk_level_enum AS ENUM ('VERY_LOW', 'LOW', 'MODERATE', 'HIGH', 'VERY_HIGH');
CREATE TYPE execution_status_enum AS ENUM ('PENDING', 'FILLED', 'PARTIAL', 'REJECTED', 'CANCELLED');
CREATE TYPE trade_direction_enum AS ENUM ('BUY', 'SELL');
CREATE TYPE trade_status_enum AS ENUM ('OPEN', 'CLOSED', 'CANCELLED', 'PENDING');
CREATE TYPE theme_enum AS ENUM ('LIGHT', 'DARK', 'SYSTEM');
CREATE TYPE user_type_enum AS ENUM ('REGULAR', 'PREMIUM', 'ADMIN', 'SUPPORT', 'ANALYST');
CREATE TYPE subscription_level_enum AS ENUM ('FREE', 'BASIC', 'PREMIUM', 'PROFESSIONAL', 'ENTERPRISE');

-- Tabla: accounts
CREATE TABLE accounts (
    account_id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    account_number VARCHAR(50) NOT NULL,
    account_type account_type_enum NOT NULL,
    currency_code CHAR(3) NOT NULL,
    balance NUMERIC(15,2) NOT NULL,
    available_balance NUMERIC(15,2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    last_updated TIMESTAMP WITH TIME ZONE NOT NULL,
    status account_status_enum NOT NULL,
    broker_account_id VARCHAR(100),
    leverage_ratio NUMERIC(10,2),
    margin_call_level NUMERIC(5,2),
    stop_out_level NUMERIC(5,2),
    credit_limit NUMERIC(15,2)
);

-- Tabla: alerts
CREATE TABLE alerts (
    alert_id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    strategy_id UUID,
    data_id UUID,
    instrument_id UUID,
    alert_type alert_type_enum NOT NULL,
    message TEXT NOT NULL,
    generated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    sent_at TIMESTAMP WITH TIME ZONE,
    is_read BOOLEAN NOT NULL,
    confidence_score NUMERIC(5,2),
    timeframe timeframe_enum,
    priority priority_enum NOT NULL,
    expiration_time TIMESTAMP WITH TIME ZONE,
    trigger_conditions JSONB,
    recommended_action VARCHAR(100),
    risk_assessment VARCHAR(500),
    market_context TEXT,
    delivery_channels VARCHAR[],
    delivery_status JSONB,
    delivery_attempts INTEGER,
    last_delivery_attempt TIMESTAMP WITH TIME ZONE,
    category VARCHAR(50),
    subcategory VARCHAR(50),
    sentiment VARCHAR(20),
    acknowledged_at TIMESTAMP WITH TIME ZONE,
    action_taken VARCHAR(100),
    outcome_notes TEXT
);

-- Tabla: audit_log
CREATE TABLE audit_log (
    audit_id UUID PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    operation VARCHAR(10) NOT NULL,
    record_id UUID NOT NULL,
    user_id UUID NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    old_values JSONB,
    new_values JSONB,
    changed_fields TEXT[],
    ip_address INET,
    user_agent TEXT,
    session_id VARCHAR(255),
    application_name VARCHAR(100),
    business_context TEXT,
    risk_level VARCHAR(20),
    compliance_flags JSONB,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Tabla: audit_log_partitioned (tabla particionada)
CREATE TABLE audit_log_partitioned (
    audit_id UUID PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    operation VARCHAR(10) NOT NULL,
    record_id UUID NOT NULL,
    user_id UUID NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    old_values JSONB,
    new_values JSONB,
    changed_fields TEXT[],
    ip_address INET,
    user_agent TEXT,
    session_id VARCHAR(255),
    application_name VARCHAR(100),
    business_context TEXT,
    risk_level VARCHAR(20),
    compliance_flags JSONB,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL
) PARTITION BY RANGE (created_at);

-- Tabla: automated_jobs
CREATE TABLE automated_jobs (
    job_id UUID PRIMARY KEY,
    job_name VARCHAR(100) NOT NULL,
    job_description TEXT,
    job_function VARCHAR(200) NOT NULL,
    schedule_expression VARCHAR(100) NOT NULL,
    is_enabled BOOLEAN NOT NULL,
    last_execution TIMESTAMP WITH TIME ZONE,
    last_status VARCHAR(20),
    last_error_message TEXT,
    execution_count BIGINT NOT NULL,
    avg_execution_time_ms NUMERIC(10,2),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Tabla: backtest_results
CREATE TABLE backtest_results (
    backtest_id UUID PRIMARY KEY,
    strategy_id UUID NOT NULL,
    config_id UUID NOT NULL,
    period_start TIMESTAMP WITH TIME ZONE NOT NULL,
    period_end TIMESTAMP WITH TIME ZONE NOT NULL,
    initial_capital NUMERIC(18,2) NOT NULL,
    final_capital NUMERIC(18,2) NOT NULL,
    total_profit_loss NUMERIC(18,2) NOT NULL,
    win_rate NUMERIC(5,2) NOT NULL,
    max_drawdown NUMERIC(5,2) NOT NULL,
    sharpe_ratio NUMERIC(10,4) NOT NULL,
    total_trades INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    detailed_results JSONB,
    equity_curve JSONB,
    monthly_returns JSONB,
    instruments_tested UUID[],
    market_conditions VARCHAR[],
    sortino_ratio NUMERIC(10,4),
    calmar_ratio NUMERIC(10,4),
    sterling_ratio NUMERIC(10,4),
    omega_ratio NUMERIC(10,4),
    kappa_ratio NUMERIC(10,4),
    volatility NUMERIC(10,4),
    downside_volatility NUMERIC(10,4),
    var_95 NUMERIC(18,2),
    var_99 NUMERIC(18,2),
    expected_shortfall NUMERIC(18,2),
    maximum_drawdown_duration_days INTEGER,
    recovery_factor NUMERIC(10,4),
    winning_trades INTEGER,
    losing_trades INTEGER,
    avg_win NUMERIC(18,2),
    avg_loss NUMERIC(18,2),
    largest_win NUMERIC(18,2),
    largest_loss NUMERIC(18,2),
    profit_factor NUMERIC(10,4),
    payoff_ratio NUMERIC(10,4),
    total_commissions NUMERIC(18,2),
    total_slippage NUMERIC(18,2),
    market_impact_cost NUMERIC(18,2),
    benchmark_instrument_id UUID,
    benchmark_return NUMERIC(10,4),
    excess_return NUMERIC(10,4),
    tracking_error NUMERIC(10,4),
    information_ratio NUMERIC(10,4),
    backtest_name VARCHAR(200),
    backtest_description TEXT,
    data_quality_score NUMERIC(3,2),
    execution_time_seconds NUMERIC(10,3),
    cpu_time_used NUMERIC(10,3),
    memory_used_mb INTEGER,
    out_of_sample_performance JSONB,
    walk_forward_results JSONB,
    monte_carlo_confidence NUMERIC(5,2),
    overfitting_score NUMERIC(5,2)
);

-- Tabla: financial_instruments
CREATE TABLE financial_instruments (
    instrument_id UUID PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    name VARCHAR(100) NOT NULL,
    type instrument_type_enum NOT NULL,
    exchange VARCHAR(50) NOT NULL,
    currency VARCHAR(10) NOT NULL,
    is_active BOOLEAN NOT NULL,
    description TEXT,
    sector VARCHAR(100),
    country VARCHAR(100),
    lot_size NUMERIC(18,8),
    min_tick NUMERIC(18,8),
    trading_hours JSONB,
    margin_requirements NUMERIC(5,2),
    isin VARCHAR(12),
    cusip VARCHAR(9),
    bloomberg_symbol VARCHAR(50),
    reuters_symbol VARCHAR(50),
    market_cap BIGINT,
    average_volume BIGINT,
    beta NUMERIC(8,4),
    dividend_yield NUMERIC(5,2),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    delisted_at TIMESTAMP WITH TIME ZONE
);

-- Tabla: market_conditions
CREATE TABLE market_conditions (
    condition_id UUID PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    parameters JSONB,
    start_date TIMESTAMP WITH TIME ZONE NOT NULL,
    end_date TIMESTAMP WITH TIME ZONE,
    instrument_id UUID NOT NULL,
    volatility_level NUMERIC(5,2),
    trend_direction trend_direction_enum,
    indicators_state JSONB,
    market_condition market_condition_enum NOT NULL,
    strength_score NUMERIC(5,2),
    duration_hours INTEGER,
    detected_by VARCHAR(100),
    detection_method VARCHAR(100),
    confidence_score NUMERIC(5,2),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Tabla: market_data
CREATE TABLE market_data (
    data_id UUID PRIMARY KEY,
    instrument_id UUID NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    open_price NUMERIC(18,8) NOT NULL,
    high_price NUMERIC(18,8) NOT NULL,
    low_price NUMERIC(18,8) NOT NULL,
    close_price NUMERIC(18,8) NOT NULL,
    volume NUMERIC(18,8) NOT NULL,
    timeframe timeframe_enum NOT NULL,
    data_source VARCHAR(50) NOT NULL,
    adjusted_close NUMERIC(18,8),
    bid NUMERIC(18,8),
    ask NUMERIC(18,8),
    spread NUMERIC(18,8),
    vwap NUMERIC(18,8),
    number_of_trades INTEGER,
    partition_key VARCHAR(50),
    data_quality_score NUMERIC(3,2),
    is_adjusted BOOLEAN,
    has_gaps BOOLEAN,
    ingested_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Tabla: portfolio_allocations
CREATE TABLE portfolio_allocations (
    allocation_id UUID PRIMARY KEY,
    portfolio_id UUID NOT NULL,
    strategy_id UUID,
    config_id UUID,
    allocation_percentage NUMERIC(5,2) NOT NULL,
    allocation_amount NUMERIC(18,2) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_active BOOLEAN NOT NULL,
    notes TEXT,
    performance_contribution NUMERIC(5,2),
    allocation_type VARCHAR(20),
    min_allocation NUMERIC(5,2),
    max_allocation NUMERIC(5,2),
    target_volatility NUMERIC(5,2),
    rebalance_tolerance NUMERIC(5,2),
    last_rebalanced_at TIMESTAMP WITH TIME ZONE,
    rebalance_frequency VARCHAR(20),
    inception_date TIMESTAMP WITH TIME ZONE,
    inception_value NUMERIC(18,2),
    current_value NUMERIC(18,2),
    unrealized_pnl NUMERIC(18,2),
    realized_pnl NUMERIC(18,2)
);

-- Tabla: portfolio_holdings
CREATE TABLE portfolio_holdings (
    holding_id UUID PRIMARY KEY,
    portfolio_id UUID NOT NULL,
    instrument_id UUID NOT NULL,
    strategy_id UUID,
    quantity NUMERIC(18,8) NOT NULL,
    average_cost NUMERIC(18,8) NOT NULL,
    current_price NUMERIC(18,8) NOT NULL,
    market_value NUMERIC(18,2) NOT NULL,
    unrealized_pnl NUMERIC(18,2) NOT NULL,
    unrealized_pnl_percentage NUMERIC(10,4) NOT NULL,
    weight_percentage NUMERIC(5,2) NOT NULL,
    first_purchase_date TIMESTAMP WITH TIME ZONE NOT NULL,
    last_transaction_date TIMESTAMP WITH TIME ZONE NOT NULL,
    days_held INTEGER,
    position_beta NUMERIC(8,4),
    position_volatility NUMERIC(8,4),
    var_contribution NUMERIC(18,2),
    target_weight NUMERIC(5,2),
    deviation_from_target NUMERIC(5,2),
    rebalance_needed BOOLEAN,
    as_of_date TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Tabla: portfolio_performance
CREATE TABLE portfolio_performance (
    performance_id UUID PRIMARY KEY,
    portfolio_id UUID NOT NULL,
    period_start TIMESTAMP WITH TIME ZONE NOT NULL,
    period_end TIMESTAMP WITH TIME ZONE NOT NULL,
    current_value NUMERIC(18,2) NOT NULL,
    profit_loss NUMERIC(18,2) NOT NULL,
    return_percentage NUMERIC(10,4) NOT NULL,
    sharpe_ratio NUMERIC(10,4),
    max_drawdown NUMERIC(5,2),
    volatility NUMERIC(10,4),
    alpha NUMERIC(10,4),
    beta NUMERIC(10,4),
    calmar_ratio NUMERIC(10,4),
    sortino_ratio NUMERIC(10,4),
    market_correlation NUMERIC(5,2),
    treynor_ratio NUMERIC(10,4),
    information_ratio NUMERIC(10,4),
    tracking_error NUMERIC(10,4),
    up_capture_ratio NUMERIC(10,4),
    down_capture_ratio NUMERIC(10,4),
    win_rate NUMERIC(5,2),
    profit_factor NUMERIC(10,4),
    var_95 NUMERIC(18,2),
    var_99 NUMERIC(18,2),
    expected_shortfall NUMERIC(18,2),
    realized_gains NUMERIC(18,2),
    unrealized_gains NUMERIC(18,2),
    dividends_received NUMERIC(18,2),
    fees_paid NUMERIC(18,2),
    taxes_paid NUMERIC(18,2),
    period_type VARCHAR(20) NOT NULL,
    trading_days INTEGER,
    number_of_trades INTEGER,
    average_trade_size NUMERIC(18,2),
    largest_win NUMERIC(18,2),
    largest_loss NUMERIC(18,2),
    benchmark_return NUMERIC(10,4),
    excess_return NUMERIC(10,4),
    relative_performance NUMERIC(10,4),
    maximum_leverage_used NUMERIC(10,2),
    average_leverage NUMERIC(10,2),
    risk_adjusted_return NUMERIC(10,4),
    calculated_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Tabla: portfolios
CREATE TABLE portfolios (
    portfolio_id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    initial_capital NUMERIC(18,2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_active BOOLEAN NOT NULL,
    currency CHAR(3) NOT NULL,
    risk_profile risk_level_enum NOT NULL,
    target_return NUMERIC(5,2),
    max_drawdown_limit NUMERIC(5,2),
    rebalancing_frequency VARCHAR(20),
    parent_portfolio_id UUID,
    auto_rebalance BOOLEAN,
    rebalance_threshold NUMERIC(5,2),
    management_fee NUMERIC(5,4),
    performance_fee NUMERIC(5,2),
    max_position_size NUMERIC(5,2),
    max_sector_allocation NUMERIC(5,2),
    max_correlation_threshold NUMERIC(5,2),
    investment_style VARCHAR(50),
    investment_horizon VARCHAR(20),
    benchmark_instrument_id UUID,
    status VARCHAR(20),
    inception_date TIMESTAMP WITH TIME ZONE,
    closure_date TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Tabla: roles
CREATE TABLE roles (
    role_id UUID PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    permissions JSONB,
    is_system_role BOOLEAN NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Tabla: strategies
CREATE TABLE strategies (
    strategy_id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    type VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_active BOOLEAN NOT NULL,
    default_parameters JSONB,
    version VARCHAR(20),
    creator VARCHAR(100),
    performance_summary JSONB,
    risk_level risk_level_enum NOT NULL,
    parent_strategy_id UUID,
    category VARCHAR(50),
    subcategory VARCHAR(50),
    min_capital_required NUMERIC(15,2),
    max_drawdown_limit NUMERIC(5,2),
    recommended_timeframes timeframe_enum[],
    suitable_instruments instrument_type_enum[],
    algorithm_type VARCHAR(50),
    complexity_score INTEGER,
    execution_frequency VARCHAR(20),
    regulatory_approval BOOLEAN,
    compliance_notes TEXT,
    last_audit_date TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE,
    deprecated_at TIMESTAMP WITH TIME ZONE
);

-- Tabla: strategy_configs
CREATE TABLE strategy_configs (
    config_id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    strategy_id UUID NOT NULL,
    parameters JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_active BOOLEAN NOT NULL,
    name VARCHAR(100),
    description TEXT,
    performance_summary JSONB,
    is_favorite BOOLEAN,
    risk_tolerance NUMERIC(5,2),
    max_position_size NUMERIC(18,8),
    stop_loss_percentage NUMERIC(5,2),
    take_profit_percentage NUMERIC(5,2),
    is_paper_trading BOOLEAN,
    live_trading_approved BOOLEAN,
    live_trading_approval_date TIMESTAMP WITH TIME ZONE,
    approved_by UUID
);

-- Tabla: strategy_performance
CREATE TABLE strategy_performance (
    performance_id UUID PRIMARY KEY,
    strategy_id UUID NOT NULL,
    config_id UUID,
    data_id UUID,
    instrument_id UUID NOT NULL,
    period_start TIMESTAMP WITH TIME ZONE NOT NULL,
    period_end TIMESTAMP WITH TIME ZONE NOT NULL,
    timeframe timeframe_enum NOT NULL,
    win_rate NUMERIC(5,2) NOT NULL,
    profit_factor NUMERIC(10,4) NOT NULL,
    max_drawdown NUMERIC(5,2) NOT NULL,
    sharpe_ratio NUMERIC(10,4) NOT NULL,
    total_trades INTEGER NOT NULL,
    winning_trades INTEGER NOT NULL,
    losing_trades INTEGER NOT NULL,
    avg_profit_loss NUMERIC(18,8) NOT NULL,
    avg_win NUMERIC(18,8) NOT NULL,
    avg_loss NUMERIC(18,8) NOT NULL,
    market_condition market_condition_enum,
    sortino_ratio NUMERIC(10,4),
    calmar_ratio NUMERIC(10,4),
    sterling_ratio NUMERIC(10,4),
    information_ratio NUMERIC(10,4),
    treynor_ratio NUMERIC(10,4),
    largest_win NUMERIC(18,8),
    largest_loss NUMERIC(18,8),
    avg_trade_duration_hours NUMERIC(10,2),
    median_trade_duration_hours NUMERIC(10,2),
    consecutive_wins INTEGER,
    consecutive_losses INTEGER,
    max_consecutive_wins INTEGER,
    max_consecutive_losses INTEGER,
    value_at_risk_95 NUMERIC(18,8),
    expected_shortfall NUMERIC(18,8),
    maximum_adverse_excursion NUMERIC(18,8),
    maximum_favorable_excursion NUMERIC(18,8),
    total_return NUMERIC(10,4),
    annualized_return NUMERIC(10,4),
    monthly_returns JSONB,
    return_volatility NUMERIC(10,4),
    downside_deviation NUMERIC(10,4),
    avg_position_size NUMERIC(18,8),
    max_position_size NUMERIC(18,8),
    position_size_volatility NUMERIC(10,4),
    kelly_criterion NUMERIC(5,2),
    calculated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    calculation_version VARCHAR(20)
);

-- Tabla: subscriptions
CREATE TABLE subscriptions (
    subscription_id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    subscription_level subscription_level_enum NOT NULL,
    start_date TIMESTAMP WITH TIME ZONE NOT NULL,
    end_date TIMESTAMP WITH TIME ZONE NOT NULL,
    monthly_fee NUMERIC(10,2) NOT NULL,
    is_active BOOLEAN NOT NULL,
    auto_renew BOOLEAN NOT NULL,
    payment_method_id VARCHAR(100),
    last_payment_date TIMESTAMP WITH TIME ZONE,
    next_payment_date TIMESTAMP WITH TIME ZONE,
    trial_period_days INTEGER,
    discount_percentage NUMERIC(5,2),
    promotional_code VARCHAR(50),
    billing_cycle VARCHAR(20),
    grace_period_days INTEGER
);

-- Tabla: system_health_metrics
CREATE TABLE system_health_metrics (
    metric_id UUID PRIMARY KEY,
    metric_name VARCHAR(100) NOT NULL,
    metric_value NUMERIC(15,4) NOT NULL,
    metric_unit VARCHAR(20) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    component VARCHAR(50) NOT NULL,
    severity VARCHAR(20),
    metadata JSONB,
    expires_at TIMESTAMP WITH TIME ZONE
);

-- Tabla: technical_indicators
CREATE TABLE technical_indicators (
    indicator_id UUID PRIMARY KEY,
    data_id UUID NOT NULL,
    instrument_id UUID NOT NULL,
    indicator_type VARCHAR(50) NOT NULL,
    parameters JSONB,
    values JSONB NOT NULL,
    calculated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    timeframe timeframe_enum NOT NULL,
    validity_period TIMESTAMP WITH TIME ZONE,
    signal_strength NUMERIC(5,2),
    partition_key VARCHAR(50),
    calculation_method VARCHAR(100),
    data_points_used INTEGER,
    confidence_level NUMERIC(5,2)
);

-- Tabla: trade_executions
CREATE TABLE trade_executions (
    execution_id UUID PRIMARY KEY,
    trade_id UUID NOT NULL,
    broker_reference VARCHAR(100),
    execution_status execution_status_enum NOT NULL,
    execution_time TIMESTAMP WITH TIME ZONE NOT NULL,
    executed_price NUMERIC(18,8) NOT NULL,
    executed_volume NUMERIC(18,8) NOT NULL,
    execution_details JSONB,
    latency_ms INTEGER,
    broker_commission NUMERIC(18,8),
    slippage NUMERIC(18,8),
    execution_venue VARCHAR(100),
    execution_algorithm VARCHAR(50),
    market_impact NUMERIC(18,8),
    implementation_shortfall NUMERIC(18,8),
    order_route TEXT,
    execution_quality_score NUMERIC(5,2),
    price_improvement NUMERIC(18,8),
    mifid_transaction_id VARCHAR(100),
    regulatory_flags JSONB,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Tabla: trades
CREATE TABLE trades (
    trade_id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    instrument_id UUID NOT NULL,
    data_id UUID,
    strategy_id UUID,
    config_id UUID,
    direction trade_direction_enum NOT NULL,
    volume NUMERIC(18,8) NOT NULL,
    entry_price NUMERIC(18,8) NOT NULL,
    exit_price NUMERIC(18,8),
    stop_loss NUMERIC(18,8),
    take_profit NUMERIC(18,8),
    entry_time TIMESTAMP WITH TIME ZONE NOT NULL,
    exit_time TIMESTAMP WITH TIME ZONE,
    profit_loss NUMERIC(18,8),
    profit_loss_percentage NUMERIC(10,4),
    commission NUMERIC(18,8),
    status trade_status_enum NOT NULL,
    notes TEXT,
    tags VARCHAR[],
    account_id UUID NOT NULL,
    order_type VARCHAR(20),
    time_in_force VARCHAR(20),
    leverage_used NUMERIC(10,2),
    margin_used NUMERIC(18,8),
    risk_reward_ratio NUMERIC(10,4),
    max_risk_amount NUMERIC(18,8),
    position_size_percentage NUMERIC(5,2),
    entry_reason TEXT,
    exit_reason TEXT,
    market_condition_at_entry market_condition_enum,
    volatility_at_entry NUMERIC(8,4),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Tabla: user_preferences
CREATE TABLE user_preferences (
    preference_id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    theme theme_enum NOT NULL,
    notification_settings JSONB,
    default_timeframe timeframe_enum,
    default_indicators JSONB,
    ui_layout JSONB,
    alert_preferences JSONB,
    language VARCHAR(10),
    currency_preference CHAR(3)
);

-- Tabla: user_roles
CREATE TABLE user_roles (
    user_id UUID NOT NULL,
    role_id UUID NOT NULL,
    assigned_at TIMESTAMP WITH TIME ZONE NOT NULL,
    assigned_by UUID NOT NULL,
    PRIMARY KEY (user_id, role_id)
);

-- Tabla: users
CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE,
    user_type user_type_enum NOT NULL,
    account_status account_status_enum NOT NULL,
    verification_status BOOLEAN NOT NULL,
    profile_picture_url VARCHAR(255),
    two_factor_enabled BOOLEAN NOT NULL DEFAULT false,
    failed_login_attempts INTEGER NOT NULL DEFAULT 0,
    locked_until TIMESTAMP WITH TIME ZONE,
    password_changed_at TIMESTAMP WITH TIME ZONE,
    email_verified_at TIMESTAMP WITH TIME ZONE,
    last_ip_address INET,
    timezone VARCHAR(50)
);

-- Restricciones de clave foránea
ALTER TABLE accounts ADD CONSTRAINT fk_accounts_user_id FOREIGN KEY (user_id) REFERENCES users (user_id);

ALTER TABLE alerts 
    ADD CONSTRAINT fk_alerts_user_id FOREIGN KEY (user_id) REFERENCES users (user_id),
    ADD CONSTRAINT fk_alerts_strategy_id FOREIGN KEY (strategy_id) REFERENCES strategies (strategy_id),
    ADD CONSTRAINT fk_alerts_data_id FOREIGN KEY (data_id) REFERENCES market_data (data_id),
    ADD CONSTRAINT fk_alerts_instrument_id FOREIGN KEY (instrument_id) REFERENCES financial_instruments (instrument_id);

ALTER TABLE audit_log ADD CONSTRAINT fk_audit_log_user_id FOREIGN KEY (user_id) REFERENCES users (user_id);

ALTER TABLE backtest_results
    ADD CONSTRAINT fk_backtest_results_strategy_id FOREIGN KEY (strategy_id) REFERENCES strategies (strategy_id),
    ADD CONSTRAINT fk_backtest_results_config_id FOREIGN KEY (config_id) REFERENCES strategy_configs (config_id),
    ADD CONSTRAINT fk_backtest_results_benchmark_id FOREIGN KEY (benchmark_instrument_id) REFERENCES financial_instruments (instrument_id);

ALTER TABLE market_conditions ADD CONSTRAINT fk_market_conditions_instrument_id FOREIGN KEY (instrument_id) REFERENCES financial_instruments (instrument_id);

ALTER TABLE market_data ADD CONSTRAINT fk_market_data_instrument_id FOREIGN KEY (instrument_id) REFERENCES financial_instruments (instrument_id);

ALTER TABLE portfolio_allocations
    ADD CONSTRAINT fk_portfolio_allocations_portfolio_id FOREIGN KEY (portfolio_id) REFERENCES portfolios (portfolio_id),
    ADD CONSTRAINT fk_portfolio_allocations_strategy_id FOREIGN KEY (strategy_id) REFERENCES strategies (strategy_id),
    ADD CONSTRAINT fk_portfolio_allocations_config_id FOREIGN KEY (config_id) REFERENCES strategy_configs (config_id);

ALTER TABLE portfolio_holdings
    ADD CONSTRAINT fk_portfolio_holdings_portfolio_id FOREIGN KEY (portfolio_id) REFERENCES portfolios (portfolio_id),
    ADD CONSTRAINT fk_portfolio_holdings_instrument_id FOREIGN KEY (instrument_id) REFERENCES financial_instruments (instrument_id),
    ADD CONSTRAINT fk_portfolio_holdings_strategy_id FOREIGN KEY (strategy_id) REFERENCES strategies (strategy_id);

ALTER TABLE portfolio_performance ADD CONSTRAINT fk_portfolio_performance_portfolio_id FOREIGN KEY (portfolio_id) REFERENCES portfolios (portfolio_id);

ALTER TABLE portfolios
    ADD CONSTRAINT fk_portfolios_user_id FOREIGN KEY (user_id) REFERENCES users (user_id),
    ADD CONSTRAINT fk_portfolios_parent_id FOREIGN KEY (parent_portfolio_id) REFERENCES portfolios (portfolio_id),
    ADD CONSTRAINT fk_portfolios_benchmark_id FOREIGN KEY (benchmark_instrument_id) REFERENCES financial_instruments (instrument_id);

ALTER TABLE strategies ADD CONSTRAINT fk_strategies_parent_id FOREIGN KEY (parent_strategy_id) REFERENCES strategies (strategy_id);

ALTER TABLE strategy_configs
    ADD CONSTRAINT fk_strategy_configs_user_id FOREIGN KEY (user_id) REFERENCES users (user_id),
    ADD CONSTRAINT fk_strategy_configs_strategy_id FOREIGN KEY (strategy_id) REFERENCES strategies (strategy_id),
    ADD CONSTRAINT fk_strategy_configs_approved_by FOREIGN KEY (approved_by) REFERENCES users (user_id);

ALTER TABLE strategy_performance
    ADD CONSTRAINT fk_strategy_performance_strategy_id FOREIGN KEY (strategy_id) REFERENCES strategies (strategy_id),
    ADD CONSTRAINT fk_strategy_performance_config_id FOREIGN KEY (config_id) REFERENCES strategy_configs (config_id),
    ADD CONSTRAINT fk_strategy_performance_data_id FOREIGN KEY (data_id) REFERENCES market_data (data_id),
    ADD CONSTRAINT fk_strategy_performance_instrument_id FOREIGN KEY (instrument_id) REFERENCES financial_instruments (instrument_id);

ALTER TABLE subscriptions ADD CONSTRAINT fk_subscriptions_user_id FOREIGN KEY (user_id) REFERENCES users (user_id);

ALTER TABLE technical_indicators
    ADD CONSTRAINT fk_technical_indicators_data_id FOREIGN KEY (data_id) REFERENCES market_data (data_id),
    ADD CONSTRAINT fk_technical_indicators_instrument_id FOREIGN KEY (instrument_id) REFERENCES financial_instruments (instrument_id);

ALTER TABLE trade_executions ADD CONSTRAINT fk_trade_executions_trade_id FOREIGN KEY (trade_id) REFERENCES trades (trade_id);

ALTER TABLE trades
    ADD CONSTRAINT fk_trades_user_id FOREIGN KEY (user_id) REFERENCES users (user_id),
    ADD CONSTRAINT fk_trades_instrument_id FOREIGN KEY (instrument_id) REFERENCES financial_instruments (instrument_id),
    ADD CONSTRAINT fk_trades_data_id FOREIGN KEY (data_id) REFERENCES market_data (data_id),
    ADD CONSTRAINT fk_trades_strategy_id FOREIGN KEY (strategy_id) REFERENCES strategies (strategy_id),
    ADD CONSTRAINT fk_trades_config_id FOREIGN KEY (config_id) REFERENCES strategy_configs (config_id),
    ADD CONSTRAINT fk_trades_account_id FOREIGN KEY (account_id) REFERENCES accounts (account_id);

ALTER TABLE user_preferences ADD CONSTRAINT fk_user_preferences_user_id FOREIGN KEY (user_id) REFERENCES users (user_id);

ALTER TABLE user_roles
    ADD CONSTRAINT fk_user_roles_user_id FOREIGN KEY (user_id) REFERENCES users (user_id),
    ADD CONSTRAINT fk_user_roles_role_id FOREIGN KEY (role_id) REFERENCES roles (role_id),
    ADD CONSTRAINT fk_user_roles_assigned_by FOREIGN KEY (assigned_by) REFERENCES users (user_id);

-- Índices
CREATE INDEX idx_accounts_user_id ON accounts (user_id);
CREATE INDEX idx_alerts_user_id ON alerts (user_id);
CREATE INDEX idx_alerts_strategy_id ON alerts (strategy_id);
CREATE INDEX idx_alerts_instrument_id ON alerts (instrument_id);
CREATE INDEX idx_audit_log_user_id ON audit_log (user_id);
CREATE INDEX idx_audit_log_table_name ON audit_log (table_name);
CREATE INDEX idx_audit_log_timestamp ON audit_log (timestamp);
CREATE INDEX idx_backtest_results_strategy_id ON backtest_results (strategy_id);
CREATE INDEX idx_backtest_results_config_id ON backtest_results (config_id);
CREATE INDEX idx_market_data_instrument_id ON market_data (instrument_id);
CREATE INDEX idx_market_data_timestamp ON market_data (timestamp);
CREATE INDEX idx_market_data_timeframe ON market_data (timeframe);
CREATE INDEX idx_portfolio_allocations_portfolio_id ON portfolio_allocations (portfolio_id);
CREATE INDEX idx_portfolio_allocations_strategy_id ON portfolio_allocations (strategy_id);
CREATE INDEX idx_portfolio_holdings_portfolio_id ON portfolio_holdings (portfolio_id);
CREATE INDEX idx_portfolio_holdings_instrument_id ON portfolio_holdings (instrument_id);
CREATE INDEX idx_portfolio_performance_portfolio_id ON portfolio_performance (portfolio_id);
CREATE INDEX idx_portfolio_performance_period_start ON portfolio_performance (period_start);
CREATE INDEX idx_portfolio_performance_period_end ON portfolio_performance (period_end);
CREATE INDEX idx_portfolios_user_id ON portfolios (user_id);
CREATE INDEX idx_strategy_configs_user_id ON strategy_configs (user_id);
CREATE INDEX idx_strategy_configs_strategy_id ON strategy_configs (strategy_id);
CREATE INDEX idx_strategy_performance_strategy_id ON strategy_performance (strategy_id);
CREATE INDEX idx_strategy_performance_instrument_id ON strategy_performance (instrument_id);
CREATE INDEX idx_strategy_performance_timeframe ON strategy_performance (timeframe);
CREATE INDEX idx_subscriptions_user_id ON subscriptions (user_id);
CREATE INDEX idx_technical_indicators_instrument_id ON technical_indicators (instrument_id);
CREATE INDEX idx_technical_indicators_timeframe ON technical_indicators (timeframe);
CREATE INDEX idx_trades_user_id ON trades (user_id);
CREATE INDEX idx_trades_instrument_id ON trades (instrument_id);
CREATE INDEX idx_trades_strategy_id ON trades (strategy_id);
CREATE INDEX idx_trades_account_id ON trades (account_id);
CREATE INDEX idx_trades_entry_time ON trades (entry_time);
CREATE INDEX idx_user_preferences_user_id ON user_preferences (user_id);
CREATE INDEX idx_users_username ON users (username);
CREATE INDEX idx_users_email ON users (email);

-- Comentarios en tablas
COMMENT ON TABLE accounts IS 'Almacena la información de las cuentas de trading de los usuarios';
COMMENT ON TABLE alerts IS 'Almacena las alertas de mercado y notificaciones para los usuarios';
COMMENT ON TABLE audit_log IS 'Registro de auditoría para cambios en datos sensibles';
COMMENT ON TABLE audit_log_partitioned IS 'Versión particionada del registro de auditoría para mejor rendimiento';
COMMENT ON TABLE automated_jobs IS 'Registro y configuración de tareas automatizadas del sistema';
COMMENT ON TABLE backtest_results IS 'Resultados detallados de backtest de estrategias';
COMMENT ON TABLE financial_instruments IS 'Catálogo de instrumentos financieros disponibles para trading';
COMMENT ON TABLE market_conditions IS 'Clasificación de las condiciones de mercado detectadas';
COMMENT ON TABLE market_data IS 'Datos históricos de precios y volumen para instrumentos financieros';
COMMENT ON TABLE portfolio_allocations IS 'Asignaciones de capital a estrategias dentro de carteras';
COMMENT ON TABLE portfolio_holdings IS 'Posiciones actuales en instrumentos dentro de carteras';
COMMENT ON TABLE portfolio_performance IS 'Métricas de rendimiento para carteras en diferentes periodos';
COMMENT ON TABLE portfolios IS 'Carteras de inversión de los usuarios';
COMMENT ON TABLE roles IS 'Roles disponibles en el sistema con sus permisos';
COMMENT ON TABLE strategies IS 'Catálogo de estrategias de trading disponibles';
COMMENT ON TABLE strategy_configs IS 'Configuraciones personalizadas de estrategias por usuario';
COMMENT ON TABLE strategy_performance IS 'Métricas de rendimiento para estrategias';
COMMENT ON TABLE subscriptions IS 'Suscripciones de usuarios a planes de servicio';
COMMENT ON TABLE system_health_metrics IS 'Métricas de salud del sistema y sus componentes';
COMMENT ON TABLE technical_indicators IS 'Valores calculados de indicadores técnicos para instrumentos';
COMMENT ON TABLE trade_executions IS 'Detalles de ejecución de órdenes de trading';
COMMENT ON TABLE trades IS 'Registro de operaciones de trading realizadas';
COMMENT ON TABLE user_preferences IS 'Preferencias de interfaz y configuración para usuarios';
COMMENT ON TABLE user_roles IS 'Asignación de roles a usuarios';
COMMENT ON TABLE users IS 'Usuarios registrados en el sistema';

-- Trigger para actualizar last_updated en accounts
CREATE OR REPLACE FUNCTION update_account_last_updated()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_updated = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trig_update_account_last_updated
BEFORE UPDATE ON accounts
FOR EACH ROW
EXECUTE FUNCTION update_account_last_updated();

-- Trigger para audit_log
CREATE OR REPLACE FUNCTION process_audit_log()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log_partitioned
        SELECT * FROM audit_log
        WHERE audit_id = NEW.audit_id;
        
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trig_process_audit_log
AFTER INSERT ON audit_log
FOR EACH ROW
EXECUTE FUNCTION process_audit_log();

-- Particionamiento para audit_log_partitioned
CREATE TABLE audit_log_partitioned_current_month PARTITION OF audit_log_partitioned
    FOR VALUES FROM (CURRENT_DATE - INTERVAL '30 days') TO (CURRENT_DATE + INTERVAL '30 days');

CREATE TABLE audit_log_partitioned_previous_month PARTITION OF audit_log_partitioned
    FOR VALUES FROM (CURRENT_DATE - INTERVAL '60 days') TO (CURRENT_DATE - INTERVAL '30 days');

CREATE TABLE audit_log_partitioned_old PARTITION OF audit_log_partitioned
    FOR VALUES FROM (TIMESTAMP '-infinity') TO (CURRENT_DATE - INTERVAL '60 days');

CREATE TABLE audit_log_partitioned_future PARTITION OF audit_log_partitioned
    FOR VALUES FROM (CURRENT_DATE + INTERVAL '30 days') TO (TIMESTAMP 'infinity');
