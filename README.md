# Project Overview

This project leverages the `google-generativeai` library to extract and infer data from documents.
The primary goal is to sanitize and analyze the content of resumes to provide structured information and insights.

## Features

- **Data Sanitization**: Removes sensitive or inappropriate content from the data before processing.
- **Data Inference**: Uses a generative AI model to infer specific details from the provided data, such as educational background and work experience.

## Setup

1. **Install Dependencies**: Ensure you have all the required packages installed. You can install them using `pip`:

    ```sh
    pip install -r requirements.txt
    ```

2. **Environment Variables**: Create a `.env` file in the root directory of the project and add your API key:

    ```dotenv
    GEMINI_API_KEY="your_api_key_here"
    ```

## Usage

To run the project, execute the `query_data.py` script. This script will load the environment variables, configure the generative AI model, and process the data.
You can add files to pdf files to the [Files]() folder, change queries in the `query_data.py` file, and run the script to see the results.
```sh
python main.py
```

## Testing

For testing purposes, a sample resume is used instead of sensitive client files. This ensures that the functionality can be verified without exposing any confidential information.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.