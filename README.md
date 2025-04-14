# Masterblog API & Frontend

## Project Description

This project consists of two main components:  
1. A Flask-based RESTful API for managing blog posts.  
2. A simple frontend built with HTML, CSS, and JavaScript that interacts with the API.

The goal is to apply key concepts of web development such as backend APIs, data persistence, and frontend integration.

## Project Structure

The project is divided into two folders:

- **backend/**  
  Contains the Flask application, including all API routes, the JSON data store, and logic for handling requests.

- **frontend/**  
  Contains a lightweight web application with HTML, CSS (including animations), and plain JavaScript for UI and user interaction.

## How It Works

The API manages a list of blog posts stored in a JSON file. These posts can be retrieved, created, or deleted using standard HTTP methods (GET, POST, DELETE). The frontend displays existing posts and allows users to submit new ones through an interactive interface.

## Technologies Used

- Python 3 with Flask (including `flask_limiter` for rate limiting)  
- HTML, CSS, and vanilla JavaScript  
- JSON file for persistent storage

## How to Run the Project

### 1. Start the Backend

- Open a terminal and navigate to the project directory.  
- (Optional) Activate your virtual environment.  
- Run the backend with the command:  
  `python3 -m backend.backend_app`  
- The API will run on port `5002` and be accessible at `http://127.0.0.1:5002` or via your Codio public URL.

### 2. Start the Frontend

- In a second terminal window, run:  
  `python3 -m frontend.frontend_app`  
- This will launch the frontend on port `5001`.  
- Open `http://127.0.0.1:5001` in your browser, or use the Codio public URL for port `5001`.


### 3. Connect Frontend to API

In the input field labeled **“Enter API Base URL”**, paste the full API address, e.g. `http://127.0.0.1:5002` or your **Codio URL with port 5002**.  
Click **“Load Posts”** to fetch and display the posts.

---

### 4. Manage Blog Posts

- You can add new blog posts using the input fields and submit button.
- Existing posts are listed below and can be deleted with a single click.
- All changes are immediately saved to the `blog_data.json` file.

---

### Common Issues

- If the frontend returns **“Failed to fetch”**, check whether the backend is running and whether the correct URL was entered.
- In Codio, make sure to use the **full public HTTPS URL with the correct port**, not `127.0.0.1`.
- Seeing **“Pretty Print []”** in the browser usually means the list is empty or the wrong endpoint was used.
- The blinking button is **purely decorative** to guide user attention.

---

### API Endpoints for Testing

- `GET /api/posts` – returns a list of all blog posts  
- `POST /api/posts` – creates a new blog post  
- `DELETE /api/posts/<id>` – deletes a blog post by ID

---

### Data Storage

All blog data is stored in a file named `blog_data.json` inside the `backend` folder.  
The file is automatically created at startup if it does not exist.

---

### License and Contribution

This project was developed as part of a **training program** and is intended for **educational purposes**.  
It is licensed under the **MIT License**, which means it is open for reuse and modification.

Feel free to reach out if you're interested in contributing or discussing improvements!

---

### Conclusion

This project demonstrates a full cycle of web development using a **RESTful API** and a **dynamic client interface**.  
It is a **beginner-friendly** yet complete example for understanding how modern web applications communicate and handle data.
