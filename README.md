# Summary:
This tool was designed to extract the data used on the paper On the Contributions from Women Key Developers to Open-Source Communities. The tool is able to clone a set of GitHub repositories, extract metadata, compute the Core Developers from the cloned repositories and classify their gender.  

To extract metadata from repositories the tool relies on GitHub API. Therefore, you must already have an account on GitHub API to be able to run it.  

In regard to computing Core Developers, it's used a Java software called Truck-Factor (https://github.com/aserg-ufmg/Truck-Factor).

The gender classifier is based on two applications: GenderComputer (https://github.com/tue-mdse/genderComputer) and Nansor (https://www.namsor.com/). The later is a web service, so you must create an API key on Nansor (nansor.com) before starting. 

In order to deal with environment issues (JVM, different Python versions, gender classifier setup) GitGender relies on a Docker container. 


# Requirements:  

* A GitHub account (it will be used to get data from GitHub API).   
* A Namsor account (it will be used to identify developers by gender).  
* Docker installed (we've tested on version 2.0.0.3).  


1 - Create a shared folder on the host machine (do not save anything on it). It will be used to share files between the container and the host machine.  
2 - Clone this repository.  
3 - Enter the cloned folder and edit dockerFile. Fulfill the variables at the start of file with your Github credentials and Namsor API key
4 - Build the docker image typing the command: docker build -t gitgender.  

# Running:
Now, you have to run a container from the created image. You must map folder /git/gender on the container to the shared folder created on step 1 (on the host machine) and the process will start automatically (be careful, it can take a long time and download a huge amount of data). For example:   
    

    docker run --rm -it -v /tmp/files:/gitgender/files/ gitgender
    
The output files (on CSV format) will be saved on the shared folder that you created on step 1.
