# FusionAuth Integration with Flask and React

This project demonstrates a robust integration of FusionAuth with a Flask backend and React frontend, providing a secure and seamless authentication system. It supports user registration, sign-in, and Google OAuth login, with session management implemented using secure HTTP-only cookies.

## Prerequisites

- Docker and Docker Compose
- Python 3.8+
- Node.js 14+
- npm 6+

## Setup Instructions

### 1. FusionAuth Setup

1. Clone this repository:
```
git clone https://github.com/raviteja-reddy-guntaka/fusionauth-flask-react-integration.git
cd fusionauth-flask-react-integration
```

2. Start FusionAuth using Docker Compose:
```
docker-compose up -d
```
3. Access FusionAuth admin UI at `http://localhost:9011`

4. Create a new application in FusionAuth:
- Open http://localhost:9011/
- Navigate to Applications → Add
- Set up OAuth settings and note down the Client ID and Client Secret
- For detailed instructions, refer to [FusionAuth Application Setup Guide](https://fusionauth.io/docs/get-started/core-concepts/applications)

5. Set up Google OAuth:
- Create a Google OAuth app and get Client ID and Secret
- Configure Google Identity Provider in FusionAuth
- Follow [FusionAuth Google Identity Provider Setup](https://fusionauth.io/docs/lifecycle/authenticate-users/identity-providers/social/google)


### 2. Backend Setup

1. Create and activate a virtual environment:
```
cd flask-app
python -m venv venv

# On Linux use
source venv/bin/activate 

# On Windows use
venv\Scripts\activate
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Update the following values in the `.env` file in the `flask-app` directory:
```
FUSIONAUTH_CLIENT_ID=your-fusionauth-application-client-id
FUSIONAUTH_CLIENT_SECRET=your-fusionauth-application-client-secret
FLASK_SECRET_KEY=your-flask-key
FLASK_ENV=development
```

4. Start the Flask application:
```
python app.py
```
Or use the provided `run_flask.bat` file on Windows.

### 3. Frontend Setup

1. Navigate to the frontend directory `react-app`:
```
cd react-app
```

2. Install dependencies:
```
npm install
```

3. Start the React application:
```
npm start
```

## Usage

- Access the React application at `http://localhost:3000`
- Use the "Sign in with FusionAuth" button to log in
- Use the "Create new account" link to register
- Google OAuth login is available if configured


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
