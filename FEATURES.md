# CampusLore Features

## 1. Authentication and profile setup

- The app uses Django Allauth with Google OAuth.
- A custom social adapter rejects every email not ending in `@mail.jiit.ac.in`.
- First-time authenticated users are redirected to a profile completion form to enter their branch and year.
- This enforces the rule that all engagement is restricted to JIIT students only.

## 2. Public browsing model

- Visitors can browse the dashboard, question feed, question detail pages, search results, programs, and college information.
- No login is required for read-only access.
- Engagement actions such as asking questions, answering, voting, confirming, and reporting remain login-gated.

## 3. Question management

- Logged-in students can create new questions with a title, description, category, and tags.
- Questions are automatically assigned a random anonymous display name, such as `JIITIAN2345`.
- Only the original author may edit, delete, or mark a question as resolved.
- The question list supports filtering by category, status, and tags.

## 4. Answer and validation system

- Students can add answers to public questions.
- Answers also use random anonymous display names.
- Each answer can receive helpful/unhelpful votes.
- A separate confirmation action tracks whether users can verify an answer from personal experience.
- Contributor reputation is updated based on helpful votes and confirmations.

## 5. Search and recommendation features

- A global search bar scans question title, description, and tags.
- Search results are available from the main navigation and the public search page.
- AJAX search returns quick live results as the user types.
- Similar-question suggestions appear while the user types a new question title, helping reduce duplicate questions.

## 6. Dashboard and content overview

- The home page displays recent questions, popular questions, unanswered questions, and category statistics.
- Summary cards show the total number of questions, answers, and active contributors.
- The layout is intentionally minimal and built with Bootstrap.

## 7. Reporting workflow

- Authenticated users can report questions and answers.
- Reports are stored with a reason and review status.
- Every user can only report a piece of content once.
- Reports are available for superuser moderation in the admin dashboard.

## 8. Superuser reporting

- Superusers can access a dedicated admin reports page.
- It shows totals, recent activity, category stats, and pending report counts.
- CSV exports are available for:
  - questions by category
  - activity over the last 30 days
  - validation stats
- PDF exports generate a summary report for the platform.

## 9. Hardcoded college information

- The project includes hardcoded JIIT details from the provided college data file.
- These include:
  - campus addresses
  - contact information
  - leadership details
  - department heads and emails
  - official website and student portal URLs
- This information is displayed on the About JIIT page.

## 10. Programs page

- A dedicated Programs page lists program offerings and their departments.
- The data supports placeholder batch sizes that can be updated later when real values are available.

## 11. Seeded initial data

- The project includes a management command named `seed_data`.
- It populates initial categories and starter program records for the platform.

## 12. Admin and moderation tooling

- Django admin is configured for all core models.
- Custom admin actions allow report review and status updates.
- Access is restricted to superusers.
