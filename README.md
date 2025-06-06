# User Questionnaire Backend

## Overview

This project is the backend service for a questionnaire application. It handles questionnaire creation, submission, data storage, and analysis.

## Server-side

- **Database**: The backend uses **MongoDB**, a NoSQL database. While MySQL is also a viable option, MongoDB was chosen for its flexibility in data insertion.
  - **Data Handling**: For questionnaire submissions, data insertion into MongoDB is straightforward. However, for robustness, data format validation should be considered. If using MySQL with JSON fields, handling would also be manageable.
  - **Data Statistics**:
    - **Current Approach**: The project currently calculates statistics by querying the database directly upon API request. This is acceptable for small-scale personal projects.
    - **Scalability Concerns**: For larger datasets or questionnaires with many questions, this direct query and computation method can be time-consuming.
    - **Proposed Improvements**:
      1. **Redis Caching**: After a user submits a form and the server responds with a 200 status, the backend could asynchronously recalculate the form's statistical information. This data would then be stored in both Redis and the database. When a questionnaire publisher requests data analysis, statistics can be quickly retrieved from Redis.
      2. **Dedicated Statistics Table**: An alternative to Redis could be a separate table for storing aggregated statistics. Each time a user submits a form, this table would be updated. This avoids querying multiple tables for calculations. However, maintaining data consistency could be challenging. For instance, if a questionnaire publisher modifies or deletes a question or changes option order, the statistics table would need complex updates.

## Front-end

- **Future Enhancements**:
  - Develop a **form editor component** based on the current frontend. By defining a clear data structure, this editor could support not only questionnaires but also exams, business form processing, and more.
  - Plan to adopt **Vue 3** and **TypeScript**.

## Project Structure

```bash
flask_backend_user_authentication/
├── app/                # Contains the main application logic
├── config/             # Configuration files for the project
├── database/           # Database-related files and migrations
├── static/             # Static assets like CSS, JS, and images
├── templates/          # HTML templates for rendering views
├── tests/              # Unit tests and integration tests
├── venv/               # Virtual environment for Python dependencies
├── docker/             # Docker-related files (e.g., Dockerfile, docker-compose)
├── logs/               # Log files for debugging and monitoring
├── README.md            # Documentation for the project, including setup, features, and deployment instructions.
├── requirements.txt     # Lists Python dependencies required for the project.
├── Dockerfile           # Defines the instructions to build a Docker image for the project.
├── gunicorn.py          # Configuration file for Gunicorn, the Python WSGI HTTP server.
├── manage.py            # Entry point for managing the Flask application (e.g., running the server, migrations).
```

## Installation (Development Environment)

### Clone the Project

```bash
git clone https://github.com/e-choness/user-questionaire.git
```

### Navigate to Project Directory

```bash
cd /user-questionnaire-backend # e.g., or your customized root directory
```

### Create a Virtual Environment

```bash
virtualenv venv
```

### Activate the Virtual Environment

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Common Issues

- If Flask's debug mode is enabled in the development environment, scheduled tasks might not run.

## Features

- **User Management**: Login, registration, email verification, and other basic user operations.
- **Questionnaire Creation**: Create questionnaires for data collection (Supported question types: single choice, multiple choice, fill-in-the-blank, dropdown).
- **Questionnaire Management**: CRUD operations for your questionnaires; supports generating questionnaires from templates.
- **Questionnaire Publishing**: Basic publish/unpublish functions, set questionnaire passwords, restrict access by IP or device to prevent repeat submissions.
- **Data Analysis**: Visualize and analyze data collected from questionnaires.

## Deploying on Docker

### Install Docker

```bash
sudo yum install docker
```

### Build the Image

Build an image from the local Dockerfile. Navigate to the project's root directory and execute:

```bash
docker build -t questionnaire:1.0
```

Here, `questionnaire` is the image name, and `1.0` is the version number. You can customize these.

### Run the Container

```bash
docker run -p 8080:5001 questionnaire:1.0
```

This command maps port 5001 (exposed by the container) to port 8080 on your host server.

### Test Deployment

Access port 8080 on your server. If you receive the following JSON response, the deployment is successful:

```json
{
  "errorCode": 0,
  "message": "Your project is running successfully!"
}
```

## Dockerfile

The following Dockerfile is located in the project root directory. It's used to package the project into an image and generally does not need modification:

```dockerfile
FROM python:3.8
COPY . .
WORKDIR .
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install gunicorn -i https://pypi.tuna.tsinghua.edu.cn/simple
CMD ["gunicorn", "-c", "gunicorn.py", "manage:app"]
EXPOSE 5001
```

## Gunicorn Configuration

The Gunicorn configuration file (`gunicorn.py`) is located in the project root directory:

```python
bind = '127.0.0.1:5001'  # Bind IP and port number

workers = 1  # Number of worker processes
threads = 2  # Number of threads per worker process
loglevel = 'debug'  # Log level (for error logs; access log level cannot be set here)
accesslog = "/home/ubuntu/questionnaire/log/gunicorn_access.log"  # Access log file
errorlog = "/home/ubuntu/questionnaire/log/gunicorn_error.log"  # Error log file
```

## Nginx Forwarding

After the steps above, the project is deployed in a Docker container on port 5001, which is then mapped to the server's port 8080. You can use Nginx for reverse proxying.

### Create an Nginx Configuration File

Create an Nginx configuration file (e.g., `questionnaire.conf`) in your project's root directory or `/etc/nginx/sites-available/`:

```nginx
server {
    listen       80;
    server_name  api.yourdomain.com; # Replace with your domain
    location / {
        proxy_pass http://127.0.0.1:8080; # Or 5001 if not remapped by Docker run command
        proxy_redirect off;
        proxy_set_header Host $host; # If using port 80, $host:80 is not needed
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### Modify Nginx Configuration

Find your Nginx installation directory and modify `nginx.conf`. Locate the `http` block and add an `include` statement for your site configuration:

```nginx
http {
    # ... other configurations ...

    ##
    # Virtual Host Configs
    ##

    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
    # Add the line below, pointing to your project's Nginx config file
    # For example, if you placed questionnaire.conf in /etc/nginx/sites-enabled/
    # and created a symlink from /etc/nginx/sites-available/
    # include /etc/nginx/sites-enabled/questionnaire.conf;
    # Or, if you placed it directly:
    # include /home/ubuntu/questionnaire/questionnaire.conf;
}
```

### Reload Nginx

Remember to reload or restart Nginx for changes to take effect:

```bash
sudo systemctl reload nginx
```

## Contributing

Feel free to contribute to this project by submitting issues or pull requests.

## License

This project is licensed under the MIT License.

## Contact

For questions or support, contact [here](mailto:echoybl1123@gmail.com).
