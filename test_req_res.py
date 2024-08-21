

# ----------------------------------------------
# =============== typed_fetch.py ===============
# ----------------------------------------------
import requests
import json
from typing import Any, Dict, Optional, Type, TypeVar


T = TypeVar('T')

def typed_fetch(domain: str, url_template: str, method: str, response_200: Type[T], query: Optional[Dict[str, Any]] = None, path: Any = None, body: Any = None) -> T:
    # Replace placeholders in the url_template with values from path
    url = url_template
    if path:
        for key, value in path.items():
            placeholder = f'{{{key}}}'
            if placeholder in url:
                url = url.replace(placeholder, str(value))
    
    # Convert query dictionary to query parameters
    query_params = ''
    if query:
        query_params = '?' + '&'.join([f'{key}={value}' for key, value in query.items()])
    
    # Full URL with query parameters
    full_url = domain + url + query_params
    
    # Convert body dictionary to JSON
    headers = {'Content-Type': 'application/json'}
    json_body = json.dumps(body) if body else None
    
    # Make the HTTP request
    try:
        response = requests.request(method=method, url=full_url, headers=headers, data=json_body)
        response.raise_for_status()  # Raises HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        try:
            # Attempt to parse the error response body
            error_response = e.response.json() # type: ignore
        except (ValueError, AttributeError):
            error_response = e.response.text if e.response else str(e)
        raise requests.exceptions.RequestException(f"Request failed: {error_response}") from e

    # Check for successful request and return the response content
    if response.status_code >= 200 and response.status_code < 300:
        try:
            # TODO: add runtime validation against
            data = response.json()
            return { "data": data } # type: ignore
        except json.JSONDecodeError:
            return response.text # type: ignore
    else:
        try:
            error_response = response.json()
        except json.JSONDecodeError:
            error_response = response.text
        raise requests.exceptions.HTTPError(f"HTTP Error: {response.status_code} - {error_response}")

# ----------------------------------------------
# =============== typed_fetch.py ===============
# ----------------------------------------------

from tests.test1.__generated_api_types import ModelMapping

# ----------- global config -----------
domain = 'http://localhost:3000'

# ----------- per route config -----------
# there is a lot of duplicities... ugh 

class POST_store_order:
    endpoint = ModelMapping._store_order.POST

    request_body = endpoint.request_body
    response_200 = endpoint.response_200

    @staticmethod
    def fetch(request_body: request_body) -> response_200:
        data = typed_fetch(
            domain,
            url_template=POST_store_order.endpoint.URL,
            method=POST_store_order.endpoint.METHOD,
            # path=path,
            body=request_body,
            response_200=POST_store_order.response_200
        )
        return data



class Services:
    POST_store_order = POST_store_order


# ----------------------------------------------
# ================= app runtime =================
# ----------------------------------------------
# app API call

def main():
    res1 = Services.POST_store_order.fetch(
        request_body = {
            "id": 1,
            "petId": 2,
            "quantity": 3,
            "shipDate": "xxx",
            "status": "placed",
            "complete": True,
        }
    )

    opt_str = res1['data']


main()

