import bz2
import zlib

# Getting bytes of package from last levl
package_pack = open("package.pack", "rb")
package_content = package_pack.read()
package_pack.close()

pieces = ""

i = 0

def WritePackage(n, content):
    package_pack = open("package %s.pack" % n, "wb")
    package_pack.write(content)
    package_pack.close()

while True:
    WritePackage(i, package_content)
    i += 1
    
    if   package_content.startswith("x\x9c"):
         package_content = zlib.decompress(package_content)
         pieces += " "
    elif package_content.endswith("\x9cx"):
         package_content = package_content[::-1]
         pieces += "\n"
    elif package_content.startswith("BZh"):
         package_content = bz2.decompress(package_content)
         pieces += "#"
    else:
        break

print pieces
