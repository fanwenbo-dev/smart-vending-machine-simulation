# Smart Drink Vending Machine (VM) Simulation

## Table of Contents
1. [Project Overview](#1-project-overview)
2. [SRS](#2-srs)
3. [Demo Run - Video](#3-demo-run---video)
4. [Docker](#4-docker)
5. [Team Contributions](#5-team-contributions)



## 1. Project Overview
[Back to Top](#table-of-contents)

### Project Description

![Screenshot](https://github.com/ET0735-DevOps-AIoT-AY2410/DCPE_2A_02_Group2/blob/wenbo/Screenshot%202024-08-08%20111932.png?raw=true)

### Project Description

The **Smart Drink Vending Machine (VM) Simulation** project aims to create a comprehensive simulation of a smart vending machine system designed for dispensing drinks. The system encompasses various functionalities including onsite and online purchases, authentication for service technicians and suppliers, and security measures such as a burglar alarm. This simulation is intended to provide a detailed representation of how such a vending machine would operate, integrating both hardware and software components to mimic real-world scenarios.

#### Key Features

* **Main Menu:** Allows users to choose between purchasing drinks or accessing service options.
* **Onsite Purchase:** Facilitates physical drink selection and purchase through an interactive menu and keypad.
* **Online Purchase:** Enables users to buy drinks remotely via a web interface, then generating QR codes or barcodes for pickup.
* **Authentication:** Provides secure access for technicians and suppliers through a user code entry system.
* **Burglar Alarm:** Activates a buzzer if the vending machine door is forcefully opened to deter theft.
* **Non-Functional Modes:** Includes inactive and active modes based on user interaction and sensor input.

The project also integrates Docker for containerization, ensuring that the vending machine simulation can be deployed and tested consistently across different environments.



## 2. SRS 
[Back to Top](#table-of-contents)

- [System Architecture](#system-architecture)
- [Functional Requirements](#functional-requirements)
- [Function 1 – Start Up and Main Menu](#function-1--start-up-and-main-menu)
- [Function 2 – Onsite Purchase](#function-2--onsite-purchase)
- [Function 3 – Online Purchase](#function-3--online-purchase)
- [Function 4 – Authentication Services](#function-4--authentication-services)
- [Function 5 – Burglar Alarm](#function-5--burglar-alarm)
- [Software Architecture](#software-architecture)

### System Architecture

<img src="https://github.com/ET0735-DevOps-AIoT-AY2410/DCPE_2A_02_Group2/blob/wenbo/Screenshot%202024-08-11%20132449.png?raw=true" alt="Screenshot" width="600" />



### Functional Requirements


#### Function 1 – Start Up and Main Menu


The Smart Drink VM will prompt users on their needs when they use the VM.

**REQ_ID** | **Requirement**
--- | ---
REQ-01 | When the VM is active, the file to be called is based on the slide switch position. <br><br>Left position: Projectmain.py file is called (for purchasing of drinks)<br>Right position: Authentication.py file is called (for service technicians and drinks suppliers)
REQ-02 | In the main menu defined in REQ-01, if the slide switch is in the left position, the Projectmain.py file will run, and the following menu shall be displayed on the LCD Screen <br><br>&nbsp;&nbsp;&nbsp;&nbsp;Line 1 : “1. Key Selection” <br>&nbsp;&nbsp;&nbsp;&nbsp;Line 2 : “2. Online Payment”
REQ-03 | In the main menu defined in REQ-01, if the slide switch is in the right position, the Authentication.py file will run, and the following menu shall be displayed on the LCD Screen <br><br>&nbsp;&nbsp;&nbsp;&nbsp;Line 1 : “Authentication”  <br><br>&nbsp;&nbsp;&nbsp;&nbsp;(wait for a while) <br><br>&nbsp;&nbsp;&nbsp;&nbsp;Line 1 : “Key user code:” <br>&nbsp;&nbsp;&nbsp;&nbsp;Line 2 : The LCD shall display “X” for each key pressed <br><br>&nbsp;&nbsp;&nbsp;&nbsp;The valid user code is made up of 6 characters, including numbers & special characters. (*73524)

#### Function 2 – Onsite Purchase
The Smart Drink VM allows users to purchase their drink physically from the VM.

**REQ_ID** | **Requirement**
--- | ---
REQ-04 | Each drink in the VM is given a corresponding number based on our CSV file for drinks (drinks.csv). <br><br>From REQ-02, if the user selects “1. Key Selection”, the VM will read the drink.csv provided by the vendor with the list of drinks and their corresponding price the vending machine is selling.
REQ-05 | The VM will prompt the user to select a drink afterwards. The user is allowed to enter any number between 0 to 99. When a number is keyed in, the following text shall be displayed on the LCD Screen. <br><br>&nbsp;&nbsp;&nbsp;&nbsp;Line 1 : “Enter Number:” <br>&nbsp;&nbsp;&nbsp;&nbsp;Line 2 : [Display number entered] : <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;“X” or “XX”, where X represent a digit from 0 to 9
REQ-06 | If the user is unsatisfied with his selection, he can choose ‘*’ to re-enter his drink number as and when he wants. <br><br>If the user is satisfied with his selection, he can choose ‘#’ to confirm his number. Afterwards, the flowchart defined in Figure 1 shall be implemented.<br>[“\*” still works when the user has accidentally press “#”]

<img src="https://github.com/ET0735-DevOps-AIoT-AY2410/DCPE_2A_02_Group2/blob/wenbo/Screenshot%202024-08-11%20105258.png?raw=true" alt="Flowchart" width="600"/>

#### Function 3 – Online Purchase
The Smart Drink VM supports “Online Purchase” remotely via smartphones or an external website.

**REQ_ID** | **Requirement**
--- | ---
REQ-12 | The user shall be able to access and view the website to purchase drinks from the VM without being physically there.
REQ-13 | The user should make payment via the app or website, and a QR code or barcode will then be generated for the user to scan at the VM, to collect their drink.
REQ-14 | From REQ-02, if the user selects “2. Online Payment”, then the flowchart defined in Figure 2 shall be implemented.

<img src="https://github.com/ET0735-DevOps-AIoT-AY2410/DCPE_2A_02_Group2/blob/wenbo/Screenshot%202024-08-08%20113803.png?raw=true" alt="Screenshot" width="600" />

#### Function 4 – Authentication Services
For service technicians and drink suppliers, they will need to enter a valid user code on the keypad to open the VM door without triggering the burglar alarm.

**REQ_ID** | **Requirement**
--- | ---
REQ-19 | Service technicians and/or drink suppliers have only 3 attempts to key in the valid code before the buzzer rings. For each invalid attempt, the following text shall be displayed on the LCD screen. <br><br>&nbsp;&nbsp;&nbsp;&nbsp;Line 1 : “Invalid code” <br>&nbsp;&nbsp;&nbsp;&nbsp;Line 2 : [Display attempts left] : <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;“(integer) attempts left”
REQ-20 | If the 6 character code corresponds to the valid user code, then the flowchart defined in Figure 3 shall be implemented.

<img src="https://github.com/ET0735-DevOps-AIoT-AY2410/DCPE_2A_02_Group2/blob/wenbo/Screenshot%202024-08-11%20110027.png?raw=true" alt="Screenshot" width="600" />


#### Function 5 – Burglar Alarm
To avoid any theft of the drinks, a buzzer will be activated if the VM door has been forcefully pried open.

**REQ_ID** | **Requirement**
--- | ---
REQ-24 | From REQ-19, if an invalid code has been keyed in wrongly for the 3rd time, the buzzer shall be activated based on the timing diagram in Figure 4

<img src="https://github.com/ET0735-DevOps-AIoT-AY2410/DCPE_2A_02_Group2/blob/wenbo/Screenshot%202024-08-08%20114446.png?raw=true" alt="Screenshot" width="600" />


### Non-Functional Requirements

#### Activation Management
The Smart Drink VM has 2 modes as defined in the State Machine Diagram in Figure 4 below. The transitions between the Inactive Mode and Active Mode are triggered by the events labeled “evEnterIM” and “evEnterAM”.

Conditions for trigger events are defined in the requirements below.

<img src="https://github.com/ET0735-DevOps-AIoT-AY2410/DCPE_2A_02_Group2/blob/wenbo/Screenshot%202024-08-08%20114809.png?raw=true" alt="Screenshot" width="600" />


**REQ_ID** | **Requirement**
--- | ---
REQ-25 | **“evEnterIM” Trigger Condition 1:** <br><br>When the keypad has not been pressed for at least 1 minute.
REQ-26 | **“evEnterIM” Trigger Condition 2:** <br><br>When the PiCam has not detected any payment for at least 1 minute.

**REQ_ID** | **Requirement**
--- | ---
REQ-27 | **“evEnterAM” Trigger Condition 1:** When the user presses any button on the keypad.

### Software Architecture

#### Static Software Architecture
The Software Architecture defines the various Software Components that are developed to realize the implementation of the system requirements.


<img src="https://github.com/ET0735-DevOps-AIoT-AY2410/DCPE_2A_02_Group2/blob/wenbo/Screenshot%202024-08-11%20132005.png?raw=true" alt="Screenshot" width="600" />



## 3. Demo Run - Video
Link to Video : https://youtu.be/A-uYHc7RFuI OR https://drive.google.com/file/d/1a_xmQt5CXC531M4qS1Fb-RfWPk6hNcDl/view?usp=sharing<br>[In ./src/mysite] python3 manage.py runserver 0.0.0.0:8000 [In browser, enter IP:8000/testcsv/update]



## 4. Docker
[Back to Top](#table-of-contents)

1. Main file: Main.py
2. Image pushed to: https://hub.docker.com/repository/docker/akrecy/devops-g2-project/general



## 5. Team Contributions
[Back to Top](#table-of-contents)
**Name** | **Contribution**
--- | ---
Angelin | <ul><li>Completed SRS</li><li>Sprint_Planning_Template.xlsx & System_Test_Report_template.xlsx (except on-site req.)</li><li>Alarm.py, TFunctions.py & test_TFunctions.py</li><li>Dockerfile</li><li>Edit ReadMe.md</li><li>Video Editing</li><li>Dockerising
Kai Yang | <ul><li>Edit SRS - System Architecture & On-site flowchart</li><li>On-site part of Online_Onsite.py & drinks.csv</li><li>test_TFunctions.py : test_online_finddrinkinfo_name()</li><li>System_Test_Report_template.xlsx (on-site) & Manual test</li><li>Take video</li><li>Dockerising
Tristan | <ul><li>Non-functional Codes & inactive.py</li><li>Online_Onsite.py (Putting everyone's code together)
Wen Bo | <ul><li>Authentication.py</li><li>PyTest for on-site</li><li>Readme
Kai Weng | <ul><li>Website</li><li>Online part of Online_Onsite.py (Include PiCam) & Main.py</li><li>owed.csv & updt.csv</li><li>Update SRS</li><li>Requirements.txt
