accounts:
account_id, uuid
user_id, uuid
account_number, character varying(50)
account_type, account_type_enum
currency_code, character(3)
balance, numeric(15,2)
available_balance, numeric(15,2)
created_at, timestamp with time zone
last_updated, timestamp with time zone
status, account_status_enum
broker_account_id, character varying(100)
leverage_ratio, numeric(10,2)
margin_call_level, numeric(5,2)
stop_out_level, numeric(5,2)
credit_limit, numeric(15,2)

alerts:
alert_id, uuid
user_id, uuid
strategy_id, uuid
data_id, uuid
instrument_id, uuid
alert_type, alert_type_enum
message, text
generated_at, timestamp with time zone
sent_at, timestamp with time zone
is_read, boolean
confidence_score, numeric(5,2)
timeframe, timeframe_enum
priority, priority_enum
expiration_time, timestamp with time zone
trigger_conditions, jsonb
recommended_action, character varying(100)
risk_assessment, character varying(500)
market_context, text
delivery_channels, character varying[]
delivery_status, jsonb
delivery_attempts, integer
last_delivery_attempt, timestamp with time zone
category, character varying(50)
subcategory, character varying(50)
sentiment, character varying(20)
acknowledged_at, timestamp with time zone
action_taken, character varying(100)
outcome_notes, text

audit_log:
audit_id, uuid
table_name, character varying(100)
operation, character varying(10)
record_id, uuid
user_id, uuid
timestamp, timestamp with time zone
old_values, jsonb
new_values, jsonb
changed_fields, text[]
ip_address, inet
user_agent, text
session_id, character varying(255)
application_name, character varying(100)
business_context, text
risk_level, character varying(20)
compliance_flags, jsonb
created_at, timestamp with time zone

audit_log_partitioned:
audit_id, uuid
table_name, character varying(100)
operation, character varying(10)
record_id, uuid
user_id, uuid
timestamp, timestamp with time zone
old_values, jsonb
new_values, jsonb
changed_fields, text[]
ip_address, inet
user_agent, text
session_id, character varying(255)
application_name, character varying(100)
business_context, text
risk_level, character varying(20)
compliance_flags, jsonb
created_at, timestamp with time zone

automated_jobs:
job_id, uuid
job_name, character varying(100)
job_description, text
job_function, character varying(200)
schedule_expression, character varying(100)
is_enabled, boolean
last_execution, timestamp with time zone
last_status, character varying(20)
last_error_message, text
execution_count, bigint
avg_execution_time_ms, numeric(10,2)
created_at, timestamp with time zone
updated_at, timestamp with time zone

backtest_results:
backtest_id, uuid
strategy_id, uuid
config_id, uuid
period_start, timestamp with time zone
period_end, timestamp with time zone
initial_capital, numeric(18,2)
final_capital, numeric(18,2)
total_profit_loss, numeric(18,2)
win_rate, numeric(5,2)
max_drawdown, numeric(5,2)
sharpe_ratio, numeric(10,4)
total_trades, integer
created_at, timestamp with time zone
detailed_results, jsonb
equity_curve, jsonb
monthly_returns, jsonb
instruments_tested, uuid[]
market_conditions, character varying[]
sortino_ratio, numeric(10,4)
calmar_ratio, numeric(10,4)
sterling_ratio, numeric(10,4)
omega_ratio, numeric(10,4)
kappa_ratio, numeric(10,4)
volatility, numeric(10,4)
downside_volatility, numeric(10,4)
var_95, numeric(18,2)
var_99, numeric(18,2)
expected_shortfall, numeric(18,2)
maximum_drawdown_duration_days, integer
recovery_factor, numeric(10,4)
winning_trades, integer
losing_trades, integer
avg_win, numeric(18,2)
avg_loss, numeric(18,2)
largest_win, numeric(18,2)
largest_loss, numeric(18,2)
profit_factor, numeric(10,4)
payoff_ratio, numeric(10,4)
total_commissions, numeric(18,2)
total_slippage, numeric(18,2)
market_impact_cost, numeric(18,2)
benchmark_instrument_id, uuid
benchmark_return, numeric(10,4)
excess_return, numeric(10,4)
tracking_error, numeric(10,4)
information_ratio, numeric(10,4)
backtest_name, character varying(200)
backtest_description, text
data_quality_score, numeric(3,2)
execution_time_seconds, numeric(10,3)
cpu_time_used, numeric(10,3)
memory_used_mb, integer
out_of_sample_performance, jsonb
walk_forward_results, jsonb
monte_carlo_confidence, numeric(5,2)
overfitting_score, numeric(5,2)

