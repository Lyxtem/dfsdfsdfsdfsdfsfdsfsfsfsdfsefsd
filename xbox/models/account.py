class Account:
    def __init__(
        self,
        email: str,
        password: str
    ):
        # Account
        self.email = email
        self.password = password
        self.access_token = None
        self.refresh_token = None
        # 3.0 Auth
        self.user_token = None
        self.xsts_token = None
        self.user_hash = None
        # 2.0 Auth
        self.security_token = None
        self.is_reauthorizing = False

    #region Properties
    @property
    def xbl3_authorization_header(self):
        return f"XBL3.0 x={self.user_hash};{self.xsts_token}"

    @property
    def live_id(self):
        return f"WLID1.0 t={self.access_token}{self.refresh_token}"

    @property
    def xbl2_authorization_header(self):
        return f"XBL2.0 x={self.security_token}"

    #endregion
