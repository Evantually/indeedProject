# Machine Learning with Indeed Job Postings

This project is my undertaking of automating a little of the job search process.

## Getting Started

I started this project with the idea of creating a dataset of job postings from Indeed using search terms that track closely to jobs relating to my skills. Created in Python, this tool will scrape all job results that return from the Indeed search without any geographical consideration. Sponsored ads will be left out, and there are checks to ensure the same jobs are not collected multiple times. After that I sifted through 5000 of the postings to classify whether I believe I am qualified. I separated out anything that appeared to be a "qualification" with a low-tech technique of all "<li>" labeled items being part of this category. Then the neural net training began to figure out the correlation between the job summary text, qualifications, job title, and location to determine whether new job postings would be of interest to me. I don't see this being readily usable by anyone, but if you love machine learning, programming, and have an affinity for working in the big cities feel free to give this a try.

### Prerequisites

Python (obviously)
ChromeDriver
Tensorflow
```
pip install tensorflow
```
Keras
```
pip install keras
```
Pandas
```
pip install pandas
```
Selenium
```
pip install selenium
```
Also, a passion for talking with computers!

### Installing

This should work (mostly) out of the box if you have set up the prerequisites. You will have to set the Chromedriver executable path found in the "initalize" function of jobSummaryPull.py.

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

* **Evan Beese** - *Initial work* - [Evantually](https://github.com/Evantually)

See also the list of [contributors](https://github.com/Evantually/indeedproject/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details