# zope imports
from zope.interface import implements
from zope.component import adapts

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop.core imports
from easyshop.core.interfaces import IAddressManagement
from easyshop.core.interfaces import ICheckoutManagement
from easyshop.core.interfaces import ICustomerManagement
from easyshop.core.interfaces import IShop

METHODS = {
    "START"                    : "_startCheckout",
    "ADDED_ADDRESS"            : "_addedAddress",
    "EDITED_ADDRESS"           : "_editedAddress",
    "SELECTED_SHIPPING_METHOD" : "_selectedShipping",
    "SELECTED_PAYMENT_METHOD"  : "_selectedPayment",
}

class CheckoutManagement:
    """
    """
    implements(ICheckoutManagement)
    adapts(IShop)

    def __init__(self, context):
        """
        """
        self.context = context

    def getNextURL(self, id):
        """Returns next URL by given id.
        """
        # Calculate next url
        method = METHODS[id]
        method = getattr(self, method)
        return method()
        
    def redirectToNextURL(self, id):
        """Redirects to next URL by given id.
        """
        next_url = self.getNextURL(id)
        self.context.REQUEST.RESPONSE.redirect(next_url)

    def _addedAddress(self):
        """
        """
        if self.context.REQUEST.get("also_invoice_address", "yes") == "yes":
            url = "/checkout-shipping"
        else:
            url = "/checkout-add-address?address_type=invoice"
            
        return self.context.absolute_url() + url

    def _editedAddress(self):
        """
        """
        if self.context.REQUEST.get("also_invoice_address", "yes") == "yes":
            url = self.context.absolute_url() + "/checkout-shipping"
        else:
            customer = ICustomerManagement(self.context).getAuthenticatedCustomer()
            invoice_address = IAddressManagement(customer).getInvoiceAddress()
            if invoice_address is None:
                url = self.context.absolute_url() + "/checkout-add-address?address_type=invoice"
            else:
                url = invoice_address.absolute_url() + "/checkout-edit-address"
                
        return url
                
    def _selectedShipping(self):
        """
        """
        return self.context.absolute_url() + "/checkout-payment"

    def _selectedPayment(self):
        """
        """
        return self.context.absolute_url() + "/checkout-order-preview"

    def _startCheckout(self):
        """
        """
        customer = ICustomerManagement(self.context).getAuthenticatedCustomer()
        shipping_address = IAddressManagement(customer).getShippingAddress()
        
        mtool = getToolByName(self.context, "portal_membership")
        if mtool.isAnonymousUser():
            if shipping_address is None:
                return self.context.absolute_url() + "/checkout-add-address"
            else:
                return shipping_address.absolute_url() + "/checkout-edit-address"
        else:    
            if shipping_address is None:
                return self.context.absolute_url() + "/checkout-add-address"
            else:
                return self.context.absolute_url() + "/checkout-select-addresses"