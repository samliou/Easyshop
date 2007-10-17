# zope imports
from zope.interface import implements
from zope.component import adapts

# EasyShop imports
from Products.EasyShop.interfaces import ICustomerManagement
from Products.EasyShop.interfaces import IShippingManagement
from Products.EasyShop.interfaces import IShippingMethodCriteriaContent
from Products.EasyShop.interfaces import IValidity

class ShippingMethodCriteriaValidity:
    """Adapter which provides IValidity for weight criteria content
    objects.
    """
    implements(IValidity)
    adapts(IShippingMethodCriteriaContent)

    def __init__(self, context):
        """
        """
        self.context = context
        
    def isValid(self, product=None):
        """Checks whether the selected shipping method of the current customer
        is within selected shipping methods of this criterion.
        """        
        shop = self.context.getShop()
        sm = IShippingManagement(shop)
        selected_method = sm.getSelectedShippingMethod()
                
        if selected_method.getId() in self.context.getShippingMethods():
            return True
        else:
            return False