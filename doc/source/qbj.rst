The *Query By JSON* (QBJ) Language
==================================

**Query By JSON** (QBJ) comes up from the need of Yatel to provide an agnostic
query language for NW-OLAP (OLAP Multidimensional Networks).


Features
--------

- Declarative.
- Strong typing.
- Design based on JSON given its wide diffusion in Python (language used to 
  implement Yatel).
- For parsing the data types we use the ``yatel.typeconv`` module that is also
  exploited in the export and import features of Yatel.
- Prior to parsing QBJ queries are validated with json-schema_ to avoid
  unnecessary calculations.
- Considered a Low-level language.


Syntax: Query and Query returns
-------------------------------

Let's start with an example of the simplest QBJ function, `ping`

The purpose of the function `ping` is simply a response without content
indicating that Yatel is listening to our queries.

#. **Simple query**

    .. code-block:: javascript

        {
            "id": "123",
            "function": {
                "name": "ping",
                "args": [],
                "kwargs": {}
            }
        }

    - ``id`` is a query identifier. It can be an integer or a string or null.
      This value will be returned in the query response. If you are processing
      it asynchronously you can use this field to discriminate processing.
    - ``function`` is the second, and final, mandatory key in the query. It
      consists of the query itself to be validated and implemented, which has
      its own various keys.

        - ``name`` the name of the function to be executed, in this case `ping`
        - ``args`` are positional arguments of the function. In this case
          `ping` does not have any parameter with which all of the key and
          the value can be avoided.
        - ``kwargs`` are named parameters of the function and being empty
          can be avoided as well.

    Removing the unnecessary parameters the function could be written

    .. code-block:: javascript

        {
            'id': '123',
            'function': {
                'name': 'ping'
            }
        }

    The answer to this query has the form:

    .. code-block:: javascript

        {
            'id': '123',
            'error': false,
            'error_msg': '',
            'stack_trace': null,
            'result': {
                'type': 'bool',
                'value': true
            }
        }

    Where:

    - ``id`` is the same id from the query.
    - ``error`` it's a Boolean value,  will be false while the query
      is processed successfully.
    - ``error_msg`` if the ``error`` value it is true this key will contain
      a description of the error that occurred.
    - ``stack_trace`` if the ``error`` value it is true and the query is 
      run in debug mode contains all the sequences of calls when the error 
      happened.
    - ``result`` always **null** if the ``error`` value  true. On the other
      hand if no error happened ``result`` has the resulting value of the
      function (in our `ping`) which is in format ``yatel.typeconv`` and
      indicates that the result is of boolean type and its value is true.

    In summary our example simply says that no error happened and as a results
    a Boolean value of true is returned.

#. **A query with errors**

    Suppose the call to a nonexistent function to see a result of
    a query with errors.

    .. code-block:: javascript

        {
            "id": 31221220,
            "function": {
                "name": "fail!",
            }
        }

    In QBJ the function **fail!** Does not exist, therefore the result would
    be if we run it in debug mode the following

    .. code-block:: javascript

        {
            'id': 31221220,
            'error': true,
            'error_msg': "'fail!'",
            'stack_trace': "Traceback (most recent call last):...",
            'result': null
        }

    Where:

    - ``id`` it is the same from the query.
    - ``error`` it is *true*.
    - ``error_msg`` tells us that we sent something with the value *fail* is
      the result of the error.
    - ``stack_trace`` contains the entire sequence of calls where the error
      within Yatel happens (cut for example) .
    - ``result`` returns empty because an error happened during the
      processing of the query.


#. **Typical Yatel query**


    We will now see an example with a more typical Yatel function domain as
    query to obtain a haplotype by its ``id``.

    .. code-block:: javascript

        {
            "id": null,
            "function": {
                "name": "haplotype_by_id",
                "args": [
                    {
                        "type": "literal",
                        "value": "01"
                    }
                ]
            }
        }

    In this case the function ``haplotype_by_id`` receives a parameter with a
    value of *01* to be the id of the haplotype to look for. The value of
    ``type`` is *literal* so that the value will not be changed from its json
    data type (string in this case) before being sent to the function. If we
    think of this as a call to a Python function ``haplotype_by_id("01")``

    .. code-block:: javascript

        {
            'id': null,
            'error': false,
            'error_msg': '',
            'stack_trace': null,
            'result': {
                'type': 'Haplotype',
                'value': {
                    'hap_id': {'type': 'int', 'value': 1},
                    'name': {'type': 'unicode', 'value': 'Amet'},
                    'special': {'type': 'bool', 'value': false}
                }
            }
        }

    The result returns a value of type ``Haplotype`` whose attributes are:
    ``hap_id`` integer of value *1*, ``name`` unicode of value *Amet* and a
    Boolean called ``special`` with value *false*


