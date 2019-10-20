"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""

import traceback
import operator
from functools import reduce


def index():
    body = """
    <h1>ABOUT</h1>
    <p>Welcome!</p>
    <p>This is a calculator and we are out here calculating.</p>
    <ul>Ex usage:<ul>  
      <li>* <a href=http://localhost:8080/multiply/3/5> href=http://localhost:8080/multiply/3/5>=> 15</a></li>
      <li>* <a href=http://localhost:8080/add/23/42> http://localhost:8080/add/23/42=> 65</a></li>
      <li>* <a href=http://localhost:8080/subtract/23/42> http://localhost:8080/subtract/23/42=> -19</a></li>
      <li>* <a href=http://localhost:8080/divide/22/11> http://localhost:8080/divide/22/11=> 2</a></li>
    </ul>
    """
    return body


def add(*args):
    """Returns a string with the sum of the arguments"""
    nums = map(int, args)
    total = reduce(operator.add, nums)

    return str(total)


def subtract(*args):
    """Returns a string with the difference of the arguments"""
    nums = map(int, args)
    total = reduce(operator.sub, nums)

    return str(total)


def multiply(*args):
    """Returns a string with the product of the arguments"""
    nums = map(int, args)
    total = reduce(operator.mul, nums)

    return str(total)


def divide(*args):
    """Returns a string with the quotient of the arguments"""
    nums = map(int, args)

    try:
        total = reduce(operator.truediv, nums)

    except ZeroDivisionError:
        raise ZeroDivisionError

    return str(total)

# TODO: Add functions for handling more arithmetic operations.

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    funcs = {
        "": index,
        "add": add,
        "subtract": subtract,
        "multiply": multiply,
        "divide": divide
    }

    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1: ]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except ZeroDivisionError:
        status = "0 Zero Division Error"
        body = "<h1>Cannot Divide by Zero</h1>"
        print(traceback.format_exc())
    except Exception:
        status = "400 Bad Request"
        body = "<h1>You've Been Bad</h1>"
        print(traceback.format_exc())
    except ValueError:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

    # TODO: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    #
    # TODO (bonus): Add error handling for a user attempting
    # to divide by zero.
    

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
