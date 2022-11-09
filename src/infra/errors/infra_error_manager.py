from src.infra.errors import UserNameNotProvidedError, PasswordNotProvidedError, UserNameTypeError, \
    PasswordWithoutLettersError, PasswordWithoutNumbersError, InsufficientDataError, UserIdNotIntegerError, \
    PasswordTypeError, DatabaseError, UserIdNotProvidedError, NoResultFoundError, IntegrityError
from src.infra.errors.pets_errors import PetNameNotProvidedError, PetNameTypeError, SpecieNotProvidedError,\
    SpecieNotAllowedError, SpecieTypeError, AgeNotIntegerError, PetIdNotIntegerError


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
        elif username:
            if not isinstance(username, str):
                raise UserNameTypeError('Name type invalid. It must be alphabetic')
        else:
            cls.__user_id_error(user_id=user_id)

    @classmethod
    def validate_insert_pet(cls, petname, specie, age, user_id):
        cls.__petname_error(petname)
        cls.__specie_error(specie)
        cls.__age_error(age)
        cls.__user_id_error(user_id)

    @classmethod
    def validate_select_pet(cls, pet_id, user_id):
        if not pet_id and not user_id:
            raise InsufficientDataError('You must provide at least a PetID or a UserID')
        elif pet_id and not user_id:
            cls.__pet_id_error(pet_id)
        elif user_id and not pet_id:
            cls.__user_id_error(user_id)
        else:
            cls.__pet_id_error(pet_id)
            cls.__user_id_error(user_id)

    @classmethod
    # def database_error(cls, error_type: any = None, message: any = None, code: any = None):
    #     if not error_type:
    #         raise DatabaseError(message, code)
    #     if error_type:
    #         if error_type == 'NoResultFound':
    #             raise NoResultFoundError(message, code)
    def database_error(cls, error):

        error_type = str(type(error))
        sep = error_type.rfind('.')
        error_type = error_type[sep + 1:-2]

        try:
            message = str(error.args[0])
        except:
            message = error.args

        try:
            code = error.__getattribute__("code")
        except:
            code = None

        if error_type == 'NoResultFound' or error_type == 'NoResultFoundError':
            raise NoResultFoundError(message=message, code=code)
        if error_type == 'IntegrityError':
            raise IntegrityError(message=message, code=code)
        else:
            raise DatabaseError(message=message, code=code)

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

    @classmethod
    def __petname_error(cls, petname):
        if not petname:
            raise PetNameNotProvidedError(message='A petname must be provided')
        elif not isinstance(petname, str):
            raise PetNameTypeError('Name type invalid. It must be alphabetic')

    @classmethod
    def __specie_error(cls, specie):
        from src.infra.entities.pets import AnimalTypes
        if not specie:
            raise SpecieNotProvidedError(message='A specie must be provided')
        elif not isinstance(specie, str):
            raise SpecieTypeError('Specie type invalid. It must be alphabetic')
        elif specie not in AnimalTypes._member_names_:
            raise SpecieNotAllowedError(message='The specie informed is not allowed because it is not in the list. '
                                                f'Species supported: {AnimalTypes._member_names_}')

    @classmethod
    def __age_error(cls, age):
        if not isinstance(age, int):
            raise AgeNotIntegerError(message='Age must be integer. Please check')

    @classmethod
    def __user_id_error(cls, user_id):
        if not user_id:
            raise UserIdNotProvidedError(message='You must provide a User ID to serve as pet owner')
        else:
            if not isinstance(user_id, int):
                raise UserIdNotIntegerError('User ID must be numeric')

    @classmethod
    def __pet_id_error(cls, pet_id):
        if not isinstance(pet_id, int):
            raise PetIdNotIntegerError('Pet ID must be numeric')
