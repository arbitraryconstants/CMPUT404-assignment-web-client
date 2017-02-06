CMPUT404-assignment-web-client
==============================

CMPUT404-assignment-web-client

See requirements.org (plain-text) for a description of the project.

Make a simple web-client like curl or wget

Contributors / Licensing
========================

Generally everything is LICENSE'D under the Apache 2 license by Abram Hindle, 
https://github.com/tywtyw2002, and https://github.com/treedust

httpclient.py contains contributions from:

* Abram Hindle
* Alanna

But the server.py example is derived from the python documentation
examples thus some of the code is Copyright © 2001-2013 Python
Software Foundation; All Rights Reserved under the PSF license (GPL
compatible) http://docs.python.org/2/library/socketserver.html

Code references:

* Re: Parsing url to obtain host, port, path and query
  By okigan (https://stackoverflow.com/users/142207/okigan)
  on stackoverflow https://stackoverflow.com/questions/27745/getting-parts-of-a-url-regex
  License: CC-BY-SA 3.0


Python Library references:

* Re: socket library:
  Author: Python Software Foundation
  Visit date: Feb 4th, 2017
  Title: 17.2. socket - Low-level socket interface
  URL: https://docs.python.org/2/library/socket.html

* Re: urllib library:
  Author: Python Software Foundation
  Visit date: Feb 4th, 2017
  Title: 20.5. urllib - open arbitrary resources by URL
  URL: https://docs.python.org/2/library/urllib.html

Note regarding recvall function
===============================

This function hangs if using HTTP/1.1 for certain requests. For example:

python2 httpclient.py GET "www.adasteam.ca/" hangs for HTTP/1.1 request likey because
the "Connection: close" header is not included in the response from www.adasteam.ca

python2 httpclient.py GET "www.adasteam.ca/" works as expected for HTTP/1.0 request
as the "Connection: close" header is include in the response from www.adasteam.ca

This was discovered after reading the 404 eclass post "Assignment 2 Redirects"

To avoid this issue, the status line of requests is now set to HTTP/1.0 rather than HTTP/1.1
