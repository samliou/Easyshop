# zope imports
from zope.interface import implements
from zope.component import adapts

# CMFCore imports
from Products.CMFCore.utils import getToolByName

# easyshop imports
from easyshop.core.interfaces import IProductManagement
from easyshop.core.interfaces import IShop

class ShopProductManagement:
    """An adapter, which provides product management for shop content objects.
    """
    implements(IProductManagement)
    adapts(IShop)
    
    def __init__(self, context):
        """
        """
        self.context = context

    def getAllProducts(self):
        """
        """
        raise Exception
        
    def getAmountOfProducts(self):
        """
        """        
        raise Exception
        
    def getProducts(self):
        """
        """
        catalog = getToolByName(self.context, "portal_catalog")
        brains = catalog.searchResults(
            object_provides = "easyshop.core.interfaces.catalog.product.IProduct",
            path = "/".join(self.context.products.getPhysicalPath()),
            sort_on = "sortable_title",
        )

        return brains
        
    def getTotalAmountOfProducts(self):
        """
        """
        raise Exception