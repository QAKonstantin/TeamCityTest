from custom_requester.custom_requester import CustomRequester


class AuthAPI(CustomRequester):

    def auth_and_get_csrf(self, user_creds):
        self.session.auth = user_creds
        try:
            csrf_token = self.send_request("GET", "/authenticationTest.html").text
        except Exception as e:
            raise ValueError(f"{e}")

        self._update_session_headers(**{"X-TC-CSRF-Token": csrf_token})
