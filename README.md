## 🚀 Testing API Endpoints via Swagger UI

This project exposes a FastAPI backend with built-in Swagger documentation, so the easiest way to verify the API is to run the backend locally and test each endpoint in the browser at `http://localhost:9000/docs`.[1]

### Important behavior from the current code

The current backend code loads `DATABASE_URL` from environment variables and only falls back to `sqlite:///./demo.db` if `DATABASE_URL` is not set.[2] The code also runs `Base.metadata.create_all(bind=engine)` at startup, so tables are created in whichever database your `DATABASE_URL` points to, including Railway if that is what you configured.[2]

Also, the current code does **not** enforce JWT authentication on `GET /api/users`, `GET /api/users/{user_id}`, or `DELETE /api/users/{user_id}` because those routes only depend on `get_db` and not on any token validation dependency.[2]

### What this section covers

This guide walks through:

- Starting the backend locally with the documented Uvicorn command.[1]
- Opening Swagger UI at `http://localhost:9000/docs`.[1]
- Registering a user and logging in to get a token.[2]
- Testing GET, POST, and DELETE endpoints with good and bad inputs based on the current code behavior.[2]
- Verifying data changes against a Railway-hosted database when `DATABASE_URL` is set to Railway.[2]

### Prerequisites

Make sure the following are installed on your machine:

- Python 3.9 or newer.
- `pip`.
- Git.
- Optional: a virtual environment tool such as `venv`.

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
venv\Scriptsctivate
```

***

### 4. Install backend dependencies

```bash
pip install -r requirements.txt
```

***

### 5. Configure environment variables

Create a file named `.env` inside the `backend/` folder.

Example:

```env
DATABASE_URL=<your Railway connection string>
SECRET_KEY=supersecretkey
```

The current code reads `DATABASE_URL` from the environment first, so if you use a Railway connection string, all inserts, reads, and deletes happen in Railway rather than in a local SQLite file.[2]

***

### 6. Start the FastAPI server

Run the backend with Uvicorn:

```bash
uvicorn simple_server:app --host 0.0.0.0 --port 9000 --reload
```

Once the server starts, the API base URL is `http://localhost:9000` and Swagger UI is available at `http://localhost:9000/docs`.[1]

***

## Available API Endpoints

The current code exposes the following routes.[2]

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check route that returns a running message.[2] |
| POST | `/api/auth/register` | Registers a user and immediately returns a bearer token.[2] |
| POST | `/api/auth/login` | Validates credentials and returns a bearer token.[2] |
| GET | `/api/users` | Lists all users.[2] |
| GET | `/api/users/{user_id}` | Returns one user by integer ID.[2] |
| DELETE | `/api/users/{user_id}` | Deletes one user by integer ID.[2] |

***

## Step-by-step Swagger workflow

### Step 1: Test the health route

1. Open Swagger UI at `http://localhost:9000/docs`.[1]
2. Expand `GET /`.
3. Click **Try it out** and then **Execute**.

**Expected result**

The route should return `{"message": "User Management API is running"}` based on the current code.[2]

***

### Step 2: Register a user with `POST /api/auth/register`

Use a valid JSON body like this:

```json
{
  "username": "demo_user",
  "email": "demo_user@example.com",
  "password": "Demo1234!"
}
```

**Expected result**

The route checks whether either the username or email already exists, creates the user, hashes the password with bcrypt, stores the row, and returns an access token plus `token_type: bearer`.[2]

#### Good registration test cases

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

#### Bad registration test cases

**Duplicate username or email**

```json
{
  "username": "demo_user",
  "email": "demo_user@example.com",
  "password": "Demo1234!"
}
```

The current code explicitly returns `400` with `"Username or email already exists"` when a matching username or email is found.[2]

**Missing field**

```json
{
  "username": "missing_email",
  "password": "Demo1234!"
}
```

Pydantic request validation should reject a missing required field because `UserCreate` requires `username`, `email`, and `password`.[2]

**Blank values**

```json
{
  "username": "",
  "email": "",
  "password": ""
}
```

The current Pydantic model uses plain `str` fields without extra validation constraints, so blank strings may still pass schema validation and should be tested as a code-quality edge case.[2]

**Invalid email format**

```json
{
  "username": "bad_email_user",
  "email": "not-an-email",
  "password": "Demo1234!"
}
```

The current model uses `email: str`, not an email-specific Pydantic type, so this may be accepted unless additional validation is added later.[2]

***

### Step 3: Log in with `POST /api/auth/login`

Use a registered username and password:

```json
{
  "username": "demo_user",
  "password": "Demo1234!"
}
```

**Expected result**

The code looks up the user by username, verifies the password with bcrypt, and returns an access token on success.[2]

#### Bad login test cases

**Wrong password**

```json
{
  "username": "demo_user",
  "password": "WrongPassword123!"
}
```

