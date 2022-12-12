<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/thenags/Project-Shadow">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Project Shadow</h3>

  <p align="center">
    Custom Wireless Student Safety Tracker for Schools
    <br />
  </p>
</div>


<!-- ABOUT THE PROJECT -->
## About The Project

This is the Github repository for my 2023 ISEF project - Project Shadow. As the subtitle describes, it is an integration of hardware and software to track students within schools using WiFi. Currently only the software is available.

How it works:
* ESP32S2 uploads RSSIS from routers or WAPs to Firebase
* Server calculates position with an error radius (averaging 2.5m) using a complex algorithm and reuploads it to Firebase
  * The algorithm requires room boundaries, positions, WAP MAC addresses (BSSIDS), and WAP positions to be obtained before
* Website (web console) retrives position data in an interactive website for teachers and admins
  * Administrators have the ability to initiate a lockdown or lockout, and the positioning algorithm can then calculate students that are in danger
  * Teachers can see each student for the current class
* Since the dedicated, separate server calculates position, it is practically impossible to break the system

This serves as a basic installation guide and explanation of the code for the sever, device, website, and Firebase data structure.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

Make sure to have your Firebase database project set up and ready to go, along with at least 1 user for the website. This user needs an email and password to be compatiable with the login page.

### Prerequisites

Hardware requirements:
* Microcontroller with connectivity to WiFi in some way and portability. This will serve as the student.
* Microcontroller with connectivity to WiFi in some way and can act as a staion. This will serve as the WAP. At least 1 every 10m. is needed for ideal position data.
Software installs:
* Firebase-admin
  ```
  pip3 install firebase-admin
  ```
* Tkinter
  ```
  sudo apt-get install python3-tk
  ```

### Installation

_Below is an example of a sample installation for the server, device, and website, and a data structure for Firebase_

Device:

- For student:
  - Add firebase credentials to Arduino program
  - Add WiFi credentials
  - Upload to device
- For WAP:
  - Upload to device

Server:

- Install packages above
- Add Firebase json credentials to serverside folder
- Add credentials and database url in server.py
- Change variables in positioner.py
  - Add image of your school and change the "YOURIMAGEHERE.png" string and image dimensions
  - Define the centers of rooms relative to the pixels in the uploaded image in roomPositions
  - Define borders of rooms relative to the pixels in the uploaded image in roomBounds
  - Define room numbers in roomNums
  - Define the WAPs' BSSIDS or MAC addresses in roomBSSIDs
  - Define the borders of the entire buildling in schoolOutline
    - You can use defineLines.py to help with this
      - You must do steps a,b,d, and e prior to running this program
  - Define the borders of each room as previously stated
- SSH into server where the install is located and run the script:
   ```sh
   nohup python3 server.py
   ```

Website:

- Add firebase config in main.js and tracking.js
- Add image of school and change this in tracking.js

Firebase Structure:

- Settings
  - 0: Emergency state
  - 1: People in danger
  - 2: Period of day
  - 3: Server status counter
- Students
  - STUDENT ID
    - details
      - 0: Is student in danger
      - 1: Student's name
    - position
      - 0: X position
      - 1: Y position
      - 2: Radius
      - 3: Epoch time when data was uploaded
    - wapBSSIDS
      - List of scanned BSSIDS from device
    - wapRSSIS
      - List of scanned RSSIS from device
- Teachers
  - Teacher UUID
    - students
      - List of periods
        - List of student IDs for each period

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

James Nagler - jamesrnagler@gmail.com

Project Link: [https://github.com/thenags/Project-Shadow](https://github.com/thenags/Project-Shadow)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
