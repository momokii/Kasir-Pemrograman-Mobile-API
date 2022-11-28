template = {
    "swagger": "2.0",
    "info": {
        "title": "Kasir REST API Pemrograman Mobile ",
        "description": "API untuk projek pemrograman mobile",
        "contact": {
            "responsibleOrganization": "",
            "responsibleDeveloper": "",
            "email": "kelanachandra7@gmail.com",
            "url": "https://kelanach.herokuapp.com/",
            "github" : "https://github.com/momokii/"
        },
        "termsOfService": "https://github.com/momokii/REST-API-Project-1",
        "version": "1.0"
    },
    "basePath": "/api/kasir",  # base bash for blueprint registration
    "schemes": [
        "http",
        "https"
    ],
}


swagger_config = {
    "headers": [],
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