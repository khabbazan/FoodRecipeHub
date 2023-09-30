from locust import HttpUser, task, between


class SIMLUser(HttpUser):
    """
    Load testing user for a REST API.

    Attributes:
        wait_time: A random wait time between 1 and 5 seconds before each task.

    Methods:
        on_start: Perform authentication to obtain the JWT token.
        user_list: Simulate fetching a user list from the API.
        recipe_list: Simulate fetching a recipe list from the API.
        follower_list: Simulate fetching a follower list from the API.
        following_list: Simulate fetching a following list from the API.
        tag_list: Simulate fetching a tag list from the API.
        _perform_login: Perform the login operation to obtain the JWT token.
        _perform_query: Perform a GET request to a specified API endpoint with query parameters.

    """

    wait_time = between(1, 5)

    def on_start(self):
        """
        Perform authentication to obtain the JWT token.
        This method is automatically called when a user starts. It performs the authentication
        process and stores the JWT token for use in APIs.
        """
        login_response = self._perform_login()
        self.jwt_token = login_response["access_token"]

    @task
    def user_list(self):
        """
        Simulate fetching a user list from the API.
        """
        query_params = "page_size=10&page_number=1"
        self._perform_query("user/list", query_params, name="User List")

    @task
    def recipe_list(self):
        """
        Simulate fetching a recipe list from the API.
        """
        query_params = "page_size=10&page_number=1"
        self._perform_query("recipe/list", query_params, name="Recipe List")

    @task
    def follower_list(self):
        """
        Simulate fetching a follower list from the API.
        """
        query_params = "page_size=10&page_number=1"
        self._perform_query("relation/follower_list", query_params, name="Follower List")

    @task
    def following_list(self):
        """
        Simulate fetching a following list from the API.
        """
        query_params = "page_size=10&page_number=1"
        self._perform_query("relation/following_list", query_params, name="Following List")

    @task
    def tag_list(self):
        """
        Simulate fetching a tag list from the API.
        """
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
        """
        Perform a GET request to a specified API endpoint with query parameters.
        """
        headers = {"Accept": "application/json", "Accept-Language": "en", "Authorization": f"JWT {self.jwt_token}"}
        self.client.get(f"{endpoint}?{query_params}", name=name, headers=headers)
