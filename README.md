# Caravaggio Python Bindings

Caravaggio Python Bindings is a library we can use to implement a robust
python bindings to operate with our RESTful API created on top of 
Django Caravaggio REST API. 

In the following sections we explain the steps we should follow to
implement our own binding.

# Add dependency to our projecty

We will declare the dependency directly from the Git repository.

- In Setup.py
 
```shell script
install_requires =
    caravaggio-python-bindings==0.1.0

dependency_links =
    git://github.com/intellstartup/caravaggio-python-bindings.git#egg=caravaggio-python-bindings-0.1.0
```

- In requirements.txt 

```shell script
git://github.com/intellstartup/caravaggio-python-bindings.git#egg=caravaggio-python-bindings-0.1.0
```

# Our API implementation

All the requests to Caravaggio APIs must be authenticated using a TOKEN always
 transmitted over HTTPS.

Other important parameter of our API will be the domain. The url where our 
API is listening for client requests. *Ex. https://myservice.io*
 
The Caravaggio API will look for your Token and Domain in the environment
variables that you will define for your API. By default this environment
variables are `CARAVAGGIO TOKEN` and `CARAVAGGIO DOMAIN.

## MyAPI class

The first thing we'll need to do is to define our API as a subclass of
 `caravaggio_python_bindings.api.CaravaggioAPI` and the name we want to use
 for our environment variables.
 
We should define our API in the python file `api.py` of our project. 
 
This is an example of API binding of name `MyAPI`:
 
```python
from caravaggio_python_bindings.api import CaravaggioAPI

class MyAPI(CaravaggioAPI):
    """
    MyAPI is a python binding client for my Caravaggio RESTful API
    """

    CARAVAGGIO_DOMAIN = "MYAPI_DOMAIN"
    CARAVAGGIO_TOKEN = "MYAPI_TOKEN"

    default_domain = "https://myservice.io"
```
 
## The base resources

By default, `CaravaggioAPI` gives you access to two resources. One for manage
 Users and other for manage Organizations in your API deployment. 
 
The user subsystem is part of Caravaggio REST API, this is why this two
resource already comes with this library.
 
These are the operations that we have in the `UserResource` object:

- def get_user_token(self, email):
- def get_user(self, id):
- def get_users(self, params={}):
- def get_user_by_email(self, email):
- def create_user(self, data):
- def update_user(self, id, data, partial_update=True):
- def delete_user(self, id):

These are the operations that we have in the `Organizationesource` object:

- def get_organizations(self, params={})
- def get_organization(self, id)
- def create_organization(self, data)
- def update_organization(self, id, data, partial_update=True)
- def delete_organization(self, id, force=False)
- def add_member(self, organization, emails)
- def remove_member(self, organization, emails)
- def add_administrator(self, organization, emails)
- def remove_administrator(self, organization, emails)
- def add_restricted_member(self, organization, emails)
- def remove_restricted_member(self, organization, emails)
 
## Create your own resources

We are going to show the process of adding new Resources available in our
API into our client API.

Let's suppose that we have a resource published that allows us manage Company
objects. We have 2 viewsets, one of type `CaravaggioHaystackFacetSearchViewSet`
and other normal of type `CaravaggioCassandraModelViewSet`.

The first viewset allows us to do solr searches (list) and get facets
on some fields.

The second viewset allows us retrieve, create, update, and delete companies.

Our Resource should be a subclass of
`caravaggio_python_bindings.resource.Resource`.
 
Example:

```python
from caravaggio_python_bindings.resource import Resource


class CompanyResource(Resource):

    def list(self, params={}):
        return self.action(
            ['companies', 'company_search_list'],
            params=params,
            validate=False)

    def facets(self, params={}):
        return self.action(
            ['companies', 'company_search_facets'],
            params=params,
            validate=False)

    def get(self, id):
        return self.action(
            ['companies', 'company_read'], params={"id": id})

    def create(self, data):
        return self.action(
            ['companies', 'company_create'], params=data)

    def update(self, id, data, partial_update=True):
        action = "company_update" \
            if not partial_update else "company_partial_update"

        if data is None:
            raise AttributeError("The data parameter cannot be None")

        if not isinstance(data, dict):
            raise AttributeError("The data parameter must be a dictionary")

        if len(data) == 0:
            raise AttributeError("The data dictionary must contain any value")

        data["id"] = id

        return self.action(
            ['companies', action],
            validate=(not partial_update),
            params=data)

    def delete(self, id):
        """
        Remove the company from the system.

        :param id: the id of the company to be deleted
        :return:
        """
        return self.action(
            ['companies', 'company_delete'], params={"id": id})
```

The next step is to add a method in our API class to get access to this
resource through the API object.

```python
from caravaggio_python_bindings.api import CaravaggioAPI

from caravaggio_python_bindings.tests.resource_company import CompanyResource


class MyAPI(CaravaggioAPI):
    """
    MyAPI is a python binding client for my Caravaggio RESTful API
    """

    CARAVAGGIO_DOMAIN = "MYAPI_DOMAIN"
    CARAVAGGIO_TOKEN = "MYAPI_TOKEN"

    default_domain = "https://myservice.io"

    def get_companies(self):
        return CompanyResource(api=self)    
```

# How to operate with the Client API

As we were saying, Caravaggio API needs to know about two environment
variables: `MYAPI_TOKEN` and `MYAPI_DOMAIN`.

`MYAPI_DOMAIN` should be optional, and we must define it when we want to connect
to a different URL as the default of our service (development, staging,
custom deployments).

## Unix and MacOS

You can add the following lines to your .bashrc or .bash_profile to set
those variables automatically when you log in:

```shell script
export MYAPI_DOMAIN=http://localhost:8001
export MYAPI_TOKEN=ae579e7e53fb9abd646a6ff8aa99d4afe83ac291
```

refer to the next chapters to know how to do that in other operating systems.

With that environment set up, connecting to the API is a breeze:

```python
from caravaggio_python_bindings.tests.api import MyAPI
api = MyAPI()
```

Otherwise, you can initialize directly when instantiating the
MyAPI class as follows:

```python
from caravaggio_python_bindings.tests.api import MyAPI
api = MyAPI(token="ae579e7e53fb9abd646a6ff8aa99d4afe83ac291", 
            domain="http://localhost:8001")
```

These Token will allow you to manage any resource in your user and
organization environment.

# Authentication on Windows

The credentials should be permanently stored in your system using

```shell script
setx MYAPI_DOMAIN http://localhost:8001
setx MYAPI_TOKEN ae579e7e53fb9abd646a6ff8aa99d4afe83ac291
```

Note that `setx` will not change the environment variables of your actual
 console, so you will need to open a new one to start using them.
 
# Authentication on Jupyter Notebook

You can set the environment variables using the `%env` command in your cells:

```jupyter
%env MYAPI_DOMAIN=http://localhost:8001
%env MYAPI_TOKEN=ae579e7e53fb9abd646a6ff8aa99d4afe83ac291
```

For Development
-----------------
In order to maintain a clean code, it's strongly recommended to install the
project pre-commit hook. Just execute the following commands in the root
directory:

::

    $ chmod +x pre-commit.sh

    $ ln -s ../../pre-commit.sh .git/hooks/pre-commit
