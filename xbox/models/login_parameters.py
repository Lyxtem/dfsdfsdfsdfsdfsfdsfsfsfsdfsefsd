class LoginParameters:
    def __init__(
        self,
        url_post: str,
        flow_token: str
    ):
        self.url_post = url_post
        self.flow_token = flow_token
        self.referer = None