from django.core.validators import RegexValidator

NAME_VALIDATOR = RegexValidator(
    regex=r'^(?!.*[<>"\'\\\/]).+$',
    message="در نام از کاراکتر های \\ / <> \" ' استفاده نکنید",
    code="invalid_name",
)
USERNAME_VALIDATOR = RegexValidator(
    regex=r"^[a-zA-Z0-9_]+$",
    message='فقط از حروف کوچک و بزرگ اینگیلیسی، اعداد و "_" استفاده کنید',
    code="invalid_username",
)
