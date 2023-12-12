{
    "name": "Product/Variant - Dynamic Pricelist",
    "summary" :  "Allows to set prices in multiple pricelists at Product/Variant list view",
    "description" :  "Allows to display multiple pricelists at Product/Variant list view and allows to edit/update the pricelist price from both Pricelist screen and Product/Variant list view. If product doesnot exist as part of pricelist, on pricelist price update from product/variant list view, will in-turn create the pricelist product/variant item and sync/update the price.",
    "category": "Sales",
    'author': 'RMinds Inc.',
    "license": "OPL-1",
    "price": 116.0,
    "currency": 'USD',
    "website":"http://www.rminds.com",
    "version": "16.0.1",
    'images': ['static/description/main_screenshot.jpeg'],
    "depends": ['sale_management'],

    "data": [
        "security/security.xml",
        "views/product_pricelist.xml",
        "views/product_template.xml"
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
    
   
}
