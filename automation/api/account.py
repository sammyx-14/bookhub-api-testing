# api/account.py
# The "API layer" for the Account endpoints (/Account/v1/...).


class AccountAPI:
    def __init__(self, request):
        self.request = request

    def create_user(self, user_name, password):
        # POST /Account/v1/User  ->  registers a new user.
        return self.request.post(
            "/Account/v1/User",
            data={"userName": user_name, "password": password},
        )

    def generate_token(self, user_name, password):
        # POST /Account/v1/GenerateToken  ->  returns a token for that user.
        return self.request.post(
            "/Account/v1/GenerateToken",
            data={"userName": user_name, "password": password},
        )

    def delete_user(self, user_id, token):
        # DELETE /Account/v1/User/{UUID}  ->  needs the user's own token.
        return self.request.delete(
            f"/Account/v1/User/{user_id}",
            headers={"Authorization": f"Bearer {token}"},
        )