##########
Changelog
##########


Current
=======

- Use of coreapi and coreapi-cli libraries to implement API-Client code for
caravaggio projects.

- Base classes to implement API bindings in python for Caravaggio RESTful APIs

- Control of Throttling exceptions (HTTP 429 - Too many Requests), the client
will try tenaciously to execute the request 12 times waiting 5 seconds between
try.

- The number of tries and seconds between requests can be overwritten
by request

.. code-block:: python
   :linenos:

    return self.action(
        ['dealflow', 'backlog_search_list'],
        params=params,
        validate=False,
        n_tries=5,
        sec_btw_tries=15)


- Ability to redefine the name of the environment variables per Client
implementation. By default the name of these variables are:
`CARAVAGGIO_TOKEN` and `CARAVAGGIO_DOMAIN`, but this can be overwritten by
client. For instance, an Client API for an application named Apian, could
define its own variables as `APIAN_TOKEN` and `APIAN_DOMAIN`.

.. code-block:: python
   :linenos:

    from caravaggio_python_bindings.api import CaravaggioAPI

    class ApianAPI(CaravaggioAPI):
        """
        ApianAPI represents a binding for the Apian RESTful app.
        """

        CARAVAGGIO_DOMAIN = "APIAN_DOMAIN"
        CARAVAGGIO_TOKEN = "APIAN_TOKEN"

        default_domain = "https://apian.io"
