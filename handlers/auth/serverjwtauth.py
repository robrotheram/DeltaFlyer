import jwt

from database.Server import ServerDocuments

secret_key = "secret_string"
options = {
    'verify_signature': True,
    'verify_exp': True,
    'verify_nbf': False,
    'verify_iat': True,
    'verify_aud': False
}


def serverjwtauth(handler_class):
    ''' Handle Tornado JWT Auth '''
    def wrap_execute(handler_execute):
        def require_auth(handler, kwargs):

            auth = handler.request.headers.get('Authorization')
            if auth:

                server = ServerDocuments().get_serverByPublic(auth)
                print server["private_key"]

                try:
                    data = jwt.decode(
                        auth,
                        server["private_key"],
                        options=options
                    )
                    handler.request.headers.add("serverName",data["serverName"])

                except Exception, e:
                    handler._transforms = []
                    handler.set_status(401)
                    handler.write(e.message)
                    handler.finish()
            else:
                handler._transforms = []
                handler.write("Missing authorization")
                handler.finish()

            return True

        def _execute(self, transforms, *args, **kwargs):

            try:
                require_auth(self, kwargs)
            except Exception:
                return False

            return handler_execute(self, transforms, *args, **kwargs)

        return _execute

    handler_class._execute = wrap_execute(handler_class._execute)
    return handler_class