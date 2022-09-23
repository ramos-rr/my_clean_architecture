 s# my_clean_architecture
Repository based on the Clean Architecture book from Robert C Martin and YouTube classes from "programador Lhama"

## Check YouTube channel ["Programador Lhama"](https://www.youtube.com/watch?v=YAMgtR3aCuY&list=PLAgbpJQADBGJmTxeRZKWvdJAoJj8_x3si&index=1)

## Relation between classes<br>
<img src="images/relacao_usuario_pets.png" alt="relationship_classes" width="480" height=""><br>
- A User takes care of some Pets<br>
### Diagram of a spcific classe<br>
<img src="images/diagram_class.png" alt="class_diagram" width="300" height=""><br>
- Shows how a Class should behave to relate with other classes (Methods and Attributes)<br>
1. We've started setting up the `infra` to store our DB. For this project, we will just use sqlite throught sqlalchemy<br>
- CREATE: `infra/config/db_config.py`
- CREATE: `<db/config.py> class DbConnectionHandler` and follow the image 2.<br>
- CREATE: `infra/config/db_config.py` to tell sqlalchemy what is going to be inside DB and their relationship between them<br>
- CREATE: `<db_config.py> Base = declarative_base()` '(_from sqlalchemy.ext.declarative import declarative_base_)'.
This to awake DB.<br>
- EDIT: `<config/__init__.py>` and point what to export > `from .db_base import Base` and `from .db_config_py import 
DbConnectionHandler`<br><br>

- CREATE: `infra/entities/` to stablish the TABLE for the DB<br>
- CREATE: `infra/entities/pets.py` and `infra/entities/users.py` that are going to be the main actors in this project<br>
- CREATE: `<users.py> class Users(Base)`, importing Base from our `config`, and also import TABLE features from sqlalchemy,
such as Column, String, Integer<br>
- CREATE: `<pets.py> class Pets(Base)`, importing Base from our `config`, and also import TABLE features from sqlalchemy,
such as Column, String, Integer<br>
- EDIT: `<entities/__init__.py>` and point what to export > `from .pets import Pets` and `from .users import Users`<br><br>

- RUN TERMINAL:<br>
`$ python`<br> `>>> from src.infra.config import *` <br>`>>> from src.infra.entities import *` <br>
`# CHECK IF EVERYTHING HAS BEEN INSTATIATED`<br>
`>>> Base` <br> `<class 'sqlalchemy.orm.decl_api.Base'>` <br>
`>>> DbConnectionHandler` <br> `<class 'src.infra.config.db_config_py.DbConnectionHandler'>` <br>
`>>> Users`<br>`<class 'src.infra.entities.users.Users'>`<br>
`>>> Pets`<br>`<class 'src.infra.entities.pets.Pets'>`<br>
`# EVERYTHING SEEMS TO BE FINE. CONTINUING...`<br>
` >>> db_conn = DbConnectionHandler()`<br>
`# CHECK OBJECT DB_CONN`<br>
`>>> db_conn` <br> `<src.infra.config.db_config_py.DbConnectionHandler object at 0x000001FC4303F730>`<br>
`# CALL ENGINE TO PUT PARTS TOGETHER`<br>
`>>> engine = db_conn.get_engine()`<br> `>>> engine`<br> 
`Engine(sqlite:///storage.db)`<br>
`# COMMAND THE CREATION OF THE FILE SQLITE DB`<br>
`>>> Base.metadata.create_all(engine)`<br>
<br>

- SEE: `storage.db` must have been created in your project's root

### TIP to create and manage DB FROM SQLALCHEMY:<br>
1. When stablishing a connection, you have to set up a ENGINE:<br>
2. Define a SESSION, which is NONE initially, but recieves a value after started<br>
3. Define _ _ enter _ _() and _ _ exit _ _() methods to set up a session every time the class 
is called, ado close in the end
<br>

```
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DbConnectionHandler:

    def __init__(self):
        self.__connection_string = "sqlite:///storage.db"  # This string is need by sqlalchemy
        self.session = None

    def get_engine(self):
        """
        Create a connection to DB
        :return: connection engine
        """
        engine = create_engine(self.__connection_string)
        return engine

    # Define a method to enter DB to garantee some levels of security
    def __enter__(self):
        engine = create_engine(self.__connection_string)
        session_maker = sessionmaker()
        self.session = session_maker(bind=engine)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
```
<br>

5. Finally, when introducing new data in DB, call `session` and one of this four commands:
- <connection_name>.session.add( <new_data> )<br>
- <connection_name>.session.commit()<br>
- <connection_name>.session.rollback()<br>
- <connection_name>.session.close()<br>
- OBS: generally, this features are used with <b>try / finally</b> resource<br>
<br>
## CREATING A USERREPOSITORY AND PETREPOSITORY CLASS<br>
<img src="images/user_repository_diagram.png" alt="user_repository_diagram" width="400" height=""><br>
- Now it is time to set up a USER REPOSITORY and a PET REPOSITORY CLASS that will call both entities and
database as desired:

