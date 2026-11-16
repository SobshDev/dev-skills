from shop.pricing import calc


def checkout_total(order, customer):
    return calc(order, customer)
