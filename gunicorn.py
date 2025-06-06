bind = '127.0.0.1:5001'  # Bind IP and port number

workers = 1  # Number of worker processes
threads = 2  # Number of threads per worker process
# Log level (for error logs; access log level cannot be set here)
loglevel = 'debug'
accesslog = "/home/ubuntu/questionnaire/log/gunicorn_access.log"  # Access log file
errorlog = "/home/ubuntu/questionnaire/log/gunicorn_error.log"  # Error log file
