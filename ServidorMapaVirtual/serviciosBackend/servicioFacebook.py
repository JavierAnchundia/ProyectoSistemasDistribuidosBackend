import requests

class Facebook():
    def get_info_facebook(self, access_token):
        api_graph = 'https://graph.facebook.com/v8.0/me'
        data = requests.get(
            api_graph,
            params={
                'fields' : 'id, name, email, first_name, last_name',
                'access_token': access_token
            }
        )
        data = data.json()
        if not data['email']:
            email = None
        else:
            email = data['email']

        datos =  {
            "username" : data["id"],
            "first_name" : data['first_name'],
            "last_name" : data['last_name'],
            "is_facebook": True,
            "email" : email,
            "password" : 'mapa_virtual'+data['id'],
            "tipo_usuario": "uf"
        }
        return datos