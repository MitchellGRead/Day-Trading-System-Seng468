# Day-Trading-System-Seng468
This is a distributed day trading system created as part of the course project for SENG 468 at the University of Victoria, Spring 2021.
It is comprised of numerous semi-independent services that together form the entire system.

# How to start up the system
The system's various services need to be started in a certain order for successful start-up. This order is as follows:
<ul>
<li> Database containers & Redis cache
<li> Database manager
<li> Audit service
<li> Dummy stock quote service
<li> Transaction service
<li> Web service
<li> Generator (for testing)
</ul>