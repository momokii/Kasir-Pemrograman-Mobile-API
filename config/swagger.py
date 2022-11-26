template = {
    "swagger": "2.0",
    "info": {
        "title": "REST API Kasir Pemrograman Mobile",
        "description": "API untuk projek pemrograman mobile",
        "contact": {
            "responsibleOrganization": "",
            "responsibleDeveloper": "",
            "email": "kelanachandra7@gmail.com",
            "url": "https://kasir-api-project-mobile.herokuapp.com/",
            "github" : "https://github.com/momokii/"
        },
        "termsOfService": "https://github.com/momokii/Kasir-Pemrograman-Mobile-API",
        "version": "1.0"
    },
    "basePath": "/api/kasir",  # base bash for blueprint registration
    "schemes": [
        "http",
        "https"
    ],
}


swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/"
}
