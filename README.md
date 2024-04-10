# Distributed-systems-4
Distributed Systems Assignment 4

There is error handling at the server and client creation/establishment. Client handling, if the client crashes or otherwise "disappears". There's also error handling at writing and receiving messages. Scalability is done through threading, although it's not massively scalable, this should be enough for this purpose. The transparency works in a way where the clients don't ever have to know that the messages go through the server, unless the server isn't running, or some other error comes up. Also if one client fails, the others can still communicate, meaning there's at least some degree of failure transparency included.

I had issues implementing the private messaging, there is implementation for it in the code, but it doesn't work as intended, I tried to focus on the distributed nature of the system and ended up not successfully implementing the private messaging part.

Youtube link to the video part of the assignment: https://youtu.be/a-oo4SAXVE8
