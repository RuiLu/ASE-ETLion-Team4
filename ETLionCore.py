import time

class ETLionCore(object):
    def __init__(self, **kwargs):
        self.self.order_discount = kwargs["order_discount"]
        self.self.order_size = kwargs["order_size"]
        self.inventory = kwargs["inventory"]
        self.trading_freq = kwargs["trading_frequency"]

    def trade(self):
        # Start with all shares and no profit
        qty = INVENTORY
        pnl = 0

        # Repeat the strategy until we run out of shares.
        while qty > 0:
            # Query the price once every N seconds.
            for _ in xrange(self.trading_freq):
                time.sleep(1)
                quote = json.loads(urllib2.urlopen(QUERY.format(random.random())).read())
                price = float(quote['top_bid']['price'])
                print "Quoted at %s" % price

            # Attempt to execute a sell order.
            order_args = (self.order_size, price - self.order_discount)
            print "Executing 'sell' of {:,} @ {:,}".format(*order_args)
            url   = ORDER.format(random.random(), *order_args)
            order = json.loads(urllib2.urlopen(url).read())

            # Update the PnL if the order was filled.
            if order['avg_price'] > 0:
                price    = order['avg_price']
                notional = float(price * self.order_size)
                pnl += notional
                qty -= self.order_size
                print "Sold {:,} for ${:,}/share, ${:,} notional".format(self.order_size, price, notional)
                print "PnL ${:,}, Qty {:,}".format(pnl, qty)
            else:
                print "Unfilled order; $%s total, %s qty" % (pnl, qty)

            time.sleep(1)