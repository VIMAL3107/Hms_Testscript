# HMS Test Automation Setup Guide

This document covers everything you need from start to finish to set up and run the automated tests on your computer.

---

## Phase 1: Environment Setup (One-Time)

1. **Unblock the ZIP file:**
   - Before extracting the project, right-click the `.zip` file.
   - Select **Properties**.
   - Check the **Unblock** box at the bottom and click **OK**.
   - Extract the folder.

2. **Run the Setup Script:**
   - Go into the `Setup` folder.
   - Double-click **`setup.bat`**.
   - Let the script download and install everything (Java, Node.js, Appium, etc.).
   - **Troubleshooting:** If Windows Smart App Control blocks it, right-click the file -> Properties -> Unblock. Alternatively, open PowerShell in the `Setup` folder and run: `powershell -ExecutionPolicy Bypass -File .\setup.ps1`

3. **Restart the Computer:**
   - **Important:** You must restart your laptop so that the installed tools are registered in your system.

---

## Phase 2: Android Studio & Emulator Setup

Instead of a physical phone, we will use an Android Virtual Device (Emulator) to run the tests.

1. **Download & Install Android Studio:**
   - Download Android Studio from the official site: [https://developer.android.com/studio](https://developer.android.com/studio)
   - Install it using the default settings.
2. **Create an Emulator:**
   - Open Android Studio.
   - Go to **Device Manager** (usually found under the "Tools" menu or on the right sidebar).
   - Click **Create Device** and set up a new virtual phone.
3. **Start the Emulator:**
   - Click the **Play** button next to your virtual device to start it up.
   - Wait for the virtual Android phone to fully turn on and load the home screen. 
   *(This emulator acts as the connected device the automation will run on.)*

---

## Phase 3: Running the Automation

Once your Android Emulator is up and running, you are ready to execute the tests! 

1. **Run the Executable (.exe):**
   - Go to the project folder (or wherever you placed the `.exe` file).
   - Double-click the **`ReservationTest01.exe`**.
   - **That's it!** The executable will automatically start the Appium server in the background, connect to your running Android emulator, and perform the tests.

---

## What to Expect (The Test Flow)

When you run the `.exe`, you do not need to provide any input. The automation is fully self-contained:

- **Predefined Credentials:** The executable already has the correct login credentials (username and PIN) baked into it. You do not need to configure any passwords.
- **End-to-End Flow:** The automation code executes the following complete flow automatically:
  1. Open the application.
  2. Log in using the predefined credentials.
  3. Navigate through the menus to create a new Reservation.
  4. Complete the booking process.
  5. **User Check-In:** Locate the newly created reservation and process the guest's check-in to assign them a room.
  6. **User Checkout:** Navigate to the checked-in guest's profile, process their payment/folio, and complete the final checkout.
  7. Validate that the entire flow finished successfully.

**Note on Login Credentials:** If a new user needs to run the tests with different login credentials, the code must be rebuilt by the developer. The user will be provided with a brand new `.zip` file containing the updated `.exe` with their specific credentials baked in.
