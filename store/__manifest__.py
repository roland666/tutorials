{
    'name': 'Store',
    'application': True,
    'depends': [
        'base'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/store_menu_view.xml',
        'views/store_article_views.xml',
        'views/store_category_views.xml',
        'views/store_order_views.xml',
        'views/store_supply_company_views.xml',
        'views/store_delivery_company_views.xml'
    ]
}
