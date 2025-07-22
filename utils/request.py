import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class request_call():
    Base_url="https://archive208.estuate.com:3051"

    def test_get_method(self, endpoint, headers=None, params=None):
        # Read token from file
        try:
            with open("utils/Auth.txt", "r", encoding="utf-8") as f:
                token = f.read().strip()
        except FileNotFoundError as exc:
            raise FileNotFoundError("Auth token not found. Run onboarding authentication test first.") from exc

        headers = headers or {"Authorization": token}
        url = f"{self.Base_url}/{endpoint}"
        get_response = requests.get(url=url, verify=False, headers=headers, params=params)
        return get_response

    
    def test_post_method(self,endpoint, json=None, headers=None,params=None):
        # Read token from file
        try:
            with open("utils/Auth.txt", "r", encoding="utf-8") as f:
                token = f.read().strip()                    
        except FileNotFoundError as exc:
            raise FileNotFoundError("Auth token not found. Run onboarding authentication test first.") from exc
        headers = headers or {"Authorization": token}
        url = f"{self.Base_url}/{endpoint}"
        post_response=requests.post(url=url,verify=False, json=json, headers=headers,params=params)
        return post_response