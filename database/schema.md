# CerebroX AI — Database Schema

SQLite (default, per FYP scope §21 cost-reduction strategy). All tables use Django's default `id` BigAutoField primary key unless noted.

## User (apps.accounts) — extends Django's AbstractUser
| Field | Type | Notes |
|---|---|---|
| username, first_name, last_name, email, password | inherited | Django auth defaults |
| role | CharField | `student` \| `admin` |
| study_level | CharField | `matric` \| `intermediate` \| `undergraduate` \| `graduate` \| `other` — drives AI note/quiz generation |
| study_level_custom | CharField(60) | Free text used only when `study_level = 'other'` |
| bio | CharField(255) | optional |
| avatar | ImageField | optional, `media/profiles/` |
| xp_points | PositiveInteger | gamification (Module 17) |
| created_at | DateTime | auto |

`effective_study_level` (property, not a DB column) resolves to
`study_level_custom` when `study_level == 'other'`, else the display label —
this is what's fed into AI prompts.

## Course (apps.learning) — **student-owned, not global**
student → FK User (CASCADE), name, description, icon (emoji), created_at —
`unique_together(student, name)`. Each student builds their own list; there is
no shared/predefined subject catalogue.

## Topic (apps.learning)
course → FK Course (CASCADE), name, description, created_at —
`unique_together(course, name)`. Ownership (`topic.student`) is derived via
`topic.course.student`.

## AINote (apps.learning)
student → FK User, topic → FK Topic, study_level (snapshot string, e.g.
"Undergraduate" or a custom value), content (JSON: introduction, explanation,
key_terms, examples, important_points, summary), created_at

## Question (apps.quizzes)
topic → FK Topic, question, option_a..d, correct_answer (A/B/C/D), explanation, difficulty, ai_generated (bool), created_at

## Quiz (apps.quizzes)
student → FK User, topic → FK Topic, difficulty, study_level (snapshot at
generation time), total_questions, score, percentage, duration_seconds,
completed, created_at

## QuizAnswer (apps.quizzes)
quiz → FK Quiz, question → FK Question, selected_answer, correct — unique_together(quiz, question)

## Performance / Weak Topics
**Not stored as tables.** Calculated dynamically from Quiz/QuizAnswer history,
always scoped to the requesting student
(`apps/analytics/performance.py`, `weak_topics.py`).
