Assignment 3
FTP Client and Server
Professor Gofman
CPSC 471
due Sat. May 19, 2018

Group members:
Alan Yang       hsuehlungyang@csu.fullerton.edu
Belinda Wong    bywong@csu.fullerton.edu

Coding language:
python3

Execution for server:
Run in command line,
    python3 serv.py <port number>
    ex. $python3 serv.py 1234

Execution for client:
Run in command line,
    python3 cli.py <host name> <port number>
    ex. $python3 serv.py localhost 1234

Extra credit not implemented.

Things to take note of
- Code works on mac machine.
- Code may or may not work on a linux machine.
- No guarantee on a windows machine.  No one tested on windows.
- When testing put function, have the serv.py file in another directory.
  You will see if the test text file is being copied/uploaded to the server.
- Tested using localhost as the host name, ecs.fullerton.edu would always time out and no connection would be made.
