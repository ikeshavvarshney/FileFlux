# Save a folder under an alias
py fileflux.py save test E:\CODing\hackathonRaptors\test

# Show info about a file
py fileflux.py info example.py

# Copy a file
py fileflux.py copy example.py copy_example.py

# Cut (move) a file
py fileflux.py cut copy_example.py SubFolder/copy_example.py

# Delete a file
py fileflux.py delete copy_example.py

# Make a directory
py fileflux.py mkdir NewFolder

# Rename a file
py fileflux.py rename old.txt new.txt

# Jump to a saved alias path
py fileflux.py jump test
# (use with PowerShell function to actually change terminal path)
