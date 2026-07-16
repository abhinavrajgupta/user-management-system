## 🚀 Testing API Endpoints via Swagger UI

This project exposes a FastAPI backend with built-in Swagger documentation, so the easiest way to verify the API is to run the backend locally and test each endpoint in the browser at `http://localhost:9000/docs`.[1]

### What this section covers

This guide walks through:

- Cloning the repository.[1]
- Starting the backend locally with `uvicorn simple_server:app --host 0.0.0.0 --port 9000 --reload`.[1]
- Opening Swagger UI at `http://localhost:9000/docs`.[1]
- Registering a user, logging in, copying the JWT token, and authorizing protected routes.[1]
- Testing GET, POST, and DELETE endpoints with both valid and invalid payloads based on the documented API flow.[1]
- Verifying that the SQLite database file `demo.db` is being updated during API calls.[1]

### Prerequisites

Make sure the following are installed on your machine:

- Python 3.9 or newer.[1]
- `pip`.[1]
- Git.[1]
- Optional: a virtual environment tool such as `venv`.[1]

***

### 1. Clone the repository

```bash
git clone https://github.com/abhinavrajgupta/user-management-system.git
cd user-management-system
```

***

### 2. Move into the backend folder

The FastAPI app runs from the `backend/` directory.[1]

```bash
cd backend
```

***

### 3. Create and activate a virtual environment

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

***

### 4. Install backend dependencies

Install dependencies from the requirements file.[1]

```bash
pip install -r requirements.txt
```

If you want to install packages manually, the README also documents FastAPI, Uvicorn, SQLAlchemy, bcrypt, `python-jose[cryptography]`, Pydantic, `python-dotenv`, and `pymysql` as required backend packages.[1]

***

### 5. Create the environment file

Create a file named `.env` inside the `backend/` folder.

Example:

```env
DATABASE_URL=sqlite:///./demo.db
SECRET_KEY=supersecretkey
```

The README documents SQLite `demo.db` for local backend testing, and the file is expected to be created automatically after the backend starts successfully.[1]

***

### 6. Start the FastAPI server

Run the backend with Uvicorn using the documented startup command.[1]

```bash
uvicorn simple_server:app --host 0.0.0.0 --port 9000 --reload
```

Expected result:

```text
Uvicorn running on http://0.0.0.0:9000
```

Once the server starts, the API base URL is `http://localhost:9000` and Swagger UI is available at `http://localhost:9000/docs`.[1]

***

## Available API Endpoints

The repository README documents the following routes for the backend workflow.[1]

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check endpoint.[1] |
| POST | `/api/auth/register` | Register a new user.[1] |
| POST | `/api/auth/login` | Authenticate a user and return a JWT token.[1] |
| GET | `/api/users` | Fetch all users, typically protected.[1] |
| GET | `/api/users/{user_id}` | Fetch one user by ID, typically protected.[1] |
| DELETE | `/api/users/{user_id}` | Delete a user by ID, typically protected.[1] |

***

## Step-by-step Swagger workflow

### Step 1: Test the health route

In Swagger UI:

1. Expand `GET /`.
2. Click **Try it out**.
3. Click **Execute**.

**Good test case**

No request body is required for this endpoint, so a successful response confirms that the FastAPI server is running and reachable.[1]

**Bad test case**

If `GET /` fails, the main problem is usually that the backend is not running or is running on a different port than `9000`.[1]

***

### Step 2: Register a new user with `POST /api/auth/register`

In Swagger UI:

1. Expand `POST /api/auth/register`.
2. Click **Try it out**.
3. Use one of the request bodies below.
4. Click **Execute**.

#### Good registration input

```json
{
  "username": "demo_user",
  "email": "demo_user@example.com",
  "password": "Demo1234!"
}
```

**Expected result**

A success response means the user was created and stored in the local database flow described by the README.[1]

#### More good registration examples

```json
{
  "username": "alice01",
  "email": "alice01@example.com",
  "password": "StrongPass123!"
}
```

```json
{
  "username": "bob_dev",
  "email": "bob.dev@example.com",
  "password": "Secure987@"
}
```

#### Bad registration inputs to test

**Case 1: Duplicate username or email**

```json
{
  "username": "demo_user",
  "email": "demo_user@example.com",
  "password": "Demo1234!"
}
```

