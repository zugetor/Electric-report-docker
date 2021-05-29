import multiprocessing

# https://docs.gunicorn.org/en/stable/design.html
# Gunicorn recommend (2 x $num_cores) + 1
workers = multiprocessing.cpu_count()
# threads = multiprocessing.cpu_count()