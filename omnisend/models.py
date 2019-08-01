from datetime import datetime

from marshmallow import Schema, ValidationError, fields, validates_schema

from omnisend import ContactStatuses


class Product(Schema):
    cartProductID = fields.Str(required=True)
    productID = fields.Str(required=True)
    variantID = fields.Str(required=True)
    title = fields.Str(required=True)
    description = fields.Str()
    quantity = fields.Str(required=True)
    price = fields.Str(required=True)
    oldPrice = fields.Str()
    discount = fields.Str()
    imageUrl = fields.Str()
    productUrl = fields.Str()


class Cart(Schema):
    cartID = fields.Str(required=True)
    email = fields.Str()
    createdAt = fields.DateTime()
    updatedAt = fields.DateTime()
    attributionID = fields.Str()
    currency = fields.Str(required=True)
    cartSum = fields.Int(required=True)
    cartRecoveryUrl = fields.Str()
    products = fields.List(fields.Nested(Product))


class Contact(Schema):
    contactID = fields.Str()
    email = fields.Str(required=True)
    createdAt = fields.Str()
    firstName = fields.Str()
    lastName = fields.Str()
    tags = fields.List(fields.Dict())
    country = fields.Str()
    countryCode = fields.Str()
    state = fields.Str()
    city = fields.Str()
    address = fields.Str()
    postalCode = fields.Str()
    gender = fields.Str()
    phone = fields.Str()
    birthdate = fields.DateTime()
    optInDate = fields.DateTime()
    optInIP = fields.Str()
    status = fields.Str(default=ContactStatuses.SUBSCRIBED)
    statusDate = fields.DateTime(
        format="%Y-%m-%dT%H:%M:%S+00:00", default=datetime.utcnow()
    )
    customFields = fields.Str()
    sendWelcomeEmail = fields.Str()
    customProperties = fields.Dict()


class Order(Schema):
    orderID = fields.Str()
    orderNumber = fields.Int()
    email = fields.Str()
    cartID = fields.Str()
    attributionID = fields.Str()
    shippingMethod = fields.Str()
    trackingCode = fields.Str()
    courierTitle = fields.Str()
    courierUrl = fields.Str()
    orderUrl = fields.Str()
    source = fields.Str()
    tags = fields.List(fields.Dict())
    discountCode = fields.Str()
    discountValue = fields.Int()
    discountType = fields.Str()
    currency = fields.Str()
    subTotalSum = fields.Str()
    orderSum = fields.Int()
    discountSum = fields.Int()
    taxSum = fields.Int()
    shippingSum = fields.Int()
    created_at = fields.DateTime(
        format="%Y-%m-%dT%H:%M:%S+00:00", default=datetime.utcnow()
    )
    updated_at = fields.DateTime(
        format="%Y-%m-%dT%H:%M:%S+00:00", default=datetime.utcnow()
    )
    contactNote = fields.Str()
    paymentMethod = fields.Str()
    paymentStatus = fields.Str()
    fulfillmentStatus = fields.Str()
    billingAddress = fields.Dict()  # TODO:
    shippingAddress = fields.Dict()  # TODO:
    products = fields.Str()
    customFields = fields.Dict()

    @validates_schema
    def validate_ids(self, data, **kwargs):
        if "email" not in data and "contact_id" not in data:
            raise ValidationError("`email` or/and `contactID` must be provided.")
