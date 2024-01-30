"""
Simple utility script to calculate the limit close and stop-loss for a trade, given profit target and risk level.

Usage:
    python forex.py
"""
from dataclasses import dataclass

@dataclass
class Trade:
    order_size: int
    limit_price: float
    trade_type: str
    profit_target: float = 0.03
    stop_loss: float = 0.01
    
@dataclass
class TradeInformation:
    trade: Trade
    limit_close: float
    stop_loss: float
    potential_profit: float
    potential_loss: float
    
def calculate_trade_parameters(trade: Trade) -> TradeInformation:
    """
    Calculate the limit close and stop-loss for a trade.

    :param trade: A Trade object containing the order size, limit price, trade type, profit target, and stop-loss.
    :return: A TradeInformation object containing the trade, limit close, stop-loss, potential profit, and potential loss.
    """
    if trade.trade_type not in ['buy', 'sell']:
        raise ValueError("Trade type must be either 'buy' or 'sell'")

    if trade.trade_type == 'buy':
        limit_close = trade.limit_price * (1 + trade.profit_target)
        stop_loss_price = trade.limit_price * (1 - trade.stop_loss)
        potential_profit = (limit_close - trade.limit_price) * trade.order_size
        potential_loss = (trade.limit_price - stop_loss_price) * trade.order_size
    else:  # sell
        limit_close = trade.limit_price * (1 - trade.profit_target)
        stop_loss_price = trade.limit_price * (1 + trade.stop_loss)
        potential_profit = (trade.limit_price - limit_close) * trade.order_size
        potential_loss = (stop_loss_price - trade.limit_price) * trade.order_size

    return TradeInformation(trade, limit_close, stop_loss_price, potential_profit, potential_loss)


if __name__ == '__main__':
    try:
        profit_target: float = float(input("Enter the profit target as decimal (default 0.03): "))
        stop_loss: float = float(input("Enter the stop loss as decimal (default 0.01): "))
    except ValueError:
        print("Invalid input. Using default values.")
        profit_target = 0.03
        stop_loss = 0.01
        
    while True:
        try:
            limit_price = float(input("Enter the limit price: "))
            trade_size: int = int(input("Enter the trade size: "))
            trade_type = input("Enter the trade type (buy/sell): ")
            trade: Trade = Trade(trade_size, limit_price, trade_type, profit_target, stop_loss)
            info: TradeInformation = calculate_trade_parameters(trade)
            output = f"""
            Details:
            Trade Type: {info.trade.trade_type}
            Order Size: {info.trade.order_size}
            Limit Price: {info.trade.limit_price}
            
            Suggestions:
            Limit Close: {info.limit_close}
            Stop Loss: {info.stop_loss}
            Potential Profit: {info.potential_profit}
            Potential Loss: {info.potential_loss}
            """
            print(output)
            
        except ValueError:
            print("Invalid input. Please try again.")