This should fail if the backend enforces uniqueness, which is the normal behavior for a user registration flow even though the exact validation text is not fully visible in the page capture.[1]

**Case 2: Missing field**

```json
{
  "username": "missing_email",
  "password": "Demo1234!"
}
```

FastAPI and Pydantic usually reject missing required fields in documented request schemas, so this is a useful negative test for request validation.[1]

**Case 3: Invalid email shape**

```json
{
  "username": "bad_email_user",
  "email": "not-an-email",
  "password": "Demo1234!"
}
```

Use this to check whether email validation exists in the route schema or backend logic.[1]

**Case 4: Empty strings**

```json
{
  "username": "",
  "email": "",
  "password": ""
}
```

This is a good boundary test to see whether the route only checks field presence or also checks content quality.

**Case 5: Very short password**

```json
{
  "username": "tiny_pass",
  "email": "tiny@example.com",
  "password": "123"
}
```

Use this to verify whether password-length or strength validation is enforced.

***

### Step 3: Log in with `POST /api/auth/login`

In Swagger UI:

1. Expand `POST /api/auth/login`.
2. Click **Try it out**.
3. Use credentials for a user that was already registered.
4. Click **Execute**.

#### Good login input

```json
{
  "username": "demo_user",
  "password": "Demo1234!"
}
```

**Expected result**

The README describes this route as returning an access token used for bearer authentication in protected routes.[1]

Example shape:

```json
{
  "access_token": "your_jwt_token_here",
  "token_type": "bearer"
}
```

#### Bad login inputs to test

**Case 1: Wrong password**

```json
{
  "username": "demo_user",
  "password": "WrongPassword123!"
}
```

This should fail and is the most important negative authentication test.

**Case 2: Unknown username**

```json
{
  "username": "user_does_not_exist",
  "password": "Demo1234!"
}
```

This should also fail because the account was never registered.

**Case 3: Missing password**

```json
{
  "username": "demo_user"
}
```

This should trigger request validation if the schema requires both username and password.

**Case 4: Empty payload values**

```json
{
  "username": "",
  "password": ""
}
```

This tests whether the endpoint rejects blank credentials instead of just missing keys.

***

### Step 4: Authorize Swagger with the JWT token

Protected endpoints require authentication.[1]

In Swagger UI:

1. Click the **Authorize** button near the top right.
2. Paste the token into the authorization field.
3. If Swagger expects the full bearer format, enter:

```text
Bearer your_jwt_token_here
```

4. Click **Authorize**.
5. Click **Close**.

**Good auth test**

After authorization, protected routes such as `GET /api/users`, `GET /api/users/{user_id}`, and `DELETE /api/users/{user_id}` should begin working if the token is valid.[1]

**Bad auth tests**

- Use no token at all.
- Use an expired or malformed token.
- Use `Bearer` with a truncated token string.

Those cases should return `401 Unauthorized` in a correct JWT-protected flow.

***

### Step 5: Test `GET /api/users`

In Swagger UI:

1. Expand `GET /api/users`.
2. Click **Try it out**.
3. Click **Execute**.

#### Good test case

Call the route after authorizing with a valid JWT token.[1]

**Expected result**

A successful response should return a JSON array of users stored through the registration flow.[1]

#### Bad test cases

**Case 1: No authorization header**

Execute the route before clicking **Authorize**.

**Expected result**

This should fail with an authentication error because the README indicates the route is protected.[1]

**Case 2: Invalid token**

Authorize Swagger with a fake or damaged token and retry the request.

**Expected result**

This should also fail with an authentication error in a correct JWT flow.

***

### Step 6: Test `GET /api/users/{user_id}`

In Swagger UI:

1. Expand `GET /api/users/{user_id}`.
2. Click **Try it out**.
3. Enter a user ID.
4. Click **Execute**.

#### Good test case

Use a real ID returned from `GET /api/users`.

Example:

```text
1
```

**Expected result**

A successful response should return details for that specific user when the ID exists.[1]

#### Bad test cases

**Case 1: Non-existent ID**

```text
9999
```

This should return a not-found style response if no user exists with that ID.

**Case 2: Invalid path value**

```text
abc
```

FastAPI path parameter typing should reject a non-integer user ID if the route expects an integer.

**Case 3: Negative ID**

```text
-1
```

Use this to see whether the route validates ID ranges in addition to type.

**Case 4: No token**

