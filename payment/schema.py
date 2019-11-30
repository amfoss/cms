import graphene
import json
import requests
from payment.paytm import Checksum
from framework.settings import PAYTM_KEY, PAYTM_MERCHANT_ID, PAYTM_WEBSITE_NAME, PAYTM_ENDPOINT


class APIException(Exception):
    def __init__(self, message, code=None):
        self.context = {}
        if code:
            self.context['errorCode'] = code
        super().__init__(message)


class PaymentAttrObj(graphene.ObjectType):
    txnToken = graphene.String()


class Query(object):
    initiateTransaction = graphene.Field(PaymentAttrObj,
                                         amount=graphene.Float(required=True),
                                         callback=graphene.String(required=True),
                                         customerID=graphene.String(required=True),
                                         orderID=graphene.String()
                                         )
    fetchPaymentOptions = graphene.Field(PaymentAttrObj,
                                         txnToken=graphene.String(required=True),
                                         orderID=graphene.String(required=True)
                                         )
    initiateUPITransaction = graphene.Field(PaymentAttrObj,
                                            txnToken=graphene.String(required=True),
                                            orderID=graphene.String(required=True),
                                            UPIAddress=graphene.String(required=True)
                                            )

    def resolve_initiateTransaction(self, info, **kwargs):
        amount = kwargs.get('amount')
        callbackUrl = kwargs.get('callback')
        customerID = kwargs.get('customerID')

        orderID = kwargs.get("orderID")
        if orderID is None:
            orderID = "VIDYUT2345"

        paytmParams = dict()
        paytmParams["body"] = {
            "requestType": "Payment",
            "mid": PAYTM_MERCHANT_ID,
            "websiteName": PAYTM_WEBSITE_NAME,
            "orderId": orderID,
            "callbackUrl": callbackUrl,
            "txnAmount": {
                "value": amount,
                "currency": "INR",
            },
            "userInfo": {
                "custId": customerID
            },
        }
        checksum = Checksum.generate_checksum_by_str(json.dumps(paytmParams["body"]), PAYTM_KEY)
        paytmParams["head"] = {
            "signature": checksum
        }

        post_data = json.dumps(paytmParams)
        url = PAYTM_ENDPOINT + "initiateTransaction?mid=" + PAYTM_MERCHANT_ID + "&orderId=" + orderID

        response = requests.post(url, data=post_data, headers={"Content-type": "application/json"}).json()
        if response['body']['resultInfo']['resultStatus'] != 'F':
            return PaymentAttrObj(txnToken=response['body']['txnToken'])
        else:
            raise APIException(response['body']['resultInfo']['resultMsg'],
                               code=response['body']['resultInfo']['resultCode'])

    def resolve_fetchPaymentOptions(self, info, **kwargs):
        orderID = kwargs.get("orderID")
        txnToken = kwargs.get("txnToken")

        paytmParams = dict()
        paytmParams["head"] = {
            "channelId": "WEB",
            "txnToken": txnToken,
            "clientId": "C11",
            "version": "v1",
        }
        paytmParams["body"] = {
            "paymentFlow": "ADDANDPAY",
            "merchantPayOption": {
                "paymentModes": [
                    "UPI", "WALLET"
                ]
            },
            "nativeJsonRequestSupported": True,
            "addMoneyPayOption": {
                "paymentModes": [
                    "UPI", "WALLET"
                ]
            },
            "merchantDetails": {
                "merchantName": "amFOSS CMS"
            },

            "merchantOfferMessage": "sss"
        }
        post_data = json.dumps(paytmParams)
        url = PAYTM_ENDPOINT + "fetchPaymentOptions?mid=" + PAYTM_MERCHANT_ID + "&orderId=" + orderID
        response = requests.post(url, data=post_data, headers={"Content-type": "application/json"}).json()
        print(response)
        PaymentAttrObj(txnToken=response)

    def resolve_initiateUPITransaction(self, info, **kwargs):
            orderID = kwargs.get("orderID")
            txnToken = kwargs.get("txnToken")
            UPIAddress = kwargs.get("UPIAddress")

            url = PAYTM_ENDPOINT + "processTransaction?mid=" + PAYTM_MERCHANT_ID + "&orderId=" + orderID
            paytmParams = dict()
            paytmParams["head"] = {
                "txnToken": txnToken,
                "channelId": "WEB"
            }
            paytmParams["body"] = {
                "mid": PAYTM_MERCHANT_ID,
                "orderID": orderID,
                "requestType": "Payment",
                "paymentMode": "UPI",
                "channelCode": "collect",
                "payerAccount": UPIAddress
            }
            post_data = json.dumps(paytmParams)

            response = requests.post(url, data=post_data, headers={"Content-type": "application/json"}).json()
            print(response)