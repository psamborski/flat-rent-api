# **Flat Rent API**

This project is designed to manage flat rentals by providing access to an API for managing cities, amenities, and flats.

---

## **Features**

- Manage cities, flats, and amenities data.
- Preloaded static data for quick and easy exposure.
- Designed for running with Docker but also supports standalone execution.

---

## **Technologies and prerequisites**

- Python 3.9 and Fast API installed locally (if using the manual setup option).
- PostgreSQL and SQLAlchemy for DB management.
- Docker and Docker Compose installed on your system.
- Dependencies specified in `requirements.txt` (for manual setup).

---
## **API Endpoints**
### **Flats**
- **Get all flats**  
  `GET /flats/`  
  **Response**:  
  ```json
  [
    {
      "id": 1,
      "title": "Cozy Apartment",
      "description": "A modern apartment in the city center.",
      "address": "ul. Marszałkowska M/N",
      "coordinates": "POINT(21.0122 52.2297)",
      "floor": 3,
      "rooms_number": 2,
      "square": 55.0,
      "price": 3500.0,
      "currency": "PLN",
      "city_id": 1
    }
  ]
  ```

- **Get a flat by ID**  
  `GET /flats/{flat_id}`  
  **Response**:  
  ```json
  {
    "id": 1,
    "title": "Cozy Apartment",
    "description": "A modern apartment in the city center.",
    "address": "ul. Marszałkowska M/N",
    "coordinates": "POINT(21.0122 52.2297)",
    "floor": 3,
    "rooms_number": 2,
    "square": 55.0,
    "price": 3500.0,
    "currency": "PLN",
    "city_id": 1
  }
  ```

- **Create a new flat**  
  `POST /flats/`  
  **Request Body**:  
  ```json
  {
    "title": "Cozy Apartment",
    "description": "A modern apartment in the city center.",
    "address": "ul. Marszałkowska M/N",
    "latitude": 52.2297,
    "longitude": 21.0122,
    "floor": 3,
    "rooms_number": 2,
    "square": 55.0,
    "price": 3500.0,
    "currency": "PLN",
    "city_id": 1,
    "amenities_ids": [1, 2]
  }
  ```  
  **Response**:  
  ```json
  {
    "id": 1,
    "title": "Cozy Apartment",
    "description": "A modern apartment in the city center.",
    "address": "ul. Marszałkowska M/N",
    "coordinates": "POINT(21.0122 52.2297)",
    "floor": 3,
    "rooms_number": 2,
    "square": 55.0,
    "price": 3500.0,
    "currency": "PLN",
    "city_id": 1
  }
  ```
  
---

### **Cities**
- **Create a new city**  
  `POST /cities/`  
  **Request Body**:  
  ```json
  {
    "name": "Warsaw",
    "country": "Poland"
  }
  ```  
  **Response**:  
  ```json
  {
    "id": 1,
    "name": "Warsaw",
    "country": "Poland"
  }
  ```

---

### **Amenities**
- **Create a new amenity**  
  `POST /amenities/`  
  **Request Body**:  
  ```json
  {
    "name": "Underground parking"
  }
  ```  
  **Response**:  
  ```json
  {
    "id": 1,
    "name": "Underground parking"
  }
  ```

---

## **Installation**

### **Clone the repository:**
   ```bash
   git clone https://github.com/psamborski/flat-rent-api.git
   ```

### **Option 1: Run the application directly using `docker-compose`**

1. Build and run the application:
   ```bash
   docker-compose up --build
   ```

2. Once the application is running, you can start using the API.

---

### **Option 2: Run the application manually without the `db-init` service**

If you don't want to use an additional container for database initialization, follow these steps:

1. Start the database:
   ```bash
   docker-compose up -d db
   ```

2. Wait for the database to initialize. To check the database status, run:
   ```bash
   docker-compose logs db
   ```

3. Once the database is ready, create the schema and tables by running:
   ```bash
   python -m scripts.create_db
   ```

4. Start the application:
   ```bash
   docker-compose up -d app
   ```

### **Option 3: Run the application locally**

1. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create database:
   ```bash
   python -m scripts.create_db
   ```

3. Run the FastAPI application:
   ```bash
   uvicorn main:app --reload
   ```

### Where is it?
The API will be available at: `http://127.0.0.1:8000`


---

## **Database Schema**

The database uses the `flat_rent_api` schema and consists of the following tables:

### **1. `cities`**
Stores information about cities.

| Column   | Type    | Description          |
|----------|---------|----------------------|
| `id`     | Integer | Primary key          |
| `name`   | String  | Name of the city     |
| `country`| String  | Country of the city  |

### **2. `amenities`**
Stores information about amenities.

| Column   | Type    | Description          |
|----------|---------|----------------------|
| `id`     | Integer | Primary key          |
| `name`   | String  | Name of the amenity  |

### **3. `flats`**
Stores information about flats.

| Column         | Type          | Description                          |
|----------------|---------------|--------------------------------------|
| `id`           | Integer       | Primary key                          |
| `title`        | String        | Title of the flat                    |
| `description`  | String        | Description of the flat              |
| `address`      | String        | Address of the flat                  |
| `coordinates`  | Geography     | Coordinates of the flat (POINT)      |
| `floor`        | Integer       | Floor number                         |
| `rooms_number` | Integer       | Number of rooms                      |
| `square`       | Float         | Size of the flat in square meters    |
| `price`        | Float         | Price per month                      |
| `currency`     | String        | Currency (default: PLN)              |
| `city_id`      | Integer       | Foreign key to `cities.id`           |

### **4. `flat_amenities`**
Represents a many-to-many relationship between flats and amenities.

| Column       | Type    | Description                          |
|--------------|---------|--------------------------------------|
| `flat_id`    | Integer | Foreign key to `flats.id`            |
| `amenity_id` | Integer | Foreign key to `amenities.id`        |

---

## **Notes**

- The `create_db` script is responsible for setting up the database schema and tables. It's designed to handle schema isolation and ensures tables are created without conflicts.
- The `load_data_from_json` functionality depends on properly structured JSON file. Check `static_data` directory for the file. You can also scrap address by coordinates with `get_flat_addresses.py` in `scripts`.
