# CMFCore imports
from Products.CMFCore.utils import getToolByName

# Five imports
from Products.Five.browser import BrowserView

# easyshop imports
from easyshop.core.config import MESSAGES
from easyshop.core.interfaces import ICartManagement
from easyshop.core.interfaces import IItemManagement
from easyshop.core.interfaces import IProductVariantsManagement
from easyshop.core.interfaces import IShopManagement

class ProductAddToCartView(BrowserView):
    """
    """
    def addToCart(self):
        """
        """        
        shop = IShopManagement(self.context).getShop()
        cm = ICartManagement(shop)
        
        cart = cm.getCart()
        if cart is None:
            cart = cm.createCart()
        
        pvm = IProductVariantsManagement(self.context)
        if pvm.hasVariants():

            # Get the actual "product"
            product = pvm.getSelectedVariant() or pvm.getDefaultVariant()
            
            # Using here the selected product ensures that we save the right
            # properties. This is important when the selected variant doesn't 
            # exist.
            properties = []
            for property in product.getForProperties():
                property_id, selected_option = property.split(":")
                properties.append(
                    {"id" : property_id,
                     "selected_option" : selected_option,
                    }
                )
        else:
            
            # The product is the context
            product = self.context

            # Unlike above we take the properties out of the request, because 
            # there is no object wich stores the different properties.
            properties = []
            for property_id, selected_option in self.request.form.items():
                if property_id.startswith("property") == False:
                    continue
             
                if selected_option == "please_select":
                    continue
                 
                properties.append(
                    {"id" : property_id[9:], 
                     "selected_option" : selected_option 
                    }
                )
        
        # get quantity
        quantity = int(self.context.request.get("quantity", 1))

        # returns true if the product was already within the cart    
        result, item_id = IItemManagement(cart).addItem(product, tuple(properties), quantity)
        
        # Set portal message
        putils = getToolByName(self.context, "plone_utils")        
        if result == True:
            putils.addPortalMessage(MESSAGES["CART_INCREASED_AMOUNT"])
            
        else:
            putils.addPortalMessage(MESSAGES["CART_ADDED_PRODUCT"])

        url = "%s/added-to-cart?id=%s" % (shop.absolute_url(), item_id)
        self.context.request.response.redirect(url)