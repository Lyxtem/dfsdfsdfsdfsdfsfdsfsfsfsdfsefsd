class ExternalAuth:
    def __init__(
        self,
        display_name: str,
        account_id: str,
        auth_type: str
    ):
        self.display_name = display_name
        self.account_id = account_id
        self.auth_type = ExternalAuth.__format_auth_type(auth_type)

    @staticmethod
    def __format_auth_type(auth_type: str):
        return auth_type.upper() if len(auth_type) <= 3\
            else auth_type.title()