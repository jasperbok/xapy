xapy
====

A simple Python wrapper around the `xapi.us`_ Xbox API service.

.. _xapi.us: https://xapi.us

Setup
-----

::

    pip install xapy

Usage
-----

Import the library and initialize a `Client`:

.. code-block::

    from xapy import Client

    client = Client("my api token")

Getting an API Token
--------------------

You can sign up for a free API token at https://xapi.us/register. Change your plan to 'Free' ('Silver' is selected by
default) to access the free plan. The free plan limits you to 60 requests per hour. For personal purposes that may be
more than enough.

After signing up you'll find your API token on your profile page at https://xapi.us/profile.