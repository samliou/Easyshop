# Zope imports
from DateTime import DateTime

# zope imports
from zope.component import getMultiAdapter

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# EasyShop imports 
from base import EasyShopTestCase
from Products.EasyShop.tests import utils
from Products.EasyShop.interfaces import IValidity

class TestShippingPriceValidityManager(EasyShopTestCase):
    """
    """
    def afterSetUp(self):
        """
        """
        utils.createTestEnvironment(self)
        self.shop.shippingprices.invokeFactory("EasyShopShippingPrice", id="shipping_price")
        self.shipping_price = self.shop.shippingprices.shipping_price

    def testIsValid_1(self):
        """Without criteria
        """
        v = IValidity(self.shipping_price)
        self.assertEqual(v.isValid(), True)

    def testIsValid_2(self):
        """With one invalid criterion.
        """
        # Note product_1 costs 22.00
        # price criterion is true if cart price > criterion price
        self.shipping_price.invokeFactory("EasyShopPriceCriteria", id="price_criterion")
        self.shipping_price.price_criterion.setPrice(23.0)

        view = getMultiAdapter((self.product_1, self.product_1.REQUEST), name="addToCart")
        view.addToCart()
        
        v = IValidity(self.shop.shippingprices.shipping_price)
        self.assertEqual(v.isValid(), False)

    def testIsValid_3(self):
        """With one valid criterion.
        """
        # Note product_1 costs 22.00
        # price criterion is true if cart price > criterion price
        self.shipping_price.invokeFactory("EasyShopPriceCriteria", id="price_criterion")
        self.shipping_price.price_criterion.setPrice(21.0)

        view = getMultiAdapter((self.product_1, self.product_1.REQUEST), name="addToCart")
        view.addToCart()
        
        v = IValidity(self.shop.shippingprices.shipping_price)
        self.assertEqual(v.isValid(), True)

    def testIsValid_4(self):
        """With one invalid and one valid criterion.
        """
        # Note product_1 costs 22.00
        # price criterion is true if cart price > criterion price
        
        # valid
        self.shipping_price.invokeFactory("EasyShopPriceCriteria", id="price_criterion")
        self.shipping_price.price_criterion.setPrice(23.0)
        view = getMultiAdapter((self.product_1, self.product_1.REQUEST), name="addToCart")
        view.addToCart()
        
        # invalid
        self.shipping_price.invokeFactory("EasyShopDateCriteria", id="date_criterion")
        start = end = DateTime() + 1
        self.shipping_price.date_criterion.setStart(start)
        self.shipping_price.date_criterion.setStart(end)
                
        v = IValidity(self.shop.shippingprices.shipping_price)
        self.assertEqual(v.isValid(), False)
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestShippingPriceValidityManager))
    return suite
                                               