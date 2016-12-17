.. ETLion Trade documentation master file, created by
   sphinx-quickstart on Fri Dec  9 23:49:36 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to ETLion Trade's documentation!
========================================

.. image:: lion.gif
   :align: center

.. toctree::
   :maxdepth: 2
   :caption: Contents:

**ETLion Trade** is an online web-based electronic trading application named “ETLion”. This application will split the order and execute each part at an even rate during a given period of time. The goal for this project is to make the process of executing client orders more efficient and transparent by automating the execution of the order, in a way that can minimize the market impact. After the trader place an order, they can use the application to monitor the overall order progress and details for each trades, including its execution time, status, and exchange quantity. The target user would be the trader who is in charge of the transaction for customers. In this application, user can login to the system, get the data from JP Morgan exchange API and make decision according to the transaction results.

User Stories
------------

+-------------------+----------------------------------------------------------------------------------------------------+
| Title             | Description                                                                                        |
+===================+====================================================================================================+
| Login System      | User can login to the system by entering user name and password.                                   |
+-------------------+----------------------------------------------------------------------------------------------------+
| User Input        | User can input the amout of order and the how long the transaction period is to execute the trade. |
+-------------------+----------------------------------------------------------------------------------------------------+
| View Transactions | User can see the result of each transaction.                                                       |
+-------------------+----------------------------------------------------------------------------------------------------+
| Logout System     | User can login to the system by entering user name and password.                                   |
+-------------------+----------------------------------------------------------------------------------------------------+
| View History      | User can view order history and detailed trades information.                                       |
+-------------------+----------------------------------------------------------------------------------------------------+
| Select Time       | User can view history by choosing a specific time or a time range.                                 |
+-------------------+----------------------------------------------------------------------------------------------------+

Tech Stack
----------

The main technology stack we will use is Flask-- a Python based Web Framework, which is easy for developers to build backend server and hock up with frontend side. For the front end side, we will use React to build the user interfaces. The server will be deployed on AWS, since AWS provides user flexibility to develop and configure the environment they want. For the static analysis tool, we will use prospector and pyflake. For later unit testing tool, we will use shell script to write the unit test script. The languages and tools are summarized as follows: 

- `Python`: Since we are working on JP Morgan project, we decide to follow JP Morgan to use Python to develop this project.
- `Flask Web Framework`: Flask is a handy web framework based on Python. 
  We will put our client side on another Flask server to   help trader interact with our system more easily.
- `React.js`: React can build our web UI in a more composable way.
- `JQuery / JS`:  JQuery can help us to implement some AJAX features on our Web UI.
- `Bootstrap`: Boostrap is a very easy front end framework which provides a lot of existing designed components, 
  like button, bar, etc. This framework can help us to buid up the front end more easily.
- `Amazon Web Services`: AWS provides user flexibility to develop and configure the environment they want.
- `Prospector & Pyflake`: These two are good Python static analysis tool.
- `PostgreSQL`: PostgreSQL is a powerful, open source object-relational database system. 
  It has more than 15 years of active development and a proven architecture that has earned it a strong reputation for reliability, data integrity, and correctness.
- `Coverage.py`: Coverage.py is for testing coverage for python.




Installation & Set Up
---------------------

You can install this package in the usual way using ``pip``::

    pip install requirement.txt
    python server.py
    python ETLionServer.py

Requirements
------------

All requirements are in requirement.txt.

Tutorial
--------

How to run this program?
^^^^^^^^^^^^^^^^^^^^^^^^

**1. Run the server program from JP Morgan:**::
    
    python server.py

**2. Run the ETLionServer to launch the system:**::

    python ETLionServer.py

**3. Input url 127.0.0.1:<port>:**::
    
    http://127.0.0.1:<port>

How to use the application?
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**1. Sign Up:**

**2. Sign In:**

**3. Place Order:**

**4. View Transaction:**

**5. View Price Chart:**

**6. View All History:**

**7. View History with Specific Date:**

**8. View History with Range Date:**