financial_instruments:
instrument_id, uuid
symbol, character varying(20)
name, character varying(100)
type, instrument_type_enum
exchange, character varying(50)
currency, character varying(10)
is_active, boolean
description, text
sector, character varying(100)
country, character varying(100)
lot_size, numeric(18,8)
min_tick, numeric(18,8)
trading_hours, jsonb
margin_requirements, numeric(5,2)
isin, character varying(12)
cusip, character varying(9)
bloomberg_symbol, character varying(50)
reuters_symbol, character varying(50)
market_cap, bigint
average_volume, bigint
beta, numeric(8,4)
dividend_yield, numeric(5,2)
created_at, timestamp with time zone
updated_at, timestamp with time zone
delisted_at, timestamp with time zone

market_conditions:
condition_id, uuid
name, character varying(50)
description, text
parameters, jsonb
start_date, timestamp with time zone
end_date, timestamp with time zone
instrument_id, uuid
volatility_level, numeric(5,2)
trend_direction, trend_direction_enum
indicators_state, jsonb
market_condition, market_condition_enum
strength_score, numeric(5,2)
duration_hours, integer
detected_by, character varying(100)
detection_method, character varying(100)
confidence_score, numeric(5,2)
created_at, timestamp with time zone

market_data:
data_id, uuid
instrument_id, uuid
timestamp, timestamp with time zone
open_price, numeric(18,8)
high_price, numeric(18,8)
low_price, numeric(18,8)
close_price, numeric(18,8)
volume, numeric(18,8)
timeframe, timeframe_enum
data_source, character varying(50)
adjusted_close, numeric(18,8)
bid, numeric(18,8)
ask, numeric(18,8)
spread, numeric(18,8)
vwap, numeric(18,8)
number_of_trades, integer
partition_key, character varying(50)
data_quality_score, numeric(3,2)
is_adjusted, boolean
has_gaps, boolean
ingested_at, timestamp with time zone

portfolio_allocations:
allocation_id, uuid
portfolio_id, uuid
strategy_id, uuid
config_id, uuid
allocation_percentage, numeric(5,2)
allocation_amount, numeric(18,2)
updated_at, timestamp with time zone
is_active, boolean
notes, text
performance_contribution, numeric(5,2)
allocation_type, character varying(20)
min_allocation, numeric(5,2)
max_allocation, numeric(5,2)
target_volatility, numeric(5,2)
rebalance_tolerance, numeric(5,2)
last_rebalanced_at, timestamp with time zone
rebalance_frequency, character varying(20)
inception_date, timestamp with time zone
inception_value, numeric(18,2)
current_value, numeric(18,2)
unrealized_pnl, numeric(18,2)
realized_pnl, numeric(18,2)

portfolio_holdings:
holding_id, uuid
portfolio_id, uuid
instrument_id, uuid
strategy_id, uuid
quantity, numeric(18,8)
average_cost, numeric(18,8)
current_price, numeric(18,8)
market_value, numeric(18,2)
unrealized_pnl, numeric(18,2)
unrealized_pnl_percentage, numeric(10,4)
weight_percentage, numeric(5,2)
first_purchase_date, timestamp with time zone
last_transaction_date, timestamp with time zone
days_held, integer
position_beta, numeric(8,4)
position_volatility, numeric(8,4)
var_contribution, numeric(18,2)
target_weight, numeric(5,2)
deviation_from_target, numeric(5,2)
rebalance_needed, boolean
as_of_date, timestamp with time zone
created_at, timestamp with time zone
updated_at, timestamp with time zone

portfolio_performance:
performance_id, uuid
portfolio_id, uuid
period_start, timestamp with time zone
period_end, timestamp with time zone
current_value, numeric(18,2)
profit_loss, numeric(18,2)
return_percentage, numeric(10,4)
sharpe_ratio, numeric(10,4)
max_drawdown, numeric(5,2)
volatility, numeric(10,4)
alpha, numeric(10,4)
beta, numeric(10,4)
calmar_ratio, numeric(10,4)
sortino_ratio, numeric(10,4)
market_correlation, numeric(5,2)
treynor_ratio, numeric(10,4)
information_ratio, numeric(10,4)
tracking_error, numeric(10,4)
up_capture_ratio, numeric(10,4)
down_capture_ratio, numeric(10,4)
win_rate, numeric(5,2)
profit_factor, numeric(10,4)
var_95, numeric(18,2)
var_99, numeric(18,2)
expected_shortfall, numeric(18,2)
realized_gains, numeric(18,2)
unrealized_gains, numeric(18,2)
dividends_received, numeric(18,2)
fees_paid, numeric(18,2)
taxes_paid, numeric(18,2)
period_type, character varying(20)
trading_days, integer
number_of_trades, integer
average_trade_size, numeric(18,2)
largest_win, numeric(18,2)
largest_loss, numeric(18,2)
benchmark_return, numeric(10,4)
excess_return, numeric(10,4)
relative_performance, numeric(10,4)
maximum_leverage_used, numeric(10,2)
average_leverage, numeric(10,2)
risk_adjusted_return, numeric(10,4)
calculated_at, timestamp with time zone

