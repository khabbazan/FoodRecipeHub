from locust import HttpUser, task, between


class SIMLUser(HttpUser):
    """
    Load testing user for a REST API.
    """

    wait_time = between(1, 5)

    def on_start(self):
        """
        Perform authentication to obtain the JWT token.
        This method is automatically called when a user starts. It performs the authentication
        process and stores the JWT token for use in APIs.
        """
        # Perform authentication to obtain the JWT token
        login_response = self._perform_login()
        self.jwt_token = login_response["access_token"]

    @task
    def user_list(self):
        query_params = "page_size=10&page_number=1"
        self._perform_query("user/list", query_params, name="User List")

    @task
    def recipe_list(self):
        query_params = "page_size=10&page_number=1"
        self._perform_query("recipe/list", query_params, name="Recipe List")

    @task
    def follower_list(self):
        query_params = "page_size=10&page_number=1"
        self._perform_query("relation/follower_list", query_params, name="Follower List")

    @task
    def following_list(self):
        query_params = "page_size=10&page_number=1"
        self._perform_query("relation/following_list", query_params, name="Following List")

    @task
    def tag_list(self):
        query_params = "page_size=10&page_number=1"
        self._perform_query("recipe/tags", query_params, name="Tag List")

    def _perform_login(self):
        """
        Perform the login operation to obtain the JWT token.
        """
        login_data = {
            "username": "<USER PHONENUMBER>",
            "password": "<USER PASSWORD>",
        }
        headers = {
            "accept": "application/json",
            "accept-language": "en",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        login_response = self.client.post("user/login/", name="Login", headers=headers, data=login_data)
        return login_response.json()

    def _perform_query(self, endpoint, query_params, name):
        headers = {"Accept": "application/json", "Accept-Language": "en", "Authorization": f"JWT {self.jwt_token}"}
        response = self.client.get(f"{endpoint}?{query_params}", name=name, headers=headers)
