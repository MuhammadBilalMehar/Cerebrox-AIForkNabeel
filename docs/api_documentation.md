# CerebroX AI — API Documentation

All endpoints use Django session authentication (login via `/accounts/login/`
or `POST /api/auth/login/`) and return JSON. Every endpoint below only ever
returns/affects **the logged-in student's own** courses, topics, notes, and
quizzes — there is no endpoint that lists another student's content.

## Auth — `/api/auth/`
| Method | Path | Description |
|---|---|---|
| POST | `/api/auth/register/` | Create a student account `{username, email, password, first_name, last_name}` |
| POST | `/api/auth/login/` | `{username, password}` |
| POST | `/api/auth/logout/` | Log out the current session |
| GET | `/api/auth/me/` | Current user profile, incl. `study_level` |

## Learning — `/api/learning/`
| Method | Path | Description |
|---|---|---|
| GET/POST | `/api/learning/courses/` | List/create **your own** courses |
| GET/PUT/DELETE | `/api/learning/courses/<id>/` | Manage one of your own courses |
| GET/POST | `/api/learning/topics/?course=<id>` | List/create topics within one of your courses |
| GET | `/api/learning/notes/` | Your own AI-generated notes |

## AI — `/api/ai/`
| Method | Path | Description |
|---|---|---|
| POST | `/api/ai/notes/generate/` | `{topic_id, length}` → generates notes using your Course + Topic + current Study Level, stores an AINote |
| POST | `/api/ai/mcq/generate/` | `{topic_id, difficulty, count}` → returns generated questions (not yet stored) using Course + Topic + Study Level + Difficulty |

## Quizzes — `/quizzes/api/`
| Method | Path | Description |
|---|---|---|
| POST | `/quizzes/api/generate/` | `{topic_id, difficulty, num_questions}` → creates + stores a full quiz for one of your own topics |
| POST | `/quizzes/api/<id>/submit/` | `{answers: {question_id: "A"}}` → scores the quiz |
| GET | `/quizzes/api/<id>/` | Quiz detail incl. score/percentage/study_level used |

## Analytics — `/analytics/api/`
| Method | Path | Description |
|---|---|---|
| GET | `/analytics/api/performance/` | Overview + topic/**course** breakdown |
| GET | `/analytics/api/weak-topics/` | Weak / strong topic lists |
| GET | `/analytics/api/recommendations/` | Personalized recommendation per topic |

## Dashboard — `/api/dashboard/summary/`
GET — total quizzes, average/highest/lowest score.