portfolios:
portfolio_id, uuid
user_id, uuid
name, character varying(100)
description, text
initial_capital, numeric(18,2)
created_at, timestamp with time zone
is_active, boolean
currency, character(3)
risk_profile, risk_level_enum
target_return, numeric(5,2)
max_drawdown_limit, numeric(5,2)
rebalancing_frequency, character varying(20)
parent_portfolio_id, uuid
auto_rebalance, boolean
rebalance_threshold, numeric(5,2)
management_fee, numeric(5,4)
performance_fee, numeric(5,2)
max_position_size, numeric(5,2)
max_sector_allocation, numeric(5,2)
max_correlation_threshold, numeric(5,2)
investment_style, character varying(50)
investment_horizon, character varying(20)
benchmark_instrument_id, uuid
status, character varying(20)
inception_date, timestamp with time zone
closure_date, timestamp with time zone
updated_at, timestamp with time zone

roles:
role_id, uuid
name, character varying(50)
description, text
permissions, jsonb
is_system_role, boolean
created_at, timestamp with time zone

strategies:
strategy_id, uuid
name, character varying(100)
description, text
type, character varying(50)
created_at, timestamp with time zone
is_active, boolean
default_parameters, jsonb
version, character varying(20)
creator, character varying(100)
performance_summary, jsonb
risk_level, risk_level_enum
parent_strategy_id, uuid
category, character varying(50)
subcategory, character varying(50)
min_capital_required, numeric(15,2)
max_drawdown_limit, numeric(5,2)
recommended_timeframes, timeframe_enum[]
suitable_instruments, instrument_type_enum[]
algorithm_type, character varying(50)
complexity_score, integer
execution_frequency, character varying(20)
regulatory_approval, boolean
compliance_notes, text
last_audit_date, timestamp with time zone
updated_at, timestamp with time zone
deprecated_at, timestamp with time zone

strategy_configs:
config_id, uuid
user_id, uuid
strategy_id, uuid
parameters, jsonb
created_at, timestamp with time zone
updated_at, timestamp with time zone
is_active, boolean
name, character varying(100)
description, text
performance_summary, jsonb
is_favorite, boolean
risk_tolerance, numeric(5,2)
max_position_size, numeric(18,8)
stop_loss_percentage, numeric(5,2)
take_profit_percentage, numeric(5,2)
is_paper_trading, boolean
live_trading_approved, boolean
live_trading_approval_date, timestamp with time zone
approved_by, uuid

strategy_performance:
performance_id, uuid
strategy_id, uuid
config_id, uuid
data_id, uuid
instrument_id, uuid
period_start, timestamp with time zone
period_end, timestamp with time zone
timeframe, timeframe_enum
win_rate, numeric(5,2)
profit_factor, numeric(10,4)
max_drawdown, numeric(5,2)
sharpe_ratio, numeric(10,4)
total_trades, integer
winning_trades, integer
losing_trades, integer
avg_profit_loss, numeric(18,8)
avg_win, numeric(18,8)
avg_loss, numeric(18,8)
market_condition, market_condition_enum
sortino_ratio, numeric(10,4)
calmar_ratio, numeric(10,4)
sterling_ratio, numeric(10,4)
information_ratio, numeric(10,4)
treynor_ratio, numeric(10,4)
largest_win, numeric(18,8)
largest_loss, numeric(18,8)
avg_trade_duration_hours, numeric(10,2)
median_trade_duration_hours, numeric(10,2)
consecutive_wins, integer
consecutive_losses, integer
max_consecutive_wins, integer
max_consecutive_losses, integer
value_at_risk_95, numeric(18,8)
expected_shortfall, numeric(18,8)
maximum_adverse_excursion, numeric(18,8)
maximum_favorable_excursion, numeric(18,8)
total_return, numeric(10,4)
annualized_return, numeric(10,4)
monthly_returns, jsonb
return_volatility, numeric(10,4)
downside_deviation, numeric(10,4)
avg_position_size, numeric(18,8)
max_position_size, numeric(18,8)
position_size_volatility, numeric(10,4)
kelly_criterion, numeric(5,2)
calculated_at, timestamp with time zone
calculation_version, character varying(20)

