import os,sys

print(sys.argv[1])
url = os.getenv(sys.argv[1])
if url is None:
    print("env not set")
else :
    print(url)