# -*- encoding:utf-8 -*-

import pandas as pd

def addorder(orderbook, order, type):
    """
    ## add an order into the order history
    - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    ## Inputs:
    #  orderbook     order history
    #  order         new order, contains time/price/quantity/fee rate/etc
    #  type          order type
    - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    ## Outputs:
    #  orderbook     new order history
    """
    datetime = order[0]
    price = order[1]
    quantity = order[2]
    fee = abs(price*quantity*order[3])
    # suspect whether the orderbook is none or not
    if len(orderbook) == 0:
        pnl = 0
        orderbook = orderbook.append(pd.DataFrame({'datetime':[datetime],'price':[price],'quantity':[quantity],'fee':[fee],'pnl':[pnl],'type':[type]}),ignore_index=True)
    else:
        if orderbook['quantity'].sum() == 0:   # for a new position, pnl=0
            pnl = 0
        elif quantity < 0:   # since it is guranteed that it would open a new position in the same direction, it is considered as close position
            pnl = abs(order[1]*order[2]*(1-order[3])) - orderbook['price'].iloc[-1]*orderbook['quantity'].iloc[-1] - orderbook['fee'].iloc[-1]
        else:   # since it is guranteed that it would open a new position in the same direction, it is considered as close position
            pnl = abs(orderbook['price'].iloc[-1]*orderbook['quantity'].iloc[-1]) - orderbook['fee'].iloc[-1] - order[1]*order[2]*(1+order[3])
        orderbook = orderbook.append(pd.DataFrame({'datetime':[datetime],'price':[price],'quantity':[quantity],'fee':[fee],'pnl':[pnl],'type':[type]}),ignore_index=True)

    return orderbook