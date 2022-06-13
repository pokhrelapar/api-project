# 1. Problem Statement

Refer to the email
 
 # 2. Sample Output
 
 Email Message ID, Email Name, Recipients, Opens, Clicks, Unsubscribes, Bounces, Top Variant
2324646,"Tell Congress: Protect Gray Wolves", 2552, 343, 98, 5, 4, "Majestic Predators Need YOU"
2324747 "Get Your Gray Wolf Tote Bag: Donate Now!", 3541, 688, 147, 10, 8, "Furry Friends in Need"
2325647 "Join Us for a Howling Good Time!", 1599, 106, 27, 6, 4, "Don't Miss Our Grey Wolf Social"

Total: 3 emails

# 2. Dependencies and packages
The project  has the folowing dependencies and packages:
• python v=3.7.13
• requests v=2.23.0
• pandas v=1.3.5

# 2.1 Installation
1. Install python 3.7
2. Install pip if you don't have a package manager
    • Download the get-pip.py file ( https://bootstrap.pypa.io/get-pip.py) and store it in the same directory as python is installed.
    • Open terminal. Change the current path of the directory in the command line to the path of the directory where the above file exists.
    • Run the following command: python get-pip.py
3. Install packages
    • pip install requests
    • pip install pandas

# 2.2 Execution

1. Clone the repository using git clone https://github.com/pokhrelapar/api-project.git or downloading as a zip file.
2.  Go to the directory where the repo is saved. Extract the files. 
3.  Open the api-project.py file in a code editor. Only change the value of the  API_KEY = 'xxx-xxxx-xxx' to your own API key. The default username is apiuser. If different, change the value of the field self.username = 'xxxxxx' to your own username. The username and password is  then combined with a username:password to form a base64-encoded string. Save the file.
4.  There is a csv file called TestReport. It was generated using the program. You can either keep it to cross check the file generated when running the program on your end or delete it.
5. Open the folder containing the api-project.py file in terminal. Run the follwing command:
                    python api-project.py
4.  The program saves the ouput as a csv file. Look for a file called EmailReport.csv as the output.
5.  Alternatively, you can acess the  Google Colab notebook for the project through https://colab.research.google.com/drive/1myXF1SmaZA-1kXVfRn7RJceyTONv72nh?usp=sharing and run the first cell. This is only meant for testing purposes. Also, you can create a vritual envrionment using Anaconda and then install the necesary dependencies and then run the program.













