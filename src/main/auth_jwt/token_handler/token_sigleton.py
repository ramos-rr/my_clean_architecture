from decouple import config
from .token_generator import TokenGenerator
token_generator = TokenGenerator(
    token_key=config("TOKEN_KEY"),
    exp_time_min=config("TOKEN_EXPIRATION_MIN", cast=int),
    refresh_time_min=config("TOKEN_REFRESH_MIN", cast=int)
)
