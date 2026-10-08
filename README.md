#  SecureGate Auth (Identity & Access Management Engine)

An intermediate, security-hardened Django application engineered to implement a complete **Identity and Access Management (IAM)** infrastructure. The system eradicates the risk of plaintext credential leaks by integrating one-way cryptographic encryption salts, manages duplicate account collision through strict database-level unique constraints, and enforces stateful user tracking utilizing secure browser session tokens.

---

## 📈 System Architectural Layout & Lifecycle Flow

Project 5 orchestrates user authenticity screening across a three-tier defensive security pipeline:

```text
[ Registration UI ] ➔ Validation Constraints ➔ Cryptographic Salting (make_password) ➔ DB Row Saved
                                                                                            │
[ Login Gateway ] ➔ DB Pointer Match ➔ Hash Verification Check (check_password) ➔ Session Token Bound
                                                                                            │
[ System Core ] ➔ Restrictive Dashboard Gate ➔ Valid Session Token Check ➔ Access Granted OR Bounced
```

###  1. User Registration & Password Hardening 
* **The Vulnerability Mitigation:** Standard application architectures that store passwords as plain text leave users vulnerable to database theft. This engine intercepts raw text input string payloads at the form boundary and applies Django's built-in cryptographic salting tool (`make_password`).
* **The Cryptographic Reality:** Passwords are converted into irreversible, one-way hashed strings (e.g., `pbkdf2_sha256$210000$...`) before they touch the physical server disk space. 

###  2. Credential Verification Engine
* **The Verification Mechanism:** Because passwords exist inside SQLite as unreadable scrambled hashes, standard string matching operators (`==`) cannot be used. 
* **The Check Engine:** The system employs Django's **`check_password`** utility. It mathematically re-hashes incoming login text parameters and safely matches them against the recorded database hash footprint without exposing user credentials.

###  3. Stateful Access Control & Restrictive Permissions
* **Session Wristband Tracking:** Upon successful verification, the backend assigns a stateful session tracking badge (`request.session['auth_user_id']`) to the client browser cookie array. 
* **Object-Level Protection Gate:** Implements a strict permission barrier on the dashboard profile workspace. If a random web user tries to bypass the login interface and types the direct path URL, the view detects the missing tracking badge, short-circuits the pipeline, and bounces them back to the login screen immediately.

---

##  Relational Database Schema Profile 

The identity database table structure runs under strict storage constraints:

### `SecAuth_Model` Database Table
* `name` (CharField, max_length=255): Stores applicant account display identifiers.
* `email` (EmailField, unique=True): **CRITICAL SHIELD** — Enforces a strict unique constraint at the SQLite table database level to permanently block account collision and duplicate registrations.
* `password` (CharField, max_length=255): Allocates highly indexed storage to hold long, cryptographically scrambled hash sequences securely.

---
## 💻 Tech Stack & Engineering Focus
* **Backend Core Framework:** Django 5.x / Python 3.x
* **Core Engineering Concepts Practiced:** Cryptographic Password Hashing Matrix, Stateful Browser Cookie Session Management, Custom Error Block Context Rendering, Route Protection Logic, Integrity Crash Prevention (`.filter().exists()`).
