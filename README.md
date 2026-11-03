# study-room

# Team · Study Room Slot Booking

| Team | Partner 1 | Partner 2 | Partner 3 | Project |
|---|---|---|---|---|
| [number] | Toshimah | Harsita | Rehaan | Study Room Slot Booking |

Every 3 hours: update this file, then commit and push it with the message `Check-in Day 1 12:00` (your day and time). Your instructor reads this page on GitHub.

## 1. Who is doing what

Update your own row at every check-in.

| Day | Partner | What will you do? | Completed? | What are you going to work on next? | Stuck on? |
|---|---|---|---|---|---|
| Day 1 | Toshimah | Build the room endpoints (E7–E9) , The database and starting data | | Test all the rules in /doc | |
| Day 1 | Harsita | Build the room endpoints (E1–E3) | | Test the room endpoints and help test the booking rules | |
| Day 1 | Rehaan | Set up GitHub, the project,Build the booking endpoints (E4–E6) and the booking rules | | Fix bugs from testing | |
| Day 2 | Toshimah | | | | |
| Day 2 | Harsita | | | | |
| Day 2 | Rehaan | | | | |
| Day 3 | Toshimah | | | | |
| Day 3 | Harsita | | | | |
| Day 3 | Rehaan | | | | |

## 2. Endpoint tracker

Status: ✅ done · 🟡 in progress · ⬜ not started

| # | Method + path | Built | Rules checked in /docs | Connected to React | Who |
|---|---|---|---|---|---|
| E1 |  | ⬜ | ⬜ | ⬜ | Harsita |
| E2 |  | ⬜ | ⬜ | ⬜ | Harsita |
| E3 |  | ⬜ | ⬜ | ⬜ | Harsita |
| E4 |  | ⬜ | ⬜ | ⬜ | Rehaan |
| E5 |  | ⬜ | ⬜ | ⬜ | Rehaan |
| E6 |  | ⬜ | ⬜ | ⬜ | Rehaan |
| E7 |  | ⬜ | ⬜ | ⬜ | Toshimah |
| E8 |  | ⬜ | ⬜ | ⬜ | Toshimah |
| E9 |  | ⬜ | ⬜ | ⬜ | Toshimah |

## 3. Frontend tracker

| Part (from section 5 of your PRD) | Shows the data | Buttons work | Shows API errors | Who |
|---|---|---|---|---|
| Rooms | ⬜ | ⬜ | ⬜ | |
| My bookings | ⬜ | ⬜ | ⬜ | |
| Manage rooms | ⬜ | ⬜ | ⬜ | |

## 4. Blockers and help needed

None yet.

## 5. How to run our app

**Backend**

```bash
cd backend
python -m venv venv
```

Turn on the virtual environment:

```bash
# Windows
venv\Scripts\activate

# Mac or Linux
source venv/bin/activate
```

Install the packages and start the API:

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

Open <http://127.0.0.1:8001/docs> to test it.

To reset the data, stop the server, delete `backend/studyrooms.db`, and start the server again.

**Frontend**

Fill this in by the end of Day 2.

```bash
cd frontend
```

## 6. Proof of work

Save a screenshot of /docs or your app as `screenshot.png` in this branch. It shows here:

![Our app](screenshot.png)
