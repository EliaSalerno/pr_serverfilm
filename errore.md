Traceback (most recent call last):
  File "C:\Users\elias\anaconda3\Lib\site-packages\flask\app.py", line 1536, in __call__
    return self.wsgi_app(environ, start_response)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\elias\anaconda3\Lib\site-packages\flask\app.py", line 1514, in wsgi_app
    response = self.handle_exception(e)
  File "C:\Users\elias\anaconda3\Lib\site-packages\flask\app.py", line 1511, in wsgi_app
    response = self.full_dispatch_request()
  File "C:\Users\elias\anaconda3\Lib\site-packages\flask\app.py", line 919, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "C:\Users\elias\anaconda3\Lib\site-packages\flask\app.py", line 917, in full_dispatch_request
    rv = self.dispatch_request()
  File "C:\Users\elias\anaconda3\Lib\site-packages\flask\app.py", line 902, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "C:\Users\elias\Desktop\progetti_git\pr_serverfilm\app.py", line 28, in index
    categories = get_categories()
  File "C:\Users\elias\Desktop\progetti_git\pr_serverfilm\app.py", line 14, in get_categories
    videos = sorted(

TypeError: '<' not supported between instances of 'dict' and 'dict'
127.0.0.1 - - [13/Jun/2026 20:23:20] "GET /?__debugger__=yes&cmd=resource&f=style.css HTTP/1.1" 304 -
127.0.0.1 - - [13/Jun/2026 20:23:20] "GET /?__debugger__=yes&cmd=resource&f=debugger.js HTTP/1.1" 304 -
127.0.0.1 - - [13/Jun/2026 20:23:21] "GET /?__debugger__=yes&cmd=resource&f=console.png&s=RzvkNMVBmP4YwRoBALkH HTTP/1.1" 200 -
127.0.0.1 - - [13/Jun/2026 20:23:21] "GET /?__debugger__=yes&cmd=resource&f=console.png HTTP/1.1" 304 -