The current code returns `401` with `"Invalid credentials"` if the password check fails.[2]

**Unknown username**

```json
{
  "username": "user_does_not_exist",
  "password": "Demo1234!"
}
```

The current code also returns `401` with `"Invalid credentials"` if no matching username exists.[2]

**Missing password**

```json
{
  "username": "demo_user"
}
```

This should fail request validation because `UserLogin` requires both `username` and `password`.[2]

***

### Step 4: Test `GET /api/users`

Open `GET /api/users` in Swagger and click **Execute**.

**Expected result**

The route returns all users as a JSON list with `id`, `username`, `email`, `is_active`, and `created_at` fields.[2]

**Important note**

Despite the app having login and token-generation routes, the current `GET /api/users` route does not require JWT authentication in the code.[2]

#### Good test case

- Run the route after registering one or more users, and confirm the returned list includes them.[2]

#### Bad or edge test case

- Run the route before any users are created and confirm it returns an empty list rather than failing, because the route simply queries all rows from the `users` table.[2]

***

### Step 5: Test `GET /api/users/{user_id}`

Use a real numeric ID returned from `GET /api/users`.

Example:

```text
1
```

**Expected result**

The route returns one user object when the ID exists.[2]

#### Bad test cases

**Non-existent ID**

```text
9999
```

The current code returns `404` with `"User not found"` if the queried ID does not exist.[2]

**Invalid path type**

```text
abc
```

The route signature declares `user_id: int`, so FastAPI should reject a non-integer path parameter before the query runs.[2]

**Negative ID**

```text
-1
```

This should query the table and then return `404` if no row exists with that ID, because the code does not add a separate positive-range validation step.[2]

***

### Step 6: Test `DELETE /api/users/{user_id}`

Use a real numeric ID from `GET /api/users`.

Example:

```text
2
```

**Expected result**

The current code deletes the matching user, commits the transaction, and returns `{"message": "User deleted successfully"}`.[2]

#### Good delete test case

- Create a temporary user, confirm it appears in `GET /api/users`, delete it with `DELETE /api/users/{user_id}`, and then re-run `GET /api/users` to confirm it is gone.[2]

#### Bad delete test cases

**Delete a user that does not exist**

```text
9999
```

The current code returns `404` with `"User not found"` when no matching row exists.[2]

**Invalid ID type**

```text
abc
```

FastAPI should reject the request because the route expects an integer `user_id`.[2]

**Delete the same user twice**

Delete a valid user once, then send the same delete request again.

The first call should succeed and the second should return `404` because the row is already gone.[2]

***

## Railway database verification

If your `.env` sets `DATABASE_URL` to Railway, then the app is using Railway and not creating a local SQLite file, because the code uses the environment value first and only falls back to `sqlite:///./demo.db` when `DATABASE_URL` is absent.[2]

Use this validation flow:

1. Register a new test user with `POST /api/auth/register`.[2]
2. Confirm the new row appears in `GET /api/users`.[2]
3. Fetch the same user with `GET /api/users/{user_id}`.[2]
4. Delete that user with `DELETE /api/users/{user_id}`.[2]
5. Confirm the record is gone from `GET /api/users`.[2]

That proves inserts, reads, and deletes are happening against the Railway-hosted database used by `DATABASE_URL`.[2]

***

## Good vs bad input summary

| Endpoint | Good input | Bad input examples | What current code suggests |
|---|---|---|---|
| `GET /` | No body needed. | Server not running, wrong port. | Should return a running message.[2] |
| `POST /api/auth/register` | Unique username, any string email, non-empty password. | Duplicate username/email, missing fields, blank strings, invalid email shape. | Duplicate check exists; strong field validation is limited.[2] |
| `POST /api/auth/login` | Existing username and correct password. | Wrong password, unknown username, missing password. | Invalid credentials return `401`.[2] |
| `GET /api/users` | No auth required in current code. | Empty dataset is a useful edge case. | Returns list of users.[2] |
| `GET /api/users/{user_id}` | Existing numeric ID. | `9999`, `abc`, `-1`. | Returns user or `404`; type errors fail earlier.[2] |
| `DELETE /api/users/{user_id}` | Existing numeric ID. | `9999`, `abc`, deleting same user twice. | Deletes once, then `404` after row is gone.[2] |

***

## Common problems and fixes

### Problem: No local `demo.db` file appears

That is expected if `DATABASE_URL` is set to Railway or any non-SQLite database URL, because the code only uses local SQLite as a fallback default.[2]

### Problem: Registration works but no protected auth is needed on user routes

That is also expected from the current code because the list, get-by-id, and delete routes do not include a token-check dependency.[2]

### Problem: Invalid email still gets accepted

That can happen because the current `UserCreate` model uses `email: str` instead of a stricter email validation type.[2]
