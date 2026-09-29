
def transform_cart(cart):
    return {
        "cart_id": cart["cart_id"],
        "user_id": cart["user_id"],
        "total": cart["total"],
        "discounted_total": cart["discounted_total"],
        "total_products": cart["total_products"],
        "total_quantity": cart["total_quantity"],
    }

def transform_cart_item(cart_id, product):
    return {
        "cart_id": cart_id,
        "product_id": product["id"],
        "title": product["title"],
        "price": product["price"],
        "quantity": product["quantity"],
        "total": product["total"],
        "discount_percentage": product["discountPercentage"],
        "discounted_total": product["discountedTotal"],
        "thumbnail": product["thumbnail"],
    }

def transform_cart_items(cart_id, products):
    return [
        transform_cart_item(cart_id, product)
        for product in products
    ]


def transform_staging_cart(row):
    cart = {
        "cart_id": row["cart_id"],
        "user_id": row["user_id"],
        "total": row["total"],
        "discounted_total": row["discounted_total"],
        "total_products": row["total_products"],
        "total_quantity": row["total_quantity"],
    }

    products = row["products_json"]

    return {
        "cart": transform_cart(cart),
        "items": transform_cart_items(
            row["cart_id"],
            products
        ),
    }

def transform_batch(rows):
    transformed = [
        transform_staging_cart(row)
        for row in rows
    ]

    return transformed