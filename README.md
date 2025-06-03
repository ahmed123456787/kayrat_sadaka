# Kayrat Sadaka

![Kayrat Sadaka Logo](https://t4.ftcdn.net/jpg/03/42/37/89/360_F_342378908_nzGSmdSNXXzaTcYBUrMMEmy1gdU7OSd2.jpg)

Kayrat Sadaka is a Django-based web application designed to manage and facilitate charity distributions for mosques. The platform allows administrators to manage resources, distributions, and needy individuals efficiently.

---

## Features

- 🧑‍💼 **User Management**: Custom user model with roles for mosque administrators and staff.
- 📦 **Resource Management**: Manage resources and their types (e.g., kilograms, liters, pieces).
- 🤝 **Distribution Management**: Track and manage charity distributions.
- 📝 **Needy Management**: Maintain records of needy individuals and their associated documents.
- 🔔 **Notifications**: Real-time notifications using WebSockets.
- 📖 **API Documentation**: Swagger and Redoc integration for API exploration.

---

## Prerequisites

Ensure you have the following installed on your system:

- 🐍 Python 3.10+
- 🐳 Docker and Docker Compose
- 🛠️ Redis (for WebSocket channels)
- 🗄️ PostgreSQL (for the database)

---

## Installation and Setup

Follow these steps to run the project locally:

### 1. Clone the Repository

```bash
$ git clone <repository-url>
$ cd kayrat_sadaka
```

### 2. Set Up Environment Variables

Create a `.env` file in the `backend` directory and add the following variables:

```
POSTGRES_DB=mydb
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password
```

### 3. Build and Run the Docker Containers

Navigate to the `backend` directory and run:

```bash
$ docker-compose up --build
```

This will set up the Django application, PostgreSQL database, and Redis server.

### 4. Apply Migrations

Run the following command to apply database migrations:

```bash
$ docker-compose exec web python manage.py migrate
```

### 5. Create a Superuser

Create an admin user to access the Django admin panel:

```bash
$ docker-compose exec web python manage.py createsuperuser
```

### 6. Access the Application

- 🌐 **API Endpoints**: `http://localhost:8000/api/v1/`
- 🔑 **Admin Panel**: `http://localhost:8000/admin/`
- 📜 **Swagger Documentation**: `http://localhost:8000/api/schema/swagger-ui/`
- 📘 **Redoc Documentation**: `http://localhost:8000/api/schema/redoc/`

---

## Project Structure

```
backend/
├── app/
│   ├── core/          # Core application logic (models, views, serializers)
│   ├── user/          # User management and authentication
│   ├── media/         # Uploaded files
│   ├── app/           # Project settings and configurations
│   └── manage.py      # Django management script
├── docker-compose.yaml
├── Dockerfile
└── requirements.txt
```

---

## Key Technologies

- **Backend**: Django, Django REST Framework
- **WebSockets**: Django Channels, Redis
- **Database**: PostgreSQL
- **Containerization**: Docker, Docker Compose

---

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
