
@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def auth_facebook(request):
    try:
        # Retrieve `code` from POST first, otherwise GET (query param)
        code = request.data.get('code', request.query_params.get('code'))

        # 1. Exchange code for token
        token_response = requests.get('https://graph.facebook.com/v8.0/oauth/access_token', params={
            'client_id': settings.FACEBOOK_CLIENT_ID,
            'redirect_uri': settings.FACEBOOK_REDIRECT,
            'client_secret': settings.FACEBOOK_SECRET,
            'code': code,
        })

        if token_response.status_code != 200:
            log.error('failed to acquire facebook token: {0}'.format(token_response.text))
            raise ParseError(detail=token_response.text)

        access_token = token_response.json()['access_token']

        # 2. Use token, to get facebook profile data
        info_response = requests.get('https://graph.facebook.com/v8.0/me', params={
            'fields': 'id,name,email',
            'access_token': access_token
        })

        if info_response.status_code != 200:
            log.error('failed to acquire facebook token: {0}'.format(info_response.text))
            raise ParseError(detail=info_response.text)

        # 3. Use info to authorize with our app
        info = info_response.json()
        social, created = SocialAuth.login_or_signup(provider='facebook', access_token, info)
        response_code = 201 if created else 200
        login_token, _ = Token.objects.get_or_create(user=social.user)

        return Response({
            'token': login_token.key,
            'user_id': social.user.id
        }, status=response_code)
    except KeyError as e:
        log.exception(e)
        raise ParseError(detail='missing "code" argument')