#. **Query with advanced type handling**

    The following query is a ``sum`` query that adds two or more values ​​
    whatever pass.

    .. code-block:: javascript

        {
            "id": "someid",
            "function": {
                "name": "sum",
                "kwargs": {
                    "nw": {
                        "type": "list",
                        "value": [
                            {"type": "literal", "value": 1},
                            {"type": "int", "value": "2"}
                        ]
                    }
                }
            }
        }

    As we see in this query the parameter ``nw`` is a list containing the
    values ​​"1" (defined as *literal*, so Yatel takes the json type) and the
    second *int* with a value represented by a string "2". Yatel with this
    automatically converts the second element to integer type

    A shorter version of the same query would be:

    .. code-block:: javascript

        {
            "id": "someid",
            "function": {
                "name": "sum",
                "kwargs": {
                    "nw": {"type": "literal", "value": [1, 2]}
                }
            }
        }


    The result has the form

    .. code-block:: javascript

        {
            'id': "someid",
            'error': false,
            'error_msg': '',
            'stack_trace': null,
            'result': {'type': 'float', 'value': 3.0}
        }

#. **Nested queries**

    .. code-block:: javascript

        {
            "id": 1545454845,
            "function": {
                "name": "haplotype_by_id",
                "args": [
                    {
                        "type": "unicode",
                        "function": {
                            "name": "slice",
                            "kwargs": {
                                "iterable": {"type": "unicode",
                                             "value": "id_01_"},
                                "f": {"type": "int", "value": "-3"},
                                "t": {"type": "int", "value": "-1"}
                            }
                        }
                    }
                ]
            }
        }

    This query really shows the QBJ potential. The first thing to note is
    that the main function, ``haplotype_by_id``, as the first argument receives
    the result of function ``slice``.
    The value of the ``type`` key into the argument indicates that the result
    of internal function if it is not a text must be converted to it.

    ``slice`` moreover, what it does is cut the text *id_01_* from its position *-3* to *-1*.

    if this were Python code the function would be somethin like

    .. code-block:: python

        haplotype_by_id(
            unicode(slice(iterable="id_01_", f=int("-3"), t=int("-1")))
        )

    or what is the same

    .. code-block:: python

        haplotype_by_id("01")

    The result of this query would return a ``Haplotype`` from the database
    as follows:

    .. code-block:: javascript

        {
            'id': "someid",
            'error': false,
            'error_msg': '',
            'stack_trace': null,
            'result': {
                'type': 'Haplotype',
                'value': {
                    'hap_id': {'type': 'int', 'value': 1},
                    'color': {'type': 'unicode', 'value': 'y'},
                    'description': {'type': 'unicode', 'value': '...'},
                    'height': {'type': 'float', 'value': 92.00891409813752},
                    'number': {'type': 'int', 'value': 16}
                }
            }
        }


Functions
---------

QBJ includes functions to query data on a network (``haplotypes``, ``edges``, 
``facts``, etc.); text handling (``split``, ``strip``, ``startswith``, 
``endswith``, etc.); Arithmetic and basic statistics (``sum``, ``average``, 
``kurtosis``, ``std``, etc.); data mining and treatment of local date and time 
as well as UTC_

The complete functions list it's available :ref:`here <qbjfunctions>`.

.. todo:: Quedan pendiente para versiones futuras funciones de expresiones
          regulares, trigonometría y constantes matemáticas.

QBJ Console
-----------

Yatel provides a comfortable command line interface to use QBJ. It's opened 
with the command:

.. code-block:: bash

    $ yatel qbjshell sqlite:///path_to_nw.db

.. seealso:: For more information see the documentation about 
             :ref:`command line interface <cli>`.


The Resolution Process
----------------------

.. warning:: This section provides implementation details useful for 
             developers or people interested in optimizing their queries
             
.. digraph:: Proccess

    source [shape=plaintext, label="User"];
    shell [label="QBJShell"];
    server [label="Server"];
    engine [label="Engine"];
    resolver [label="Resolver"];

    source -> shell [label="query JSON"];
    source -> server [label="query JSON"];
    shell -> engine [label="query dict"];
    server -> engine [label="query dict"];
    engine -> resolver [label="function"];
    resolver -> resolver [label="arguments"];
    resolver -> engine [label="data"];
    engine -> shell [label="response dict"];
    engine -> server [label="response dict"];

    shell -> source [label="response JSON"];
    server -> source [label="response JSON"];



#. Yatel both the server and console always receives queries in JSON_ 
   formatted in UTF-8_.
#. The server or console are responsible for converting the ``string`` into a
   ``dict`` hereafter referred as the **query**.
#. The QBJ engine receives the **query** and one more parameter that tells if 
   it should add the stacktrace if anything fails.
#. The engine extracts the main parameters of the query ``id`` 
   and ``function``.
#. The engine validates the **query** against the json-schema_ of QBJ
#. The engine creates a resolver for the main function and sends it with it's 
   context (the context is the network on wich is executing) 
#. The resolver extracts the parameters (\*args and \**kwargs) of the functions 
   and solves each separated depending on the case by:
        
        #. If the argument is a function, it generates a new resolver for that 
           function and passes the context of the current resolver.
        #. If the argument is just a value it's extracted.
        
#. Each argument is then casted to the data type specified by itself in the 
   parameter ``type`` , with the ``typeconv`` module.
#. The function is executed with all the preprocessed arguments and the result 
   it's returned to the engine.
#. At any step that an error is detected the engine draws it's description for 
   the response and the stacktrace if it was required.
#. The engine simplifies the result with ``typeconv`` module and creates the 
   response dictionary.
#. Finally the **query** is serialized into JSON_ and printed on console 
   (if using the QBJ shell) or sent back through the server.
