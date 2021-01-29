log_title = lambda message: '\n'.join([
    '',
    '=' * (len(message) + 2),
    f' {message}',
    '=' * (len(message) + 2),
    '',
])

log_subtitle = lambda message: '\n'.join([
    '',
    f' {message}',
    '-' * (len(message) + 2),
    '',
])

log_error = lambda message: '\n'.join([
    '',
    '-' * (len(message) + 2 + 7),
     f' ERROR: {message}',
    '-' * (len(message) + 2 + 7),
    '',
])

log_success = lambda message: '\n'.join([
    '',
    '-' * (len(message) + 2 + 3),
     f' OK {message}',
    '-' * (len(message) + 2 + 3),
    '',
])
