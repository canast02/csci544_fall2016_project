import json


def jsonify(object):
    business = _jsonify_business(object)

    return business


def _jsonify_business(obj):
    fields = [
        'display_phone',
        'distance',
        'eat24_url',
        'id',
        'image_url',
        'is_claimed',
        'is_closed',
        'menu_provider',
        'menu_date_updated',
        'mobile_url',
        'name',
        'phone',
        'rating',
        'rating_img_url',
        'rating_img_url_small',
        'rating_img_url_large',
        'reservation_url',
        'review_count',
        'snippet_image_url',
        'snippet_text',
        'url'
    ]

    nested_fields = {
        'categories': _jsonify_category,
        'location': _jsonify_location,
        'reviews': _jsonify_review
    }

    bussiness = {}

    for f in fields:
        bussiness[f] = obj.__dict__[f]

    for f, p in nested_fields.items():
        if isinstance(obj.__dict__[f], (list, tuple)):
            bussiness[f] = [p(x) for x in obj.__dict__[f]]
        else:
            bussiness[f] = p(obj.__dict__[f])

    return bussiness


def _jsonify_location(obj):
    fields = [
        'address',
        'city',
        'country_code',
        'cross_streets',
        'display_address',
        'geo_accuracy',
        'neighborhoods',
        'postal_code',
        'state_code'
    ]

    def _jsonify_coordinates(obj):
        fields = [
            'latitude',
            'longitude'
        ]

        return {key: obj.__dict__[key] for key in fields}

    nested_fields = {
        'coordinate': _jsonify_coordinates
    }

    location = {}

    for f in fields:
        location[f] = obj.__dict__[f]
    for f, p in nested_fields.items():
        location[f] = p(obj.__dict__[f])

    return location


def _jsonify_category(obj):
    return {'name': obj[0], 'alias': obj[1]}


def _jsonify_review(obj):
    fields = [
        'id',
        'excerpt',
        'time_created',
        'rating',
        'rating_image_url',
        'rating_image_small_url',
        'rating_image_large_url',
    ]

    if obj is None:
        return []

    review = {f: obj.__dict__[f] for f in fields}

    return review
