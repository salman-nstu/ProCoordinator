# ProCoordinator – A Critical Path Method (CPM) Calculator

## 📌 Project Description
**ProCoordinator** is a Critical Path Method (CPM) Calculator designed to help project managers determine the critical path of complex projects, calculate earliest/latest start and finish times, and identify tasks with slack.  
With an intuitive **Graphical User Interface (GUI)**, users can input tasks, view computed results, and visualize project timelines for efficient planning and execution.

---

## ✨ Features
- 🖥 **User-friendly GUI** for quick task entry
- ⏳ Calculates **Earliest Start (ES)**, **Earliest Finish (EF)**, **Latest Start (LS)**, and **Latest Finish (LF)**
- 📊 Identifies the **Critical Path**
- 🎨 Displays results in a **color-coded table**
- 💾 Saves results automatically to a `.txt` file

---

## 🛠 Prerequisites
Before running the project, ensure you have:
- **Java Development Kit (JDK)** 8 or higher
- **Java IDE** (IntelliJ IDEA, Eclipse, NetBeans) or a terminal with `javac` and `java` commands

---

## 🚀 How to Run

### Option 1: Using a Java IDE
1. Download or clone this repository.
2. Open the project in your Java IDE.
3. Ensure the package structure is intact (`gui`, `logic`).
4. Run the `WelcomeScreen` or `Main` class.

### Option 2: Using Command Line
1. Navigate to the project directory in your terminal.
2. Compile all `.java` files:
   ```bash
   javac src/**/*.java
   ```
3. Run the application:
   ```bash
   java gui.WelcomeScreen
   ```

---

## 📂 Project Structure
```
/src
 ├── /gui
 │    ├── WelcomeScreen.java
 │    ├── InputPage.java
 │    ├── OutputPage.java
 │    └── RoundedButton.java
 ├── /logic
 │    ├── Task.java
 │    └── CPMCalculator.java
/output
/README.md
```

---

## 📖 How to Use

1. **Launch the Application**  
   - A Welcome Screen with **Start** and **About** buttons will appear.

2. **Input Tasks**  
   - Click **Start** to open the task input page.  
   - Enter **Task Name**, **Duration**, and **Dependencies** (comma-separated).  
   - Leave the dependency field blank if none.  
   - Click **Add Task** for each entry, then **Submit** to calculate.

3. **View Results**  
   - The Output Page displays all tasks, schedules, and the Critical Path in a **color-coded table**.  
   - **Light Green** = Critical tasks  
   - **Light Pink** = Non-critical tasks  

4. **Save Results**  
   - Results are saved automatically to `output/project_results.txt`.

---

## 💡 Example Use Cases
- Software development project planning
- Construction project scheduling
- Any workflow with task dependencies and deadlines

---

## 📬 Contact
**Md. Salman Khan**  
📧 Email: [salman2517@student.nstu.edu.bd](mailto:salman2517@student.nstu.edu.bd)

---