Run the request without authorization.

This should fail with `401 Unauthorized` if the route is protected as documented.[1]

***

### Step 7: Test `DELETE /api/users/{user_id}`

Use this route carefully because it removes a user from the database.[1]

In Swagger UI:

1. Expand `DELETE /api/users/{user_id}`.
2. Click **Try it out**.
3. Enter the target user ID.
4. Click **Execute**.

#### Good test case

Create a temporary test user, get its ID from `GET /api/users`, then delete that user.

Example user ID:

```text
2
```

**Expected result**

The user should be removed successfully and should no longer appear in the `GET /api/users` response.[1]

#### Bad test cases

**Case 1: Delete a user that does not exist**

```text
9999
```

This should return a not-found style response.

**Case 2: Invalid ID type**

```text
abc
```

This should be rejected by FastAPI path validation if the route expects an integer.

**Case 3: No authorization token**

Run the delete request without authorization.

This should fail with `401 Unauthorized` in a protected delete flow.[1]

**Case 4: Delete the same user twice**

Delete a valid user once, then immediately try deleting the same ID again.

The first call should succeed and the second should return a not-found style response because the record is already gone.

***

## Suggested end-to-end manual test script

Use this exact flow to validate the whole API in Swagger:

1. Start the backend with `uvicorn simple_server:app --host 0.0.0.0 --port 9000 --reload`.[1]
2. Open `http://localhost:9000/docs`.[1]
3. Test `GET /`.[1]
4. Register a new user with `POST /api/auth/register`.[1]
5. Log in with `POST /api/auth/login`.[1]
6. Copy the `access_token` value.[1]
7. Click **Authorize** and add the token as bearer auth.
8. Test `GET /api/users`.[1]
9. Test `GET /api/users/{user_id}` using an ID returned by the users list.[1]
10. Test `DELETE /api/users/{user_id}` on a temporary test account.[1]
11. Call `GET /api/users` again and confirm the deleted account is gone.

This sequence verifies server startup, Swagger access, POST registration, POST login, JWT authorization, protected GET routes, DELETE behavior, and database persistence through the documented local setup.[1]

***

## How to confirm the database is working

The local README flow documents SQLite with `DATABASE_URL=sqlite:///./demo.db`, and that means the backend creates and uses a local file named `demo.db` inside `backend/` during testing.[1]

Use these checks:

- Confirm that `backend/demo.db` appears after the backend starts.[1]
- Register a user and confirm that `GET /api/users` returns that user after login and authorization.[1]
- Delete a test user and confirm that the user disappears from the list route on the next request.[1]

***

## Good vs bad input summary

| Endpoint | Good input | Bad input examples | What to look for |
|---|---|---|---|
| `GET /` | No body needed. | Server not running, wrong port. | Should confirm API availability.[1] |
| `POST /api/auth/register` | Unique username, valid email, non-empty password. | Missing fields, duplicate username/email, invalid email, empty strings, very short password. | Should create a user or return validation/conflict errors. |
| `POST /api/auth/login` | Existing username + correct password. | Wrong password, unknown username, missing password, blank values. | Should return JWT or auth failure. |
| `GET /api/users` | Valid bearer token. | No token, invalid token. | Should return user list or `401`. |
| `GET /api/users/{user_id}` | Existing numeric ID + valid token. | `9999`, `abc`, `-1`, no token. | Should return record, validation error, not found, or `401`. |
| `DELETE /api/users/{user_id}` | Existing numeric ID + valid token. | `9999`, `abc`, no token, delete same user twice. | Should delete once, then fail cleanly after that. |

***

## Common problems and fixes

### Problem: `ModuleNotFoundError` or Uvicorn cannot find `simple_server`

Make sure you are inside the `backend/` directory before running the documented startup command.[1]

```bash
cd backend
uvicorn simple_server:app --host 0.0.0.0 --port 9000 --reload
```

### Problem: Swagger opens but protected routes return `401 Unauthorized`

The README flow requires using the token from `POST /api/auth/login` in Swagger authorization before testing protected endpoints.[1]

### Problem: `GET /api/users/{user_id}` returns not found

Use `GET /api/users` first, then copy a real ID from the list before testing the single-user route.

### Problem: `demo.db` is missing

Make sure `backend/.env` contains `DATABASE_URL=sqlite:///./demo.db` and that the backend actually started successfully.[1]
