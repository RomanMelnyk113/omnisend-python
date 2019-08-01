class ClientException(Exception):
    pass


class ContactStatuses:
    SUBSCRIBED = "subscribed"


class OrderPaymentStatus:
    AWAITING_PAYMENT = "awaitingPayment"
    PARTIALLY_PAID = "partiallyPaid"
    PAID = "paid"
    PARTIALLY_REFUNDED = "partiallyRefunded"
    REFUNDED = "refunded"
    VOIDED = "voided"


class OrderFulfilmentStatus:
    UNFULFILLED = "unfulfilled"
    IN_PROGRESS = "inProgress"
    FULFILLED = "fulfilled"
    DELIVERED = "delivered"
    RESTOCKED = "restocked"


# awaitingPayment = "Awaiting payment"
#     partiallyPaid = "Partially paid"
#     paid = "Order paid"
#     partiallyRefunded = "Partially refunded"
#     refunded = "Refunded"
#     voided = "Payment canceled"


# unfulfilled	order placed
# inProgress	order in progress
# fulfilled	order prepared for pickup (if delivery type pickup selected) or shipped
# delivered	order has been picked up by or delivered to customer
# restocked	Restocked
