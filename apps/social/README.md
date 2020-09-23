# Facebook Login

## Who is this for?:

This is for applications that use Facebook as a login and account creation tool.

There is a Facebook application for testing login. This MUST be replaced with the client's
Facebook application for production.

Test Facebook App "Django Starter Login"
https://developers.facebook.com/apps/2291491961126343/dashboard/:

Test User for Facebook App "Django Starter Login"
email: django_bpcqhdj_fett@tfbnw.net
password: SuperDuper123

There are four end points that exist in an attempt to make the Facebook login and user creation
process as robust as possible.

End points:

1. facebook/url

Returns the URL for the Facebook login page. This is the URL that would be used for the login button
on the front end login page.

Example return value:
https://www.facebook.com/v3.1/dialog/oauth?redirect_uri=https%3A%2F%2Ffront-end.com%2Fprocess-login&client_id=2291491961126343&scope=email

The user clicks the button and, once the user successfully logs in on the Facebook side, Facebook
will forward them to the URL specified in the settings.FACEBOOK_SUCCESSFUL_LOGIN_URL. Note that this
URL must match the URL specified in the Facebook app login settings "Valid OAuth Redirect URIs".
See https://developers.facebook.com/apps/2291491961126343/dashboard/ for an example (Ask Gavin for
access).

Example redirect URL after successful login:
https://front-end.com/process-login?code=AQDFjv5Kq-yfn3LK-MDM9vLjXH7zDxWi5L3XgP0AxUyCWaFzsU2IJDTidpoHY4zXeBv7eKLMTc3HofxmJ7TC7j55Y_ZS1DXF1SLiRPVNJlwZRj7qelbRYKwHL00JgJgv37695nO8sFbvDsmqXoKj1aBoYFHQvq7QBvsXvMPZJwpBnrNms3YaYzkgtd50vWz2lh8sarAkcnQFrdECYVCtJfqROYd_QiBkHRokXoDO0UxKeODwoUv6SogY1qwyioA292nN7vzAp8WPQNyOcn9TSjhsa4GhbCl015W-cxt_QoJuQHb4mclxCEFfWDstqji1F38gnJCl33i7fzR7kqR3-8cy#_=_

2. facebook/authcode/fb-token

Login a user using the Facebook auth code.

Returns an access token in exchange for a Facebook auth code. Creates the user if they don't exist.
The user is created with the email address that is associated with the Facebook account for the
auth code.

The Facebook auth code is returned by the redirect URL above. Example:

code=AQDFjv5Kq-yfn3LK-MDM9vLjXH7zDxWi5L3XgP0AxUyCWaFzsU2IJDTidpoHY4zXeBv7eKLMTc3HofxmJ7TC7j55Y_ZS1DXF1SLiRPVNJlwZRj7qelbRYKwHL00JgJgv37695nO8sFbvDsmqXoKj1aBoYFHQvq7QBvsXvMPZJwpBnrNms3YaYzkgtd50vWz2lh8sarAkcnQFrdECYVCtJfqROYd_QiBkHRokXoDO0UxKeODwoUv6SogY1qwyioA292nN7vzAp8WPQNyOcn9TSjhsa4GhbCl015W-cxt_QoJuQHb4mclxCEFfWDstqji1F38gnJCl33i7fzR7kqR3-8cy

**Note on the next two endpoints. The next two endpoints split the previous endpoint into two steps.

The regular data flow is:
Facebook auth code -> Facebook user token -> Django access token

The facebook/authcode/token endpoint allows for the data flow:
Facebook auth code -> Django access token

This is because the endpoint logic handles the Facebook user token exchange behind the scenes.

If there is use a case where the Facebook user token is required, or there is need to split
the login steps, these endpoints allow for it.

3. /facebook/authcode/fb-token

Return the Facebook user token in exchange for a Facebook auth code.

4. /facebook/fb-token/token

Login a user using a Facebook user token.

Returns an access token in exchange for a Facebook user token. Creates the user if they don't exist.
The user is created with the email address that is associated with the Facebook account for the
Facebook user token.


# Google Login

## Who is this for?:

This is for applications that use Google (gmail) as a login and account creation tool.

Google docs: https://developers.google.com/api-client-library/python/auth/web-app

There is a Googe application for testing login. This MUST be replaced with the client's
Google application for production.

Test Google App "Django Starter Login"
https://console.developers.google.com/apis/library?project=django-starter-login&authuser=1&organizationId=726546110496

Keys:
https://console.developers.google.com/apis/credentials?authuser=1&organizationId=726546110496&project=django-starter-login

Authorized domains: https://console.developers.google.com/apis/credentials/consent?project=django-logon&authuser=1&organizationId=726546110496

To do - complete Google specific dataflow. It is nearly identical to the Facebook dataflow above.
