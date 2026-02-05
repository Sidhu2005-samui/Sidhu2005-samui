# Bricks vs Balls - Android APK Build Guide

This game is built using HTML5 Canvas and JavaScript. To export it as an Android APK, we can use **Capacitor** by Ionic, which wraps web applications into native apps.

## Prerequisites

1.  **Node.js & npm**: Install from [nodejs.org](https://nodejs.org/).
2.  **Android Studio**: Install from [developer.android.com](https://developer.android.com/studio).
3.  **Java JDK**: Ensure JDK 11 or 17 is installed.

## Step-by-Step Guide

### 1. Initialize Project

Open your terminal in the `bricks_vs_balls` directory (or copy the contents to a new folder for the build).

```bash
# Initialize a new package.json
npm init -y

# Install Capacitor
npm install @capacitor/core @capacitor/cli @capacitor/android
npx cap init
# Follow prompts:
# Name: Bricks vs Balls
# ID: com.yourname.bricksvsballs
# Directory: www (or static)
```

### 2. Prepare Web Assets

Capacitor expects your web assets (HTML, CSS, JS) to be in a specific distribution folder (default is `www` or `dist`).

Since this project structure uses `templates` and `static`, we need to rearrange them for the build:

1.  Create a folder named `www`.
2.  Copy `templates/index.html` to `www/index.html`.
3.  Copy the `static` folder to `www/static`.

Ensure `www/index.html` refers to assets relatively (e.g., `src="static/js/game.js"`), which we have already configured.

### 3. Add Android Platform

```bash
npx cap add android
```

### 4. Sync Assets

Every time you update your JS/CSS/HTML in `www`, run:

```bash
npx cap sync
```

### 5. Build & Open in Android Studio

```bash
npx cap open android
```

This will launch Android Studio.

1.  Wait for Gradle sync to finish.
2.  Connect your Android device or create an Emulator.
3.  Click the **Run** (Green Play) button to test on device.

### 6. Export APK (Release)

To generate a signed APK for the Play Store:

1.  In Android Studio, go to **Build > Generate Signed Bundle / APK**.
2.  Select **APK**.
3.  Create a new KeyStore (save the password safely).
4.  Select `release` build variant.
5.  Click **Finish**.

The APK file will be generated in `android/app/release/`.

## Optimization for Mobile

-   **Fullscreen**: The `style.css` includes `touch-action: none` to prevent scrolling.
-   **Icons**: Replace the default Capacitor icons in `android/app/src/main/res` with your game icons.
-   **Orientation**: To lock to portrait mode, open `android/app/src/main/AndroidManifest.xml` and add `android:screenOrientation="portrait"` to the `<activity>` tag.

## Troubleshooting

-   **White Screen**: Check if `index.html` paths are correct. Use Chrome Remote Debugging (chrome://inspect) to see console errors on the device.
-   **Touch Issues**: Ensure `touch-action: none` is applied to the canvas/body.
