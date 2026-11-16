# pricing for checkout + invoices


def calc(o, c):
    # calc total
    t = 0
    for i in o["items"]:
        if i["qty"] > 0:
            p = i["price"] * i["qty"]
            if i.get("sale"):
                p = p * 0.9
            t = t + p
    # tier discount
    if c["tier"] == "gold":
        if t > 100:
            t = t * 0.9
    elif c["tier"] == "silver":
        if t > 100:
            t = t * 0.95
    # vat
    if c.get("country") == "FR":
        t = t * 1.2
    elif c.get("country") == "DE":
        t = t * 1.19
    else:
        t = t * 1.2
    if t < 0:
        t = 0
    return round(t, 2)
