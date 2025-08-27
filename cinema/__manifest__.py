{
    'name': 'Cinema',
    'category': 'Entertainment',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/cinema_menus_view.xml',
        'views/cinema_movies_views.xml',
        'views/cinema_genres_views.xml',
        'views/cinema_production_companies_views.xml',
        'views/cinema_review_views.xml',
        'views/cinema_persons_views.xml',
        'views/cinema_search_view.xml'
    ],
    'application': True,
}
