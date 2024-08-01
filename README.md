
<br><h1 align="center">Hotel Booking App</h3>
<!-- USAGE EXAMPLES -->
## Usage

To run the web application, install the Poetry virtual environment, the necessary dependencies from pyproject.toml, populate the .env file as shown in .env.example, then perform alembic migrations using the commands "alembic init migrations", "alembic revision --autogenerate - m "Comment", "alembic upgrade head" and use the command "uvicorn main:app".

  
<!-- ABOUT THE PROJECT -->
## Project structure

admin/

    admin.py - admin settings.
    auth.py - authentication settings.

bookings/

    dao.py - DAO file for bookings.
    model.py - booking model.
    router.py - routing file.
    scheme.py - scheme for booking.

dao/

    base.py - base DAO file.

hotels/

    rooms/
           dao.py - DAO file for rooms.
           model.py - room model
           router.py - routing file.
           scheme.py - scheme for room.
    dao.py - DAO file for hotels.
    model.py - hotel model
    router.py - routing file.
    scheme.py - scheme for hotel.

images/

    router.py - routing file.

migrations/

    versions/ - folder contains the migration files.
    env.py - migration settings.

static/

    images/ - folder with images.

tasks/

    tasks.py - sending a message to the user by email.

templates/

    hotel_rooms.html - hotel rooms template.
    hotels.html - hotels page template.
    index.html - home page template.
    room.html - room page template.

users/

    auth.py - authentication settings.
    dao.py - DAO file for users.
    dependencies.py - 
    model.py - user model.
    router.py - routing file.
    scheme.py - scheme for user.

.env - environment variable file must be filled in.

.env.example - example of filling out a .env file.

.flake8 - file flake8.

.gitignore - GIT file.

alembic.ini - migration settings.

config.py - configuration file.

database.py - database file.

exceptions.py - exception handling.

main.py - application launch file.

poetry.lock - Poetry file.

pyproject.toml - necessary environmental dependencies.


<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.


<!-- CONTACT -->
## Contact

kettariec@gmail.com

https://github.com/Kettariec/booking_hotel_fastapi