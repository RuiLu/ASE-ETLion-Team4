# ETLion System - v1.0
Team: ET-Lion 
* Chia-Hao Hsu (ch3141)
* MIng-Ching Chu (mc4107)
* Jin Liang (jl4598)
* Rui Lu (rl2784)

## How to run this program?
1. Run the server program from JP Morgan first:<br>

  ```python
  python server.py
  ```
2. Run the ETLionServer to launch the system:<br>

  ```python
  python ETLionServer.py
  ```
3. Input the parameters into the input boxes on the website, then click 'Place Order' button
![place order](http://i.imgur.com/6aFCM1e.png)

4. The transaction results will show up dynamically in the table one by one.
![Trade History](http://i.imgur.com/6EJNrx2.png)


## System Design
#### Frontend:
Boostrap, jQuery, Javascript

#### Backend:
Server: Socket-IO (Async Display), Flask(Server Framework)<br>
Database: PostgreSQL
