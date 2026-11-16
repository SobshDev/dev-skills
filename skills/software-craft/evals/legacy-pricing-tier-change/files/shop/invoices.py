from shop.pricing import calc


def invoice_line(order, customer):
    return f"Total due: {calc(order, customer):.2f} EUR"
