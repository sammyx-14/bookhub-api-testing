# api/account.py
# The "API layer" for the Account endpoints (/Account/v1/...).


class AccountAPI:
    def __init__(self, request):
        self.request = request

    def create_user(self, user_name, password=None):
        # POST /Account/v1/User  ->  registers a new user.
        # `password=None` leaves the field out, so a test can send an incomplete body.
        body = {"userName": user_name}
        if password is not None:
            body["password"] = password
        return self.request.post("/Account/v1/User", data=body)

    def generate_token(self, user_name, password):
        # POST /Account/v1/GenerateToken  ->  returns a token for that user.
        return self.request.post(
            "/Account/v1/GenerateToken",
            data={"userName": user_name, "password": password},
        )

    def authorize(self, user_name, password):
        # POST /Account/v1/Authorized  ->  checks credentials, answers true or an error.
        return self.request.post(
            "/Account/v1/Authorized",
            data={"userName": user_name, "password": password},
        )

    def get_user(self, user_id, token=None):
        # GET /Account/v1/User/{UUID}  ->  details of one user. Needs that user's token.
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        return self.request.get(f"/Account/v1/User/{user_id}", headers=headers)

    def delete_user(self, user_id, token):
        # DELETE /Account/v1/User/{UUID}  ->  needs the user's own token.
        return self.request.delete(
            f"/Account/v1/User/{user_id}",
            headers={"Authorization": f"Bearer {token}"},
        )