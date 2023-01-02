# cihi_posts

# app
    React front end to allow a CIHI admin to log in to the app with Facebook and stores an access token in Secrets Manager.

# backend
## TokenSet
    AWS lambda as back end service for validating and storing a CIHI admin user's token to be used by the app.
## SendEmail
    AWS lambda run on a cron throughout the weekend to pull the CIHI posts with the cached admin user's token and send the posts as an email to all subscribers.
