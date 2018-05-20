Check your current version with cmake --version

Uninstall it with sudo apt remove cmake

Visit https://cmake.org/download/ and download the latest binaries

In my case cmake-3.6.2-Linux-x86_64.sh is sufficient

chmod +x /path/to/cmake-3.6.2-Linux-x86_64.sh (use your own file location here, but chmod makes the script executable)

sudo /path/to/cmake-3.6.2-Linux-x86_64.sh (you'll need to press y twice)

The script installs to /opt/cmake-3.6.2-Linux-x86_64 so in order to get the cmake command, make a symbolic link:

sudo ln -s /opt/cmake-3.6.2-Linux-x86_64/bin/* /usr/local/bin

Test your results with cmake --version