from src.infra.errors import UserNameNotProvidedError, PasswordNotProvidedError, UserNameTypeError, \
    PasswordWithoutLettersError, PasswordWithoutNumbersError, InsufficientDataError, UserIdNotIntegerError, \
    PasswordTypeError, DatabaseError


class ErrorManager:
    """
    Class ErrorManager to handle all types of errors related to Repositories and Entities
    """
    @classmethod
    def validate_insert_user(cls, username, password):
        cls.__username_error(username)
        cls.__password_error(password)

    @classmethod
    def validate_select_user(cls, username, user_id):
        if not username and not user_id:
            raise InsufficientDataError('You must provide at least a UserName or a UserID')
        elif username and not isinstance(username, str):
            raise UserNameTypeError('Name type invalid. It must be alphabetic')
        elif user_id and not isinstance(user_id, int):
            raise UserIdNotIntegerError('User ID must be numeric')

    @classmethod
    def database_error(cls, message: any, code: any):
        raise DatabaseError(message, code)

    @classmethod
    def __username_error(cls, username):
        if not username:
            raise UserNameNotProvidedError(message='A username must be provided')
        elif not isinstance(username, str):
            raise UserNameTypeError('Name type invalid. It must be alphabetic')

    @classmethod
    def __password_error(cls, password):
        if not password:
            raise PasswordNotProvidedError('You must provide both Name and Password')
        elif isinstance(password, int):
            raise PasswordTypeError('Password must be string. Please verify')
        else:
            if password.isnumeric():
                raise PasswordWithoutLettersError('Password invalid. It must have letters to')
            elif password.isalpha():
                raise PasswordWithoutNumbersError('Password invalid. It must have numbers to')
