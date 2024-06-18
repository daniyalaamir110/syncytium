# Accounts App

This app is responsible for:

- ## User registration
  Provides API endpoint to register a new user, thereby sending a welcome email and a verification email.
- ## User's email updation and verification
  Provides API endpoints for changing email, or generating a verification link. Both the endpoints send an email to the user's email address with a verification link, accessing which verifies the email, if the link is valid or token hasn't expired.
- ## User's profile, address, education, work experience
  Provides API endpoints to get user's mentioned details. However, for other users, the access is restricted as per the user's privacy settings.
- ## User's privacy
  Provides API endpoints to get or update one's privacy settings.
