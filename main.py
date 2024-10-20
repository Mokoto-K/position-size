import guts as exchange

while True:
    direction = input("Enter Direction: ")

    if direction == "buy".lower() or direction == "sell".lower():
        entry_price = int(input("Enter entry price: "))
        stop_price = int(input("Enter stop price: "))
        risk_percent = float(input("Enter amount of risk: "))
        account_size = exchange.get_balance()

        if direction == "buy".lower():
            difference = (entry_price - stop_price) / entry_price
            break
        else:
            difference = (stop_price - entry_price) / entry_price
            break

    else:
        print("Input incorrect, try 'buy' or 'sell'")


risk_amount = account_size * risk_percent / 100
size = risk_amount / difference
print(f"Direction: {direction}\nEntry: {entry_price}\nStop Loss: {stop_price}\nSize: {round(size)}")
