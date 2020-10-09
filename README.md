# django_url_short and demo

[![Build Status](https://travis-ci.org/KarolisM/django_url_short.svg?branch=master)](https://travis-ci.org/KarolisM/django_url_short)

This simple project enables user to create short urls on [Django](https://github.com/django/django) framework.  
Short URLs are created and saved to the database via API.

## Installation

1. Setup environment with `codna`:

    ```bash
    conda env create -f envs/environment.yaml
    ```

1. Activate environment:

    ```bash
    conda activate -n url_short
    ```

1. Start test server for the project:

    ```bash
    ./manage.py makemigrations
    ./manage.py migrate
    ./manage.py createsuperuser
    ./manage.py runserver
    ```

## Options in settings

* **SITE_URL** - site url with `%` which will be replaced with a random part of the short url.  
* **ENCODER** - option to change default `DjangoJSONEncoder`. Used in the API response.  
* **CONTENT_TYPE** - option to change default `application/json` type. Used in the API response.  
* **LINK_EXPIRATION_DELTA** - option to change link expiration delta date.  
* **LINK_LENGTH** - option to change default length of the random part of the short url.

## Usage

1. To create new short link a POST request is send to the url linked to `CreateLink` class.

    ```groovy
    {'link': <url>}
    ```

1. Server will respond with the created short link.

    ```groovy
    {
        'link': <short_url>,
        'destination': <original_url>,
        'expires': <date_time>
    }
    ```

1. If all alright server will respond with `status_code=200`. Otherwise:

    * User is not authenticated - 401
    * Link expired - 410
    * Sort URL does not exist - 404
    * Malformed original URL - 400
    * Failed to fullfil the request - 500

## License

[MIT](LICENSE)