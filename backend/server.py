from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client

# Supabase connection
SUPABASE_URL = "https://phoelhjhfpvawdwywtxx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBob2VsaGpoZnB2YXdkd3l3dHh4Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MTk5NTk3OCwiZXhwIjoyMDc3NTcxOTc4fQ.xN3Y6PaghIrP3ely9bgeryXvyvj8_cvFmSQDI8IFStU"

app = FastAPI()

# CORS setup to allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to ["http://localhost:3000"] for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


@app.get("/")
def read_root():
    return {"message": "Backend running successfully!"}


@app.get("/meeting-summary")
def get_meeting_summary():
    try:
        # Fetch recent meetings from the correct table: "transcripts"
        response = (
            supabase.table("transcripts")
            .select("meeting_name, summary, tasks, pending_tasks, created_at")
            .order("created_at", desc=True)
            .limit(5)
            .execute()
        )

        if response.data:
            return {"data": response.data}
        else:
            return {"message": "No meeting summaries found."}
    except Exception as e:
        return {"error": str(e)}
