# Recap Python Concepts

## List

- list[x:y] = slicing
- list.append(x) = add
- list.insert(x, y) = add multiple itens
- list.remove(8) = remove
- list.pop(0) = remove item by index
- list.sort() = sort by default strategy

## Set/Tuples

- Set does not keep order
- Set does not keep repetition
- Tuple is like a set, but It is unchangable after creation
- [] for list, () for tuple and {} for set
- set.discard(x) = remove
- set.add(x) = add
- set.update([x, y]) = add multiple elements

## Dictionaries

- dict.pop(key) = remove a item
- dict.clear() = remove all itens
- del dict = complete delete the dict

# Object Oriented Programming (OOP)

OBject Oriented Programming (OOP) is a programming paradigm based on the concept of objects, which can contain data and code. Efficiency, reusability and scalability.

The four pillars: 

Encapsulation: Bundling of data, protecting data to not be changed after instantiated or only be changed over a specific process.
 - Provides more flexibility to our code;
 - Provides more reusability with our code;
 - Provides a way to shield/protect data and code.

Abstraction: hide complexity and implementation and allow an external element to interact with a simple interface;

Inheritance: process of acquiring properties from one class to other classes. Creates a hierarchy between classes.

Polymorphism: Multi forms, behavior of managing multi objects that inherit from the same origin as the same thing. Good for flexibility, reusability.

Composition:
 - A has to relationship;
 - A way to create objects of other objects.

# What is FastAPI

It is a Python web-framework for building modern APIS:
 - Fast (Performance)
 - Fast (Development)

# Components

## Pydantic

Pydantic = Python library that is used for data modeling, data parsing and has efficient error handeling

## Status Codes Types:

1xx = Information Response: Request Processing.
2xx = Sucess:
3xx = Redirection messages
4xx = Client error responses
5xx = Server error responses

# JWT

Json web token is a data format used to transfer user claims among systems. It uses json format to organize data and It is signed using a secret key or private/public keys. Useful It is encoded in base64.

The json object has 3 parts:
    - Header: information about the cryptographic algorithm used in the JWT token
    - Payload: information about the claims carried in the jwt itself
    - Signature: Unique information, gathering encoded header, encoded payload and signing using the secret and specified algorithm 

# Alembic

It is a package that works with SqlAlchemy providing tools to create and manage schema migrations over the databases.

Useful commands:
 - alembic init <folder name>       = initializes a new, generic env
 - alembic revision -m <message>    = creates a new revision of the env
 - alembic upgrade <revison #>      = run our upgrade migration to our db
 - alembic downgrade -1             = run our downgrade migration to our db

# Useful Commands

Run project dev mod = fastapi dev books2.py

## Useful Informations

- Routers is useful to separate the code, increase readability and scalability;
- It uses and integrate well with SQLAlchemy;
- It uses dependecy injection to pass info like db session to endpoints;

# Jinja

Fast, expressive and extensible templating language.

Able to write code similar to Python in the DOM.

Jinga tags allows developers to be confident while working with backend data, using tags that are similar to HTML.