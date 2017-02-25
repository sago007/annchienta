# annchienta
A small fork of http://annchienta.sourceforge.net/ - Mostly for research

While looking around for open source RPGs I fell over http://annchienta.sourceforge.net/. 
It had not been updated since 2010 but was descriped as feature complete.

It does now compile again. Although it still feels old in some ways.

Still a few minor changes may make it enjoyable again.

##Compile

The engine can be compiled with
```
cd Annchienta/annchienta
cmake .
make
```
It needs installing. In my case I had to copy "annchienta.py" and "_annchienta.so" to "~/.local/lib/python2.7/site-packages".

I'll try to get a build environment up, so I can see the exact requirements.

##Known problems

Theoretically you should be able to type "sudo make install" after "make" to have it installed but it appeared to install it to the wrong directory. In my case it installed to "/usr/local/lib/python3.5/site-packages/" and it did not work.
