<a name="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
[![LinkedIn2][linkedin-shield]][linkedin-url2]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/asanzra/Betelgeuse_Gazers-EcoForecast_Revolutionizing_Green_Energy_Surplus_Prediction_in_Europe">
    <img src="https://i.ytimg.com/vi/e0i_VdHhlIw/maxresdefault.jpg" alt="Logo" width="320" height="180">
  </a>

<h3 align="center">SE-Europe-Data_Challenge</h3>

  <p align="center">
    SE + NUWE Online Data Science hackathon
    <br />
    <a href="https://github.com/asanzra/Betelgeuse_Gazers-EcoForecast_Revolutionizing_Green_Energy_Surplus_Prediction_in_Europe"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/asanzra/Betelgeuse_Gazers-EcoForecast_Revolutionizing_Green_Energy_Surplus_Prediction_in_Europe">View Demo</a>
    ·
    <a href="https://github.com/asanzra/Betelgeuse_Gazers-EcoForecast_Revolutionizing_Green_Energy_Surplus_Prediction_in_Europe/issues">Report Bug</a>
    ·
    <a href="https://github.com/asanzra/Betelgeuse_Gazers-EcoForecast_Revolutionizing_Green_Energy_Surplus_Prediction_in_Europe/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#exploratory-data-analysis">Exploratory Data Analysis</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#usage">Usage</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

The objective of this project is to is to create a model capable of predicting the country (from a list of nine) that will have the most surplus of green energy in the next hour.
We can request the data from the [ENTSO-E Transparency portal using its API](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html). 

This data includes, in intervals from 15 minutes to 1 hour:
- Power generation from different sources (solar, wind, fossil fuels, etc.) in each country.
- Total power load in each country.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [Tensorflow](https://www.tensorflow.org/)
* [Scikit-learn](https://scikit-learn.org/)
* [Numpy](https://numpy.org/)
* [Pandas](https://pandas.pydata.org/)
* [Matplotlib](https://matplotlib.org/)


<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Exploratory Data Analysis

First of all, it's surprising the amount of missing data, specially as we go towards the end of the year.

![missing_values_time_plot]

This mainly comes from some energy types, which stop showing data from a certain point.

![missing_values_energy_plot]


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
<!-- GETTING STARTED -->
## Getting Started

### Installation


First, clone the repository:
   ```sh
   git clone https://github.com/asanzra/Betelgeuse_Gazers-EcoForecast_Revolutionizing_Green_Energy_Surplus_Prediction_in_Europe
   ```
Access to the project folder with:
  ```sh
  cd Betelgeuse_Gazers-EcoForecast_Revolutionizing_Green_Energy_Surplus_Prediction_in_Europe
  ```

We will create a virtual environment with `python3`
* Create environment with python 3 
    ```sh
    python3 -m venv venv
    ```
    
* Enable the virtual environment
    ```sh
    source venv/bin/activate
    ```

* Install the python dependencies on the virtual environment
    ```sh
    pip install -r requirements.txt
    ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage
The `run_pipeline.sh` document can be executed from the command line using different arguments.

* To get the information of the arguments use:
    ```sh
    ./run_pipeline.sh <start_date> <end_date> <raw_data_file> <processed_data_file> <model_file> <test_data_file> <predictions_file>
    ```
    For example::
    ```sh
    ./run_pipeline.sh 2020-01-01 2020-01-31 data/raw_data.csv data/processed_data.csv models/model.pkl data/test_data.csv predictions/predictions.json
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


See the [open issues](https://github.com/asanzra/Betelgeuse_Gazers-EcoForecast_Revolutionizing_Green_Energy_Surplus_Prediction_in_Europe/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Alejandro Sanz Ramirez - [Linkedin](https://www.linkedin.com/in/alejandro-sanz-ramirez-3b631a201/) - asanz2003@gmail.com

Tristán Ortiz Roset - [Linkedin](https://www.linkedin.com/in/tristan-ortiz-roset-ba2762221/) - tortiz.roset@gmail.com

Project Link: [https://github.com/asanzra/Betelgeuse_Gazers-EcoForecast_Revolutionizing_Green_Energy_Surplus_Prediction_in_Europe](https://github.com/asanzra/Betelgeuse_Gazers-EcoForecast_Revolutionizing_Green_Energy_Surplus_Prediction_in_Europe)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/asanzra/Betelgeuse_Gazers-EcoForecast_Revolutionizing_Green_Energy_Surplus_Prediction_in_Europe.svg?style=for-the-badge
[contributors-url]: https://github.com/asanzra/Betelgeuse_Gazers-EcoForecast_Revolutionizing_Green_Energy_Surplus_Prediction_in_Europe/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/asanzra/Betelgeuse_Gazers-EcoForecast_Revolutionizing_Green_Energy_Surplus_Prediction_in_Europe.svg?style=for-the-badge
[forks-url]: https://github.com/asanzra/Betelgeuse_Gazers-EcoForecast_Revolutionizing_Green_Energy_Surplus_Prediction_in_Europe/network/members
[stars-shield]: https://img.shields.io/github/stars/asanzra/Betelgeuse_Gazers-EcoForecast_Revolutionizing_Green_Energy_Surplus_Prediction_in_Europe.svg?style=for-the-badge
[stars-url]: https://github.com/asanzra/Betelgeuse_Gazers-EcoForecast_Revolutionizing_Green_Energy_Surplus_Prediction_in_Europe/stargazers
[issues-shield]: https://img.shields.io/github/issues/asanzra/Betelgeuse_Gazers-EcoForecast_Revolutionizing_Green_Energy_Surplus_Prediction_in_Europe.svg?style=for-the-badge
[issues-url]: https://github.com/asanzra/Betelgeuse_Gazers-EcoForecast_Revolutionizing_Green_Energy_Surplus_Prediction_in_Europe/issues
[license-shield]: https://img.shields.io/github/license/asanzra/Betelgeuse_Gazers-EcoForecast_Revolutionizing_Green_Energy_Surplus_Prediction_in_Europe.svg?style=for-the-badge
[license-url]: https://github.com/asanzra/Betelgeuse_Gazers-EcoForecast_Revolutionizing_Green_Energy_Surplus_Prediction_in_Europe/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/alejandro-sanz-ramirez-3b631a201/
[linkedin-url2]: https://www.linkedin.com/in/tristan-ortiz-roset-ba2762221/
[product-screenshot]: images/screenshot.png
[missing_values_energy_plot]: data/missing_values_energy_plot.png
[missing_values_time_plot]: data/missing_values_time_plot.png