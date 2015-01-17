

AUTHENTICATION_BACKENDS = (
    'nopassword.backends.email.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)
