San Francisco Food Truck Finder
===============================

Unleash your inner foodie and discover the best food trucks in San Francisco!
-----------------------------------------------------------------------------

This project empowers you to navigate the vibrant food truck scene of San Francisco with ease. Find delicious meals on wheels wherever you roam, whether you're craving a specific cuisine or simply want to explore nearby options.


Features:
---------

*   **Interactive Map View:** Visually pinpoint the locations of at least 5 food trucks closest to you. Explore all registered food trucks on a comprehensive map. (Implemented)
*   **Complete Food Truck Listing:** Browse a comprehensive list of all registered food trucks in San Francisco with details like cuisine type and location.
*   **Filter by Category:** Refine your search by selecting your preferred cuisine (e.g., Mexican, Thai, BBQ). Find exactly what your taste buds desire! (Implemented)
*   **Admin Panel:** Empower authorized users to upload and manage food truck data, ensuring the information remains up-to-date. (Implemented)

Technologies Used:
------------------

*   Python (3.x)
*   Django Web Framework
*   Django REST Framework (for a more robust API)
*   Leaflet.js (for interactive maps)
*   Tailwind CSS (for rapid UI development)

Fuctionality:
-------------------

This project highlights proficiency in building full-fledged Django web applications with a focus on:

*   **API Development:** Providing a robust API for data access and manipulation.
*   **Interactive User Interface:** Creating a visually appealing and user-friendly experience with Leaflet.js and Tailwind CSS.
*   **Data Management:** Implementing an admin panel for authorized users to upload and manage food truck data.

Getting Started:
----------------

### 1.Clone the Repository:

    git clone https://github.com/Misganaw-Berihun/san-francisco-food-trucks.git

### 2.Install Dependencies:

    pip install -r requirements.txt

### 3.Run Migrations:

    python manage.py migrate

### 4.Create Admin User:

    python manage.py createsuperuser

This command will prompt you to enter a username, email address, and a strong password. These credentials will be used to log in to the admin panel.

### Run the Development Server:

    python manage.py runserver

### Login as Admin and Upload Data

#### Open Admin Panel:

Navigate to [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) in your web browser.

#### Login:

Enter the username and password you created in step 4 to log in to the Django admin panel.

#### Upload Food Truck Data:

*   1.Click on the "csv datas" link in the admin panel sidebar.
*   2.Click on the "upload csv" button.
*   3.Choose the csv file that includes the data
*   4.Click the "upload" button to add the data to the database.
*   5.Naviagate to [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/) in your web browser

#### Video Demo
<div>
    <a href="https://www.loom.com/share/41cb26a6928249949a257e34405c04b5">
      <p>Library | Loom - 10 June 2024 - Watch Video</p>
    </a>
    <a href="https://www.loom.com/share/41cb26a6928249949a257e34405c04b5">
      <img style="max-width:300px;" src="https://cdn.loom.com/sessions/thumbnails/41cb26a6928249949a257e34405c04b5-with-play.gif">
    </a>
  </div>

#### Deployement

* **Renderurl**: https://food-truck-finder-8h2u.onrender.com
* **NB**: By default, the deployed application creates a superuser account with the following credentials:

    * **Username:** admin
    * **Password:** adminpassword

License
-------

This project is licensed under the MIT License. See the LICENSE file for details.
