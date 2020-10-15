# Sprint #1
The initial version of this application was developed during a single day hackathon with the goal of creating a starting point for the project.

#### Performance
Web server requests per second: ~350

#### Next steps
Testing:
- Create unit tests to ensure the correct implementation of the matching engine
- Ensure thread safety of the matching engine in order to utilize a multi threaded web server

Scalability:
- Utilize a multi threaded web server to increase requests per second

# Spring #2
1. Utilized a multi threaded web server 
2. Thread safe orderbook implementation.
3. Implemented some code styling according to pep8

#### Performance
Web server requests per second: ~300
Latency: ~500 ms

Web server requests per second: ~150
Latency: ~150 ms
