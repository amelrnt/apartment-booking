# Travelio Apartment Booking Module

This Odoo 19 module manages apartment unit bookings with an automated waitlist system and FIFO (First-In-First-Out) promotion logic.

## Features
- **Booking Management**: Create bookings in `Hold`, `Confirmed`, `Cancelled`, or `Expired` states.
- **Waitlist System**: Automatically moves overlapping requests to a waitlist if a unit is occupied.
- **Auto-Expire**: Automated cron job sets bookings to `Expired` after 30 minutes of inactivity in the `Hold` state.
- **FIFO Promotion**: Automatically promotes the earliest matching waitlist entry when a unit becomes available.

## Installation
1. Copy the `travelio_apartment` folder to your Odoo custom addons directory.
2. Restart the Odoo server.
3. Enable **Developer Mode**.
4. Go to **Apps** > **Update Apps List**.
5. Search for `Travelio Apartment Booking` and click **Install**.

## Test Scenarios

### 1. Booking Available (Hold Formed)
- Go to **Travelio Booking** > **Units**.
- Select a unit and click the **Request Booking** wizard.
- Input a customer and a date range.
- **Expected Result**: A new record is created in `travelio.apartment.booking` with state `Hold` and an expiration time set to Now + 30 minutes.

### 2. Booking Overlap (Waitlist Entry)
- While the previous booking is still `Hold` or `Confirmed`, create a new request for the **same unit** and **overlapping dates**.
- **Expected Result**: No booking is created. Instead, a record is created in **Waitlist** with state `Waiting`.

### 3. Manual Cancel & Promote
- Open the active `Hold` booking from Scenario 1.
- Click **Cancel Booking** and provide a mandatory reason in the popup.
- **Expected Result**: The booking state changes to `Cancelled`. Simultaneously, the Waitlist entry from Scenario 2 is promoted to a new `Hold` booking.

### 4. Auto Expire via Cron
- Create a `Hold` booking.
- Manually edit the `hold_expired_at` field in the database (or wait 30 minutes) to a past time.
- Run the scheduled action: `Apartment Booking: Auto Expire Hold`.
- **Expected Result**: The booking state becomes `Expired`, and the next compatible Waitlist entry is promoted.

### 5. Double Booking Prevention
- Attempt to manually create a booking in the `Confirmed` state that overlaps with another `Confirmed` booking for the same unit.
- **Expected Result**: The system triggers an SQL or Python Validation Error, preventing the save.