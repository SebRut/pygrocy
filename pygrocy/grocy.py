from pygrocy.utils import parse_date, parse_int, parse_float
from .grocy_api_client import GrocyApiClient


class Grocy(object):
    def __init__(self, base_url, api_key):
        self._api_client = GrocyApiClient(base_url, api_key)

    def stock(self, volatile_only=False):
        if (volatile_only):
            return self._api_client.get_volatile_stock()
        else:
            return self._api_client.get_stock()

    def product(self, product_id):
        return self._api_client.get_product(product_id)


class Product(object):
    def __init__(self, parsed_json):
        self._id = parse_int(parsed_json['id'])
        self._name = parsed_json['name']
        self._description = parsed_json.get('description', None)
        self._location_id = parse_int(parsed_json.get('location_id', None))
        self._qu_id_stock = parse_int(parsed_json.get('qu_id_stock', None))
        self._qu_id_purchase = parse_int(parsed_json.get('qu_id_purchase', None))
        self._qu_factor_purchase_to_stock = parse_float(parsed_json.get('qu_factor_purchase_to_stock', None))
        self._barcodes = parsed_json.get('barcode', "").split(",")
        self._picture_file_name = parsed_json.get('picture_file_name', None)
        self._allow_partial_units_in_stock = bool(parsed_json.get('allow_partial_units_in_stock', None) == "true")
        self._row_created_timestamp = parse_date(parsed_json.get('row_created_timestamp', None))
        self._min_stock_amount = parse_int(parsed_json.get('min_stock_amount', None), 0)
        self._default_best_before_days = parse_int(parsed_json.get('default_best_before_days', None))

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name


class QuantityUnit(object):
    def __init__(self, parsed_json):
        self._id = parse_int(parsed_json['id'])
        self._name = parsed_json['name']
        self._name_plural = parsed_json['name_plural']
        self._description = parsed_json['description']
        self._row_created_timestamp = parse_date(parsed_json['row_created_timestamp'])


class Location(object):
    def __init__(self, parsed_json):
        self._id = parse_int(parsed_json['id'])
        self._name = parsed_json['name']
        self._description = parsed_json['description']
        self._row_created_timestamp = parse_date(parsed_json['row_created_timestamp'])
