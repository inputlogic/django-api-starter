# Facebook Login

## Who is this for?:

This is for applications that use Facebook as a login and account creation tool.
End points and data flow:

1. facebook/url

Returns the URL for the Facebook login page. This is the URL that would be used
for the login button on the front end login page. Example return value:
https://www.facebook.com/v3.1/dialog/oauth?redirect_uri=https%3A%2F%2Ffront-end.com%2Fprocess-login&client_id=2291491961126343&scope=email

Once the user successfully logs in, Facebook will forward them to the URL specified in the
settings.FACEBOOK_SUCCESSFUL_LOGIN_URL. Note that this must match must match the URL specified in
the Facebook app login settings "Valid OAuth Redirect URIs".

Example redirect URL:
https://front-end.com/process-login?code=AQDFjv5Kq-yfn3LK-MDM9vLjXH7zDxWi5L3XgP0AxUyCWaFzsU2IJDTidpoHY4zXeBv7eKLMTc3HofxmJ7TC7j55Y_ZS1DXF1SLiRPVNJlwZRj7qelbRYKwHL00JgJgv37695nO8sFbvDsmqXoKj1aBoYFHQvq7QBvsXvMPZJwpBnrNms3YaYzkgtd50vWz2lh8sarAkcnQFrdECYVCtJfqROYd_QiBkHRokXoDO0UxKeODwoUv6SogY1qwyioA292nN7vzAp8WPQNyOcn9TSjhsa4GhbCl015W-cxt_QoJuQHb4mclxCEFfWDstqji1F38gnJCl33i7fzR7kqR3-8cy#_=_

2. facebook/token
