from unittest import TestCase
import pytest
import convert_crypto_currency


# using python pytest fixture to create and destroy class object
@pytest.yield_fixture(scope="class", autouse=True)
def convert_crypto_currency_fixture(request):
    ''' Creating function fixture for convert crypto currency '''
    # Requirement: to create object only once

    ccc_object = convert_crypto_currency.ConvertCryptoCurrency()
    if request.cls is not None:
        request.cls.ccc_object = ccc_object
    yield ccc_object
    del ccc_object


# implementing fixture to complete test class
@pytest.mark.usefixtures('convert_crypto_currency_fixture')
class TestConvertCryptoCurrency(TestCase):
    ''' Test class to test methods of convert_crypto_currency.py '''

    # Testing validate amount
    def test_validate_amount_1(self):
        result = self.ccc_object.validate_amount('1')
        assert result is True

    def test_validate_amount_2(self):
        result = self.ccc_object.validate_amount('1.5')
        assert result is True

    def test_validate_amount_3(self):
        result = self.ccc_object.validate_amount('0')
        assert result is False

    def test_validate_amount_4(self):
        result = self.ccc_object.validate_amount('-0.5')
        assert result is False

    def test_validate_amount_5(self):
        result = self.ccc_object.validate_amount('0.5')
        assert result is True

    # Testing validate currency
    # testing NATIVE Currencies
    def test_validate_currency_6(self):
        result = self.ccc_object.validate_currency('USD', 'JPY')
        assert result is True

    def test_validate_currency_7(self):
        result = self.ccc_object.validate_currency('CBA', 'XYZ')
        assert result is False

    def test_validate_currency_8(self):
        result = self.ccc_object.validate_currency('USD', 'XYZ')
        assert result is False

    def test_validate_currency_9(self):
        result = self.ccc_object.validate_currency('CBA', 'USD')
        assert result is False

    # testing Crypto Currencies
    def test_validate_currency_10(self):
        result = self.ccc_object.validate_currency('XRP', 'CDT')
        assert result is True

    def test_validate_currency_11(self):
        result = self.ccc_object.validate_currency('XRP', 'XYZ')
        assert result is False

    def test_validate_currency_12(self):
        result = self.ccc_object.validate_currency('CBA', 'CDT')
        assert result is False

    # testing combination of native and crypto currencies
    def test_validate_currency_13(self):
        result = self.ccc_object.validate_currency('USD', 'CDT')
        assert result is True

    def test_validate_currency_14(self):
        result = self.ccc_object.validate_currency('XRP', 'USD')
        assert result is True

    # testing native currency exchange
    def test_convert_native_currency_15(self):
        result = self.ccc_object.convert_native_currency('1', 'USD', 'JPY')
        assert result is not None
        assert result != ""

    def test_convert_native_currency_16(self):
        result = self.ccc_object.convert_native_currency('0.5', 'CBA', 'JPY')
        assert result is None

    def test_convert_native_currency_17(self):
        result = self.ccc_object.convert_native_currency('2.3', 'USD', 'CBA')
        assert result is None

    def test_convert_native_currency_18(self):
        result = self.ccc_object.convert_native_currency('-3.5', 'USD', 'JPY')
        assert result is None

    # testing crypto currency exchange
    def test_convert_crypto_currency_19(self):
        result = self.ccc_object.convert_crypto_currency('1', 'XRP', 'LTC')
        assert result is not None
        assert result != ""

    def test_convert_crypto_currency_20(self):
        result = self.ccc_object.convert_crypto_currency('0.5', 'CBA', 'LTC')
        assert result is None

    def test_convert_crypto_currency_21(self):
        result = self.ccc_object.convert_crypto_currency('2.3', 'XRP', 'CBA')
        assert result is None

    def test_convert_crypto_currency_22(self):
        result = self.ccc_object.convert_crypto_currency('-3.5', 'XRP', 'LTC')
        assert result is None

    # testing convert currency method
    def test_convert_currency_23(self):
        result = self.ccc_object.convert_currency('100', 'JPY', 'LTC')
        assert result is not None

    def test_convert_currency_24(self):
        result = self.ccc_object.convert_currency('100', 'LTC', 'JPY')
        assert result is not None
