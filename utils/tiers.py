def get_tier(wallet_value):
    if wallet_value < 1000:
        return 1, 0.3
    elif wallet_value < 5000:
        return 2, 0.5
    elif wallet_value < 15000:
        return 3, 1.0
    elif wallet_value < 25000:
        return 4, 1.5
    return 5, 2.0
