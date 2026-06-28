"""
Seed the database with sample meetings when it is empty.

Run from the backend directory:

    python seed.py
"""

from datetime import datetime

from sqlalchemy import func, select

from app.database import SessionLocal, init_db
from app.models.action_item import ActionItem
from app.models.meeting import Meeting
from app.models.participant import Participant
from app.models.transcript import Transcript


def _distribute_transcript_timestamps(meeting: Meeting) -> None:
    """Assign evenly spaced timestamps from meeting start through the final minutes."""
    transcripts = meeting.transcripts
    if not transcripts:
        return

    total_seconds = meeting.duration * 60
    end_buffer_seconds = 150  # last entry within ~2.5 minutes of meeting end
    end_seconds = max(0, total_seconds - end_buffer_seconds)
    count = len(transcripts)

    if count == 1:
        transcripts[0].timestamp = 0
        return

    for index, entry in enumerate(transcripts):
        entry.timestamp = round(end_seconds * index / (count - 1))


def _build_meetings() -> list[Meeting]:
    """Return five realistic meetings with related records."""
    return [
        Meeting(
            title="Q2 Product Roadmap Review",
            meeting_date=datetime(2026, 5, 12, 14, 0),
            duration=52,
            summary=(
                "The team aligned on Q2 priorities, focusing on transcription accuracy, "
                "speaker identification, and a self-serve onboarding flow. Engineering "
                "capacity was reserved for two major releases in June and July."
            ),
            key_topics="Roadmap, Transcription accuracy, Speaker ID, Onboarding, Q2 goals",
            participants=[
                Participant(name="Sarah Chen", email="sarah.chen@company.com"),
                Participant(name="Marcus Webb", email="marcus.webb@company.com"),
                Participant(name="Priya Nair", email="priya.nair@company.com"),
                Participant(name="James Okafor", email="james.okafor@company.com"),
            ],
            transcripts=[
                Transcript(speaker="Sarah Chen", timestamp=0, text="Thanks everyone for joining. Let's walk through the Q2 roadmap and confirm what ships this quarter."),
                Transcript(speaker="Marcus Webb", timestamp=42, text="Transcription accuracy is still the top customer request. We should prioritize the new diarization model."),
                Transcript(speaker="Priya Nair", timestamp=98, text="Agreed. If we land speaker ID improvements in June, marketing can run a launch campaign in July."),
                Transcript(speaker="James Okafor", timestamp=156, text="From a design perspective, onboarding needs fewer steps before a user sees their first summary."),
                Transcript(speaker="Sarah Chen", timestamp=210, text="Let's lock June for speaker ID and July for onboarding. Marcus, can you share a rough estimate?"),
                Transcript(speaker="Marcus Webb", timestamp=268, text="Two sprints for speaker ID if we keep scope tight. Onboarding is closer to three."),
                Transcript(speaker="Priya Nair", timestamp=320, text="I'll draft the external messaging once engineering confirms dates."),
                Transcript(speaker="Sarah Chen", timestamp=372, text="Great. We'll revisit resourcing next week after the sprint review."),
            ],
            action_items=[
                ActionItem(task="Share speaker ID implementation estimate by Friday", assigned_to="Marcus Webb"),
                ActionItem(task="Draft Q2 launch messaging outline", assigned_to="Priya Nair"),
                ActionItem(task="Audit onboarding flow and propose wireframes", assigned_to="James Okafor"),
                ActionItem(task="Schedule resourcing follow-up for next Tuesday", assigned_to="Sarah Chen"),
            ],
        ),
        Meeting(
            title="Engineering Sprint Planning",
            meeting_date=datetime(2026, 5, 19, 10, 30),
            duration=45,
            summary=(
                "Sprint 14 planning covered API pagination, meeting search indexing, and "
                "bug fixes from the last release. The team committed to 34 story points "
                "with one engineer on-call rotation."
            ),
            key_topics="Sprint planning, API pagination, Search indexing, Bug fixes",
            participants=[
                Participant(name="Marcus Webb", email="marcus.webb@company.com"),
                Participant(name="Elena Rodriguez", email="elena.rodriguez@company.com"),
                Participant(name="Tom Hughes", email="tom.hughes@company.com"),
                Participant(name="Aisha Khan", email="aisha.khan@company.com"),
                Participant(name="Ryan Park", email="ryan.park@company.com"),
            ],
            transcripts=[
                Transcript(speaker="Marcus Webb", timestamp=0, text="Welcome to sprint planning. Carry-over from last sprint is the pagination bug on meetings list."),
                Transcript(speaker="Elena Rodriguez", timestamp=38, text="I can take pagination. It's mostly cursor-based paging and test coverage."),
                Transcript(speaker="Tom Hughes", timestamp=92, text="Search indexing depends on pagination landing first. I'll start schema changes in parallel."),
                Transcript(speaker="Aisha Khan", timestamp=145, text="I'll pick up the transcript export timeout bug. Repro steps are in ticket 482."),
                Transcript(speaker="Ryan Park", timestamp=198, text="I'm on-call this sprint, so I'm limiting commitment to support and small fixes."),
                Transcript(speaker="Marcus Webb", timestamp=250, text="Sounds good. Elena, what's your point estimate for pagination?"),
                Transcript(speaker="Elena Rodriguez", timestamp=288, text="Eight points including integration tests and docs."),
                Transcript(speaker="Tom Hughes", timestamp=330, text="Search indexing is thirteen points if we include backfill for existing meetings."),
                Transcript(speaker="Marcus Webb", timestamp=378, text="Let's cap the sprint at thirty-four points and move backfill to a stretch goal."),
            ],
            action_items=[
                ActionItem(task="Implement cursor-based pagination for meetings API", assigned_to="Elena Rodriguez"),
                ActionItem(task="Fix transcript export timeout bug", assigned_to="Aisha Khan"),
                ActionItem(task="Draft search index migration plan", assigned_to="Tom Hughes"),
            ],
        ),
        Meeting(
            title="Client Discovery Call — Acme Corp",
            meeting_date=datetime(2026, 5, 22, 16, 0),
            duration=38,
            summary=(
                "Acme Corp's sales and customer success teams need searchable meeting "
                "archives, CRM integrations, and role-based access. They are evaluating "
                "vendors and want a pilot with twenty users next month."
            ),
            key_topics="Enterprise pilot, CRM integration, RBAC, Search, Acme Corp",
            participants=[
                Participant(name="Sarah Chen", email="sarah.chen@company.com"),
                Participant(name="David Miller", email="david.miller@acmecorp.com"),
                Participant(name="Lisa Tran", email="lisa.tran@acmecorp.com"),
                Participant(name="Priya Nair", email="priya.nair@company.com"),
            ],
            transcripts=[
                Transcript(speaker="Sarah Chen", timestamp=0, text="Thanks for making time today. We'd love to understand how your teams use meeting notes today."),
                Transcript(speaker="David Miller", timestamp=45, text="Our reps record calls manually and paste summaries into Salesforce. It's slow and inconsistent."),
                Transcript(speaker="Lisa Tran", timestamp=102, text="Customer success needs searchable archives by account and rep. We lose context between handoffs."),
                Transcript(speaker="Priya Nair", timestamp=158, text="We support Salesforce and HubSpot integrations on our enterprise tier, plus keyword search across all transcripts."),
                Transcript(speaker="David Miller", timestamp=215, text="Role-based access is important. Managers should see their team's meetings, not the whole company."),
                Transcript(speaker="Sarah Chen", timestamp=268, text="We can scope a twenty-user pilot with SSO and RBAC enabled. Does that match your timeline?"),
                Transcript(speaker="Lisa Tran", timestamp=318, text="Yes, we'd want to start in June if security review moves quickly."),
                Transcript(speaker="Sarah Chen", timestamp=355, text="Perfect. We'll send a pilot proposal and security documentation by end of week."),
            ],
            action_items=[
                ActionItem(task="Send Acme Corp pilot proposal and pricing", assigned_to="Sarah Chen"),
                ActionItem(task="Prepare SSO and RBAC documentation for security review", assigned_to="Priya Nair"),
                ActionItem(task="Share sample CRM integration architecture diagram", assigned_to="Sarah Chen"),
                ActionItem(task="Schedule follow-up demo with Acme sales leadership", assigned_to="Priya Nair"),
            ],
        ),
        Meeting(
            title="Weekly Team Standup",
            meeting_date=datetime(2026, 5, 26, 9, 0),
            duration=22,
            summary=(
                "Quick sync on progress: pagination merged, search indexing in review, "
                "and design handoff for the dashboard refresh. No blockers reported."
            ),
            key_topics="Standup, Pagination, Search indexing, Dashboard design",
            participants=[
                Participant(name="Elena Rodriguez", email="elena.rodriguez@company.com"),
                Participant(name="Tom Hughes", email="tom.hughes@company.com"),
                Participant(name="James Okafor", email="james.okafor@company.com"),
                Participant(name="Aisha Khan", email="aisha.khan@company.com"),
            ],
            transcripts=[
                Transcript(speaker="Elena Rodriguez", timestamp=0, text="Pagination PR merged last night. Monitoring error rates today."),
                Transcript(speaker="Tom Hughes", timestamp=28, text="Search indexing PR is in review. I need one more approval before merge."),
                Transcript(speaker="James Okafor", timestamp=58, text="Dashboard refresh mockups are ready. I'll share Figma links after standup."),
                Transcript(speaker="Aisha Khan", timestamp=92, text="Export timeout fix is deployed to staging. QA signed off this morning."),
                Transcript(speaker="Elena Rodriguez", timestamp=125, text="No blockers on my side."),
                Transcript(speaker="Tom Hughes", timestamp=148, text="Same here. Just waiting on review."),
                Transcript(speaker="James Okafor", timestamp=172, text="I'll need feedback on dashboard nav by Thursday."),
                Transcript(speaker="Aisha Khan", timestamp=198, text="All good. I'll pick up the next bug from the backlog."),
            ],
            action_items=[
                ActionItem(task="Monitor pagination rollout metrics", assigned_to="Elena Rodriguez"),
                ActionItem(task="Share dashboard refresh Figma links with the team", assigned_to="James Okafor"),
                ActionItem(task="Chase second approval on search indexing PR", assigned_to="Tom Hughes"),
            ],
        ),
        Meeting(
            title="AI Feature Brainstorm",
            meeting_date=datetime(2026, 6, 3, 15, 30),
            duration=61,
            summary=(
                "Brainstormed AI-powered features including auto-generated meeting briefs, "
                "sentiment tracking, and smart action item detection. The group prioritized "
                "briefs for the next prototype and deferred sentiment analysis."
            ),
            key_topics="AI briefs, Sentiment analysis, Action item detection, Prototype",
            participants=[
                Participant(name="Sarah Chen", email="sarah.chen@company.com"),
                Participant(name="Marcus Webb", email="marcus.webb@company.com"),
                Participant(name="Priya Nair", email="priya.nair@company.com"),
                Participant(name="Ryan Park", email="ryan.park@company.com"),
                Participant(name="Lisa Tran", email="lisa.tran@acmecorp.com"),
            ],
            transcripts=[
                Transcript(speaker="Sarah Chen", timestamp=0, text="Goal for today is to pick one AI feature for a quick prototype this month."),
                Transcript(speaker="Ryan Park", timestamp=35, text="Auto-generated meeting briefs could save users ten minutes after every call."),
                Transcript(speaker="Marcus Webb", timestamp=78, text="We already have summaries. Briefs could combine summary, decisions, and action items in one view."),
                Transcript(speaker="Priya Nair", timestamp=132, text="Customers also ask for sentiment tracking, but that's harder to explain and validate."),
                Transcript(speaker="Lisa Tran", timestamp=188, text="From a buyer perspective, briefs are easier to demo in a first meeting."),
                Transcript(speaker="Ryan Park", timestamp=240, text="Smart action item detection overlaps with briefs. We could extract tasks as part of the same pipeline."),
                Transcript(speaker="Marcus Webb", timestamp=295, text="Technically, one LLM pass can produce brief plus action items if we structure the prompt."),
                Transcript(speaker="Sarah Chen", timestamp=348, text="Let's prototype briefs with embedded action items and revisit sentiment in Q3."),
                Transcript(speaker="Priya Nair", timestamp=395, text="I'll validate messaging with three design partners next week."),
                Transcript(speaker="Ryan Park", timestamp=430, text="I can spike the prompt template and evaluation set by Monday."),
                Transcript(speaker="Sarah Chen", timestamp=465, text="Great work. We'll review the spike in next week's product sync."),
            ],
            action_items=[
                ActionItem(task="Spike LLM prompt for meeting briefs and action items", assigned_to="Ryan Park"),
                ActionItem(task="Interview three design partners on briefs UX", assigned_to="Priya Nair"),
                ActionItem(task="Define evaluation criteria for brief quality", assigned_to="Marcus Webb"),
                ActionItem(task="Add AI briefs to Q3 roadmap draft", assigned_to="Sarah Chen"),
                ActionItem(task="Document deferred sentiment analysis requirements", assigned_to="Priya Nair", completed=False),
            ],
        ),
    ]


def seed() -> None:
    """Insert sample meetings when the database has no meeting rows."""
    init_db()
    db = SessionLocal()

    try:
        meeting_count = db.scalar(select(func.count()).select_from(Meeting)) or 0
        if meeting_count > 0:
            print(f"Database already contains {meeting_count} meeting(s). Skipping seed.")
            return

        meetings = _build_meetings()
        for meeting in meetings:
            _distribute_transcript_timestamps(meeting)
        db.add_all(meetings)
        db.commit()
        print(f"Seeded {len(meetings)} meetings with participants, transcripts, and action items.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
