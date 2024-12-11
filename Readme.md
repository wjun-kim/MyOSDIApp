# MyOSDIApp Project

This `README.md` file contains the entire process for developing, building, and deploying the MyOSDIApp project, which is an Android app for dry eye self-diagnosis using the Ocular Surface Disease Index (OSDI) questionnaire.

---

## **1. Project Overview**
MyOSDIApp is a mobile application designed to assess dry eye symptoms using the OSDI questionnaire. The app allows users to input responses, calculates the OSDI score, and provides feedback on their eye condition.

### **Features**
- User-friendly interface with images and clear instructions.
- Ability to save up to 5 past scores for tracking progress.
- Provides recommendations and links for further dry eye management.

---

## **2. Development Environment**

### **Prerequisites**
1. **Operating System**: Ubuntu (or WSL on Windows)
2. **Python Version**: 3.10 or 3.11
3. **Build Tools**:
   - Buildozer
   - Android SDK/NDK
4. **Dependencies**:
   - Kivy
   - Cython

### **Tools Installed**
- OpenJDK 8 for Java development.
- pip and virtual environment setup for Python package management.

---

## **3. Project Directory Structure**

```
MyOSDIApp/
├── main.py                # Main application script
├── buildozer.spec         # Buildozer configuration file
├── assets/                # Images and resources
│   ├── eyes.png
│   └── ...
├── bin/                   # APK output directory
└── README.md              # Project documentation
```

---

## **4. Development Process**

### **Step 1: Setting Up the Development Environment**

1. **System Update**:
   ```bash
   sudo apt update
   sudo apt upgrade -y
   ```

2. **Install Python and Dependencies**:
   ```bash
   sudo apt install python3.10 python3.10-venv python3-pip -y
   sudo apt install build-essential git zlib1g-dev libssl-dev -y
   ```

3. **Install Cython**:
   ```bash
   python3 -m pip install Cython
   ```

4. **Install Kivy**:
   ```bash
   python3 -m pip install kivy
   ```

5. **Install Buildozer**:
   ```bash
   python3 -m pip install buildozer
   ```

---

### **Step 2: Setting Up JAVA_HOME**

1. Install OpenJDK 8:
   ```bash
   sudo apt install openjdk-8-jdk -y
   ```

2. Configure `JAVA_HOME`:
   ```bash
   echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64" >> ~/.bashrc
   echo "export PATH=\$JAVA_HOME/bin:\$PATH" >> ~/.bashrc
   source ~/.bashrc
   ```

---

### **Step 3: Creating the Application**
1. Write the main application logic in `main.py`. Example:
   ```python
   from kivy.app import App
   from kivy.uix.boxlayout import BoxLayout

   class MainApp(App):
       def build(self):
           return BoxLayout()

   if __name__ == '__main__':
       MainApp().run()
   ```

2. Customize the `buildozer.spec` file:
   ```bash
   buildozer init
   nano buildozer.spec
   ```
   Key settings to modify:
   - `title = MyOSDIApp`
   - `package.name = myosdiapp`
   - `requirements = kivy`

---

### **Step 4: Building the APK**

1. Build the APK:
   ```bash
   buildozer android debug
   ```

2. Output APK file is stored in the `bin/` directory:
   ```bash
   ls bin/
   MyOSDIApp-0.1-debug.apk
   ```

---

### **Step 5: Testing the App**

1. **Install APK on Android Device**:
   - Use USB or `adb`:
     ```bash
     adb install bin/MyOSDIApp-0.1-debug.apk
     ```

2. **Run the App**:
   - Open the app on your device and test its functionality.

---

## **5. Troubleshooting**

### **Common Errors**
1. **Cython Not Found**:
   ```
   ERROR: Cython not found.
   ```
   **Solution**:
   Install Cython using pip:
   ```bash
   python3 -m pip install Cython
   ```

2. **JAVA_HOME Invalid Directory**:
   ```
   ERROR: JAVA_HOME is set to an invalid directory
   ```
   **Solution**:
   Ensure JAVA_HOME is correctly set to the OpenJDK 8 directory:
   ```bash
   export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
   export PATH=$JAVA_HOME/bin:$PATH
   ```

3. **Missing Dependencies**:
   ```
   ERROR: Missing dependencies.
   ```
   **Solution**:
   Ensure all necessary libraries and tools are installed:
   ```bash
   sudo apt install build-essential python3-dev -y
   ```

---

## **6. Future Improvements**
- Add additional features such as user account creation and cloud data storage.
- Implement a better UI design using advanced Kivy widgets.
- Provide multi-language support.

---

## **7. Credits**
This project was built using:
- **Kivy**: A Python framework for developing multi-platform applications.
- **Buildozer**: A tool to package Python apps into standalone APKs.

---

## **8. References**
- ChatGPT
