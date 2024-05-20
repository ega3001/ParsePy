import json
import io
import uuid

import requests
import magic


class Parse:
    """Class for comfortable managing Parse Server data
    """
    def __init__(self, url: str, app_id: str, master_key: str):
        """Initializing requests headers

            Parameters:
                url: server url
                app_id: parse application id
                master_key: master key for connection
        """

        self.url = url
        self.app_id = app_id
        self.master_key = master_key
        self.headers = {
            'X-Parse-Application-Id': self.app_id,
            'X-Parse-Master-Key': self.master_key
        }

    def _return_result(func):
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            if res.status_code > 299 and res.status_code < 200:
                raise Exception(f"ParseDal: something went wrong during request: {res.content}")
            return res.json()
        return wrapper
    
    def _get_class_headers(self):
        copy = self.headers
        copy['Content-type'] = 'application/json'
        return copy
    
    def make_file_link(self, name: str, link: str) -> dict:
        """Prepare file data for linking to a class

            Parameters:
                name: file name
                link: file link
            Returns:
                dict: filled with prepared data
        """

        return {
            'name': name,
            'url': link,
            '__type': 'File'
        }

    @_return_result
    def upload_file(self, bytes: io.BytesIO, mime: str = None, name: str = None) -> dict:
        """Uploading file

            Parameters:
                bytes: file bytes
                mime: file mime type, if not provided it'll auto finded
                name: file name, if not provided it'll auto generated
            Returns:
                dict: filled with created file name and link to it
        """

        content = bytes.read()
        if not mime:
            mime = magic.Magic(mime=True).from_buffer(content[:2048])
        if not name:
            name = f"{uuid.uuid4()}.{mime.split('/')[1]}"

        loc_headers = self.headers
        loc_headers['Content-type'] = mime
        return requests.post(
            f"{self.url}/parse/files/{name}",
            data=content,
            headers=loc_headers
        )
    
    @_return_result
    def delete_file(self, name: str) -> dict:
        """Deleting provided file from server by name

            Parameters:
                name: file name
            Returns:
                dict: deletion result
        """

        return requests.delete(
            f"{self.url}/parse/files/{name}",
            headers=self.headers
        )

    @_return_result
    def get_object(self, class_name: str, obj_id: str) -> dict:
        """Returns class object

            Parameters:
                class_name: object class name for search in
                obj_id: exact object id for search
            Returns:
                dict: filled with object fields or search error
        """

        return requests.get(
            f"{self.url}/parse/classes/{class_name}/{obj_id}",
            headers=self._get_class_headers()
        )

    @_return_result
    def post_object(self, class_name: str, data: dict) -> dict:
        """Add new object to class

            Parameters:
                class_name: object class name for paste in
                data: dictionary with future class object fields info
            Returns:
                dict: with createdAt and objectId fields
        """

        return requests.post(
            f"{self.url}/parse/classes/{class_name}",
            headers=self._get_class_headers(),
            json=data
        )
    
    @_return_result
    def put_object(self, class_name: str, obj_id: str, data: dict) -> dict:
        """Update existing class object

            Parameters:
                class_name: object class name for paste in
                obj_id: object id for update
                data: updated object fields
            Returns:
                dict: with updatedAt field
        """

        return requests.put(
            f"{self.url}/parse/classes/{class_name}/{obj_id}",
            headers=self._get_class_headers(),
            json=data
        )
    
    @_return_result
    def query_object(self, class_name: str, json_query: dict = {}) -> dict:
        """Search for objects by filters
            
            Parameters:
                class_name: class name for search
                json_query: dict with fields filters
            Returns:
                dict: with result field with array
        """
        
        return requests.get(
            f"{self.url}/parse/classes/{class_name}",
            data=json.dumps(json_query),
            headers=self._get_class_headers()
        )
    
    @_return_result
    def delete_object(self, class_name: str, obj_id: str) -> dict:
        """Deleting object

            Parameters:
                class_name: object class name
                obj_id: object id which would be deleted
            Returns:
                dict: empty or with error code
        """
        
        return requests.delete(
            f"{self.url}/parse/classes/{class_name}/{obj_id}",
            headers=self._get_class_headers()
        )
        