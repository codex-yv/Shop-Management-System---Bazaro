# Bazaro - Inventory & Shop Management System

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-green)
![MongoDB](https://img.shields.io/badge/Database-MongoDB-brightgreen)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-UI-orange)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-teal)
![Render](https://img.shields.io/badge/Hosting-Render-blueviolet)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)

## Overview
**Bazaro** is an intelligent and user-friendly inventory and shop management system designed for small to medium-sized businesses. It helps store owners manage their stock, sales, billing, customer relations, and more with powerful features and an intuitive GUI.

## About this branch
This branch **(bazaro/server-main)** is a production level branch based on **API** whose server is handled by render and github via CI/CD pipeline.
  

## Core Features

### ▶ Inventory Management
- Add, update, and delete products
- Real-time stock updates after sales
- Batch and expiry date tracking
- Low stock and expiry alerts
- Barcode scanner support

### ▶ Sales & Billing
- Quick and intuitive billing interface
- Apply discounts, taxes, and offers
- Accept multiple payment methods (Cash, Card, UPI)
- Print and save bills as PDF
- Real-time stock deduction
- Daily, Weekly, Monthly earning progress bar 

### ▶ Customer Management
- Manage customer profiles
- View customer purchase history

### ▶ Supplier Management (under development)
- Supplier profile creation 
- Purchase order generation
- Auto alerts for stock replenishment

### ▶ Reports & Analytics
- View daily, weekly, monthly sales (Real-time is Premium)
- Export inventory and analytics as Excel and PDF
- Graphical Visualisation of the Earnings based on <br>
   1) Daily Earnigs
   2) Weekly Earnigs (1-Months, 3-Months, 6-Months, 12-Months)
   3) Monthly Earnings

---

## Advanced Features

### ▶ Multi-Counter Support *(Available)*
- Centralized inventory for multiple counters
- Who sold what and Who added what --> can be analysed in history


### ▶ Permissions
- Login
- Sign Up
- Shop ID

### ▶ Expense Management *(Upcoming)*
- Record daily expenses
- Categorize expenses and generate reports

### ▶ E-Commerce Integration *(Upcoming)*
- Sync inventory with online platforms
- Manage online orders

### ▶ Notifications & Alerts
- Expiry alerts, low stock, and payment reminders
- Email and SMS notifications (Upcoming)

### ▶ Mobile App Support *(Planned)*
- Monitor sales and stock in real-time
- Instant updates and push alerts

### ▶ Data Backup & Security
- Automatic database backups
- Secure login with OTP or biometrics
- Environment variables for sensitive data

### ▶ Security
- Email and phone verification during sign-up
- OTP-based password reset

---

## Installation

1. **Clone or Download** the repository:
   ```bash
   git clone https://github.com/codex-yv/Shop-Management-System---Bazaro.git

2. **Requirement files** run setup.py file:
   ```bash
   py setup.py

3. **Basic Setup** run firstrunner.py file:
   ```bash
   py firstrunner.py

4. **Main Application** run main.py file:
   ```bash
   py main.py
   
3. **Read "How to use.txt" file**  (Not updated yet)

## Development Status

| Module                      | Status         | Notes                                |
|----------------------------|----------------|--------------------------------------|
| Inventory Management       | ✅ Completed    | Fully functional add/update/delete   |
| Billing and Reports        | ✅ Completed    | PDF & Excel export, GST support      |
| Alerts (Stock & Expiry)    | ✅ Completed    | Auto-alert on low stock/expiry       |
| Customer Management        | ✅ Completed    | Loyalty system in place              |
| Supplier Management        | ✅ Completed    | Purchase order & profile support     |
| Login & Authentication     | ✅ Completed    | OTP-based with email/phone verify    |
| Dashboard (Graphical)      | 🛠️ In Progress  | Visual charts and graphs being added |
| Settings Module            | 🛠️ In Progress  | User customization coming soon       |
| Multi-Counter Support      | ✅ Completed    | Centralized data & store linking     |
| Expense Management         | 🔜 Planned      | Record & analyze store expenses      |
| Mobile App Companion       | 🔜 Planned      | Android/iOS real-time monitoring     |


-  **Login Interface**

<img src="screenshots\\Screenshot 2025-06-05 171805.png" alt="main" width="800" height='450'/>

- **Dashboard**

<img src="screenshots\\Screenshot 2025-06-05 171826.png" alt="before" width="720" height='300'/>

- **INVENTORY**

<img src="screenshots\\Screenshot 2025-06-05 171844.png" alt="before" width="720" height='300'/>


- **Alerts** 

<img src="screenshots\\Screenshot 2025-06-05 171906.png" alt="before" width="720" height='300'/>

- **Billing**

<img src="screenshots\\Screenshot 2025-06-05 171947.png" alt="before" width="720" height='300'/>

- And here is the **History**

<img src="screenshots\\Screenshot 2025-06-05 172011.png" alt="before" width="720" height='300'/>

- And here is the **Customer Care**

<img src="screenshots\\Screenshot 2025-06-05 172031.png" alt="before" width="720" height='300'/>