subscriptions:
subscription_id, uuid
user_id, uuid
subscription_level, subscription_level_enum
start_date, timestamp with time zone
end_date, timestamp with time zone
monthly_fee, numeric(10,2)
is_active, boolean
auto_renew, boolean
payment_method_id, character varying(100)
last_payment_date, timestamp with time zone
next_payment_date, timestamp with time zone
trial_period_days, integer
discount_percentage, numeric(5,2)
promotional_code, character varying(50)
billing_cycle, character varying(20)
grace_period_days, integer

system_health_metrics:
metric_id, uuid
metric_name, character varying(100)
metric_value, numeric(15,4)
metric_unit, character varying(20)
timestamp, timestamp with time zone
component, character varying(50)
severity, character varying(20)
metadata, jsonb
expires_at, timestamp with time zone

technical_indicators:
indicator_id, uuid
data_id, uuid
instrument_id, uuid
indicator_type, character varying(50)
parameters, jsonb
values, jsonb
calculated_at, timestamp with time zone
timeframe, timeframe_enum
validity_period, timestamp with time zone
signal_strength, numeric(5,2)
partition_key, character varying(50)
calculation_method, character varying(100)
data_points_used, integer
confidence_level, numeric(5,2)

trade_executions:
execution_id, uuid
trade_id, uuid
broker_reference, character varying(100)
execution_status, execution_status_enum
execution_time, timestamp with time zone
executed_price, numeric(18,8)
executed_volume, numeric(18,8)
execution_details, jsonb
latency_ms, integer
broker_commission, numeric(18,8)
slippage, numeric(18,8)
execution_venue, character varying(100)
execution_algorithm, character varying(50)
market_impact, numeric(18,8)
implementation_shortfall, numeric(18,8)
order_route, text
execution_quality_score, numeric(5,2)
price_improvement, numeric(18,8)
mifid_transaction_id, character varying(100)
regulatory_flags, jsonb
created_at, timestamp with time zone

trades:
trade_id, uuid
user_id, uuid
instrument_id, uuid
data_id, uuid
strategy_id, uuid
config_id, uuid
direction, trade_direction_enum
volume, numeric(18,8)
entry_price, numeric(18,8)
exit_price, numeric(18,8)
stop_loss, numeric(18,8)
take_profit, numeric(18,8)
entry_time, timestamp with time zone
exit_time, timestamp with time zone
profit_loss, numeric(18,8)
profit_loss_percentage, numeric(10,4)
commission, numeric(18,8)
status, trade_status_enum
notes, text
tags, character varying[]
account_id, uuid
order_type, character varying(20)
time_in_force, character varying(20)
leverage_used, numeric(10,2)
margin_used, numeric(18,8)
risk_reward_ratio, numeric(10,4)
max_risk_amount, numeric(18,8)
position_size_percentage, numeric(5,2)
entry_reason, text
exit_reason, text
market_condition_at_entry, market_condition_enum
volatility_at_entry, numeric(8,4)
created_at, timestamp with time zone
updated_at, timestamp with time zone

user_preferences:
preference_id, uuid
user_id, uuid
theme, theme_enum
notification_settings, jsonb
default_timeframe, timeframe_enum
default_indicators, jsonb
ui_layout, jsonb
alert_preferences, jsonb
language, character varying(10)
currency_preference, character(3)

user_roles:
user_id, uuid
role_id, uuid
assigned_at, timestamp with time zone
assigned_by, uuid

users:
user_id, uuid
username, character varying(50)
email, character varying(100)
password_hash, character varying(255)
full_name, character varying(100)
created_at, timestamp with time zone
last_login, timestamp with time zone
user_type, user_type_enum
account_status, account_status_enum
verification_status, boolean
profile_picture_url, character varying(255)
two_factor_enabled, boolean
failed_login_attempts, integer
locked_until, timestamp with time zone
password_changed_at, timestamp with time zone
email_verified_at, timestamp with time zone
last_ip_address, inet
timezone, character varying(50)
