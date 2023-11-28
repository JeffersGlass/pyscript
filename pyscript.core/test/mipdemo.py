#import mip

#Install from Micropython-lib
#This doesn't work yet, due to cors restrictions on:
#mip.install('keyword')
#mip.install('keyword', version="0.0.1")
#mip.install('keyword', target="some-other-folder")

#Install from URL:
#mip.install("http://example.com/x/y/foo.py")
#mip.install('https://github.com/micropython/micropython-lib/tree/master/python-stdlib/keyword/keyword.py')

#Install from GitHub
#mip.install('github:micropython/micropython-lib/python-stdlib/keyword/keyword.py')

#Using package.json
#mip.install("github:org/user/path/package.json")


# The Challenge - would like to use the 'keyword' package
# to load a list of Micropython keywords, but it's not
# installed.


# The 'keyword' package is in micropython's stdlib
# But not currenly baked into MP-PyScript. How does
# A user use-it?
from pyscript import display

from keyword import kwlist
display("Micropython's keywords are: " + str(kwlist))
