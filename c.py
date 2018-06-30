import json
import requests
from bs4 import BeautifulSoup


class ConvertCryptoCurrency(object):
    ''' Class ConvertCryptoCurrency '''

    def validate_amount(self, amount):
        ''' To validate amount, should be greater than 0 '''

        if float(amount) > 0:
            return True
        return False

    def __validate_currency_from_json(self, currency):
        ''' To validate native currencies '''

        with open('native_currencies.json', 'r') as json_file:
            currency_dict = json.load(json_file)
            if currency in currency_dict.keys():
                return True
        return False

    def __validate_currency_from_crypto_compare(self, currency):
        ''' To validate crypto currencies '''

        try:
            url = "https://www.cryptocompare.com/api/data/coinlist/"
            response = requests.get(url)
            response_content = response.content  # getting complete response data

            # decoding response content as it is of byte format, so that we get proper string json
            str_json = response_content.decode('utf8').replace("'", '"')

            # now converting string to dict
            response_dict = json.loads(str_json)

            # getting "Data" from response_dict : Data comprises of information about all crypto currencies
            response_data = response_dict["Data"]

            # evaluating currency type in response data in order to validate it
            if currency in response_data.keys():
                return True
            return False
        except Exception as exception:
            print('Caught exception. ' + str(exception))

    def validate_currency(self, from_currency, to_currency):
        ''' To validate from and to currency '''

        # params
        validated_from_currency = False
        validated_to_currency = False

        # CASE 1: FROM_CURRENCY COULD BE NATIVE TYPE
        # validating from_currency from json file
        if self.__validate_currency_from_json(from_currency):
            validated_from_currency = True

        # CASE 2: FROM_CURRENCY COULD BE CRYPTO TYPE
        # validating from_currency from CRYPTO COMPARE
        if not validated_from_currency:
            if self.__validate_currency_from_crypto_compare(from_currency):
                validated_from_currency = True

        # CASE 3: TO_CURRENCY COULD BE NATIVE TYPE
        # validating to_currency from json file
        if self.__validate_currency_from_json(to_currency):
            validated_to_currency = True

        # CASE 4: TO_CURRENCY COULD BE CRYPTO TYPE
        # validating to_currency from CRYPTO COMPARE
        if not validated_to_currency:
            if self.__validate_currency_from_crypto_compare(to_currency):
                validated_to_currency = True

        # checking if both currencies are valid i.e. either native or crypto currency
        if validated_from_currency and validated_to_currency:
            return True
        return False

    def convert_native_currency(self, amount, from_currency, to_currency):
        ''' To convert the given amount from native currency to another '''

        try:
            validated_amount = self.validate_amount(amount)
            validate_currency_type = self.validate_currency(
                from_currency, to_currency)
            if validated_amount is True and validate_currency_type is True:
                url = "https://finance.google.com/finance/converter?a=" + \
                    amount + "&from=" + from_currency + "&to=" + to_currency
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                return soup.find(id="currency_converter_result").text.strip()

            # in case amount or currency is not validated
            return None
        except Exception as exception:
            print('Caught exception. ' + str(exception))

    def convert_crypto_currency(self, amount, from_currency, to_currency):
        ''' To convert the given amount from one cryptocurrency to another '''

        try:
            validated_amount = self.validate_amount(amount)
            validate_currency_type = self.validate_currency(
                from_currency, to_currency)
            if validated_amount is True and validate_currency_type is True:
                url = "https://min-api.cryptocompare.com/data/pricemulti?fsyms=" + \
                    from_currency + "&tsyms=" + to_currency
                response = requests.get(url)
                exchange_value = response.json()[from_currency][to_currency]
                return str(float(amount) * exchange_value)

            # in case amount or currency is not validated
            return None
        except Exception as exception:
            print('Caught exception. ' + str(exception))

    def convert_currency(self, amount, from_currency, to_currency):
        ''' To convert the given amount from one native/crypto currency to another '''

        try:
            validated_amount = self.validate_amount(amount)
            validate_currency_type = self.validate_currency(
                from_currency, to_currency)
            if validated_amount is True and validate_currency_type is True:
                # check if from currency is a native currency or not
                if self.__validate_currency_from_json(from_currency):
                    # if True, then from_currency is native currency
                    native_currency = from_currency
                    crypto_currency = to_currency

                    # get equivalent USD for native_currency
                    calculated_usd = self.convert_native_currency(
                        amount, native_currency, 'USD').split(" ")[3]

                    # get equivalent crypto currency for BTC
                    value = self.convert_crypto_currency(
                        calculated_usd, 'USD', crypto_currency)
                else:
                    native_currency = to_currency
                    crypto_currency = from_currency

                    # get equivalent BTC for crypto currency
                    calculated_usd = self.convert_crypto_currency(
                        amount, crypto_currency, 'USD')

                    # get equivalent BTC for native currency
                    value = self.convert_native_currency(
                        calculated_usd, 'USD', native_currency).split(" ")[3]

                result = "{0} {1} = {2} {3}".format(
                    amount, from_currency, value, to_currency)
                return result

            # in case amount or currency is not validated
            return None
        except Exception as exception:
            print('Caught exception. ' + str(exception))
            return None


