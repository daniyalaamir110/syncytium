# Authentication App

This app is responsible for:

- ## User login
  Provides API enpoints to get access and refresh tokens, refresh to get a new access token, and verify a token using JWT simple auth.
- ## Google login
  Allows users to authenticate using their Google accounts. This feature provides API endpoints to handle the Google OAuth flow and obtain access and refresh tokens for the authenticated user.
- ## Password reset
  Provides API endpoints to reset the password if it's been forgotten, using the email.
- ## Current User
  Provided an API endpoint to get the currently logged in user by verifying the access token.
