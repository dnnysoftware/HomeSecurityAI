<a name="readme-top"></a>

[![macOS](https://svgshare.com/i/ZjP.svg)](https://svgshare.com/i/ZjP.svg)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
      </ul>
    </li>
    <li><<a href="#installation">Installation</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

![MY SECURITY CAMERA DEMO](img/demo-screenshot.png)

This Project is supposed to simulate a security camera system like Amazon's RING product in which the algorithm notices human movement by object detection and classification then begins recording and uploads the video instance to the cloud in this case AWS s3.

At Runtime: 
* The program creates a video display using opencv to monitor the physical environment 
* Creates the object classification and detection model, then begins surveying environment data within the capture algorithm
* Records the video from the cv2 display once it classifies a person 
* Saves that recording to a local directory until the recording is quit by pressing 'q' on the display 
* uploads all stored videos to AWS s3 and removes all videos from local directory.


<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

Languages:
* Python
* Shell Script

API's:
* Twilio (twilio API)
* AWS s3 (aioboto3 API)

Libraries:
* OpenCV (cv2)
* Python Decouple (decouple)
* Stopwatch.py (stopwatch)
* asyncio 

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

Clone the repository, via HTTP or SSH above, all dependencies have been added to the virtual environment and everything has been handled in that regard. However, you need to add some environment variables in a `.env` file that you will create some API keys (further explained below) because obviously I'm not giving out mine.

### Installation

1. Get a free API Key at:
* [Create Your Own AWS S3 Cloud Database](https://aws.amazon.com/pm/serv-s3/)
* [Get You Own Twilio SMS Keys](https://www.twilio.com/docs/sms)
2. Clone the repo
  ```sh
  git clone https://github.com/dnnysoftware/HomeSecurityAI.git
  ```
3. Enter your API in `.env`
  ```python
  SMS_ACCOUNT_SID='Twilio Account SID Key'
  SMS_AUTH_TOKEN='Twilio Authentication Token'
  TWILIO_NUMBER='Twilio Generated Phone Number For Testing'
  TARGET_NUMBER='Your Personal Phone Number'
  AWS_ACCESS_KEY='AWS s3 Access Token'
  AWS_SECRET_KEY='AWS s3 Secret Token'
  AWS_SECURITY_BUCKET_NAME='AWS Name Of Your Created Bucket'
  ```
4. Run Program
  * In root directory run by typing in CLI
  ```sh
  ./run.sh
  ```
5. Quit Program
  * Quit by key press 'q' in CV2 display

<p align="right">(<a href="#readme-top">back to top</a>)</p>
