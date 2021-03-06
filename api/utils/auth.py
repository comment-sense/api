from flask import url_for, redirect, session, request, jsonify
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery


def credentials_to_dict(credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }


def authorize(secretes=None, _scopes=None):
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        secretes, scope=_scopes
    )

    # The URI created here must exactly match one of the authorized redirect URIs
    # for the OAuth 2.0 client, which you configured in the API Console. If this
    # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
    # error.
    flow.redirect_uri = url_for("oauth2callback", _external=True)

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type="offline",
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes="true",
    )

    session["state"] = state

    return redirect(authorization_url)


def oauth2callback(secrets=None, _scopes=None):
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = session["state"]

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        secrets, scopes=_scopes, state=state
    )
    flow.redirect_uri = url_for("oauth2callback", _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    session["credentials"] = credentials_to_dict(credentials)

    return redirect(url_for("test_api_request"))


def test_api_request(service_name="youtube", api_version=3):
    if "credentials" not in session:
        return redirect("authorize")

    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(**session["credentials"])

    drive = googleapiclient.discovery.build(
        service_name, api_version, credentials=credentials
    )

    files = drive.files().list().execute()

    # Save credentials back to session in case access token was refreshed.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    session["credentials"] = credentials_to_dict(credentials)

    return jsonify(**files)
