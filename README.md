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
3. Signup or login with a user account.
![Login/Signup](http://i.imgur.com/mIes5Rw.png)

4. Place order with total number of shares, expected end time, and order size.
![Place Order](http://i.imgur.com/fvmf599.png)

5. Track your order history and details for each order.
![Trade History](http://i.imgur.com/TKxP0f6.png)


## Software stack
#### Frontend:
Boostrap, jQuery, Javascript, D3.js

#### Backend:
Server: Socket-IO (Async Display), Flask(Server Framework)<br>
Database: PostgreSQL
