import pytest


class TestProduct:
    @pytest.mark.vcr
    def test_product_get_details_valid(self, grocy, grocy_api_client):
        product = grocy.product(10)

        assert product.name == "Cheese"
        assert product.available_amount == 5
        assert len(product.barcodes) == 0

    @pytest.mark.vcri3s
    def test_product_get_details_non_existant(self, grocy):
        import requests

        with pytest.raises(requests.exceptions.HTTPError):
            grocy.product(200)
