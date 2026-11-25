# Metamorphosis

**Metamorphosis** is a web-based currency conversion and money transfer platform designed to help users conveniently convert foreign currencies into Philippine Pesos (PHP) without visiting physical currency exchange booths.

## Implemented Features

### Standard Account Features (Project Development 1)
- **Account Registration:** User registration with email uniqueness validation, password confirmation, and hashed password storage.
- **Login / Logout:** Session authentication with POST logout and `@login_required` protection.
- **Role-Based Dashboards:** Separate dashboards and backend access checks for **Customer** and **Admin** roles.
- **User Profile:** View and edit profile details and avatar uploads scoped strictly to the logged-in user.

### Core Feature (Project Development 2)
- **PHP Currency Conversion (Full Vertical Slice):**
  - Convert foreign currencies (`USD`, `EUR`, `GBP`, `JPY`, `AUD`, `SGD`, `CAD`) into Philippine Pesos (`PHP`).
  - Full CRUD support (Create, Read, Update, Delete) persisted in PostgreSQL/Supabase.
  - Input validation for positive amounts and exchange rates with clear success/error alerts.
  - Ownership and role-based access: Customers manage their own conversion records; Admins can view and manage all conversion records.

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone [https://github.com/](https://github.com/)ravenelleceleres/Metamorphosis-Celeres-Ravenelle-G2.git
   cd Metamorphosis-Celeres-Ravenelle-G2