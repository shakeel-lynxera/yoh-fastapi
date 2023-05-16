# YOH
The goal of this project is to implement a search module using Redis and FastAPI.
When a user searches for a keyword, it will be saved for future suggestions.
Subsequent searches of the same keyword will be prioritized using a ranking
algorithm, ensuring they appear at the top. Additionally, the user's real-time 
location will be stored in the cache.



## Tools and Technologies
        Python3
        FastAPI
        Redis
        Docker


## Running the Project

To run the project, follow these steps:

1. Configure `Redis` in `main.py`
2. Build Docker using `docker build -t your-image-name .`
3. Access the project's APIs in your browser at: `http://localhost:80/docs`


## Directory structure
    .
    |
    |-- BaseModels
    |-- Dockerfile
    |-- main.py
    |-- README.md
    |-- requirement.txt
    |-- response.py
    |-- utils.py

## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature: `git checkout -b feature-name`
3. Make your changes and commit them: `git commit -am 'Add some feature'`
4. Push the branch to your forked repository: `git push origin feature-name`
5. Open a pull request on GitHub.

Please ensure that your code follows the project's coding conventions and includes appropriate tests.