# Feral Fotos

## Server

* Flask server to accept photo uploads, resize them and copy them to the client with an
  instruction (portrait or landscape)
* Python client to print every photo which gets SCP'd into a specific folder

## Network architecture

* Server should be accessible on public WAN
* Client should have port 22 open to a specific DuckDNS URL
* Both server and client should be local GitHub runners
* CI/CD Deploy should: 
    * Update server and client software
    * Test the SSH connection
    * Include these variables:
        * client_print_folder
        * border_image_landscape
        * border_image_portrait

# Licence

Copyright 2025 Will Thong

Permission is hereby granted, free of charge, to any person obtaining a copy of this
software and associated documentation files (the “Software”), to deal in the Software
without restriction, including without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT
OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
