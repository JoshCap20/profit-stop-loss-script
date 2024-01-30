"""
Simple utility script to calculate the limit close and stop-loss for a trade, given profit target and risk level.

Usage:
    python main.py
"""
from decimal import Decimal, getcontext, InvalidOperation
from dataclasses import dataclass

getcontext().prec = 10

@dataclass
class Trade:
    order_size: int
    limit_price: Decimal
    trade_type: str
    profit_target: Decimal
    stop_loss: Decimal
    
@dataclass
class TradeInformation:
    trade: Trade
    limit_close: Decimal
    stop_loss: Decimal
    potential_profit: Decimal
    potential_loss: Decimal
    
def calculate_trade_parameters(trade: Trade) -> TradeInformation:
    """
    Calculate the limit close and stop-loss for a trade.

    :param trade: A Trade object containing the order size, limit price, trade type, profit target, and stop-loss.
    :return: A TradeInformation object containing the trade, limit close, stop-loss, potential profit, and potential loss.
    """
    if trade.trade_type not in ['buy', 'sell']:
        raise ValueError("Trade type must be either 'buy' or 'sell'")

    limit_close: Decimal = trade.limit_price * (Decimal('1') + trade.profit_target if trade.trade_type == 'buy' else Decimal('1') - trade.profit_target)
    stop_loss_price: Decimal = trade.limit_price * (Decimal('1') - trade.stop_loss if trade.trade_type == 'buy' else Decimal('1') + trade.stop_loss)
    
    potential_profit: Decimal = (limit_close - trade.limit_price) * trade.order_size if trade.trade_type == 'buy' else (trade.limit_price - limit_close) * trade.order_size
    potential_loss: Decimal = (trade.limit_price - stop_loss_price) * trade.order_size 

    return TradeInformation(trade, limit_close, stop_loss_price, potential_profit, potential_loss)


if __name__ == '__main__':
    try:
        profit_target: Decimal = Decimal(input("Enter the profit target as decimal (default 0.03): "))
        stop_loss: Decimal = Decimal(input("Enter the stop loss as decimal (default 0.01): "))
    except (ValueError, InvalidOperation) as e:
        print("Invalid input. Using default values.")
        profit_target = Decimal('0.03')
        stop_loss = Decimal('0.01')
        
    while True:
        try:
            limit_price: Decimal = Decimal(input("Enter the limit price: "))
            trade_size: int = int(input("Enter the trade size: "))
            trade_type: str = input("Enter the trade type (buy/sell): ").lower()
            trade: Trade = Trade(trade_size, limit_price, trade_type, profit_target, stop_loss)
            info: TradeInformation = calculate_trade_parameters(trade)
            output: str = f"""
            Details:
            \tTrade Type: {info.trade.trade_type}
            \tOrder Size: {info.trade.order_size}
            \tLimit Price: {info.trade.limit_price}
            
            Suggestions:
            \tLimit Close: {info.limit_close}
            \tStop Loss: {info.stop_loss}
            \tPotential Profit: {info.potential_profit}
            \tPotential Loss: {info.potential_loss}
            """
            print(output)
            
        except (ValueError, InvalidOperation) as e:
            print(f"Invalid input: {e}. Please try again.")
        except:
            continue
