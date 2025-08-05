Project Title: ProCoordinator - A Critical Path Method (CPM) Calculator

Project Description-
This project is a Critical Path Method (CPM) Calculator designed to assist project managers in determining the critical path of complex projects, calculating the earliest and latest start/finish times, and identifying tasks with slack. The graphical user interface (GUI) enables users to input tasks, view calculated results, and understand project timelines visually.

Features:
-User-friendly GUI for task entry.
-Calculates Earliest Start (ES), Earliest Finish (EF), Latest Start (LS), and Latest Finish (LF).
-Identifies the Critical Path.
-Displays results in a color-coded table.
-Allows saving results in a .txt file.

Prerequisites-

Before running the project, ensure you have the following installed:
	-Java Development Kit (JDK) 8 or higher
	-Java IDE (e.g., IntelliJ IDEA, Eclipse, NetBeans) or a terminal with javac and java commands.

How to Run the Project-

Option 1: Using a Java IDE:
	-Download the project from the repository or place the files in a local folder.
	-Open the project in your Java IDE.
	-Ensure the package structure is intact (e.g., gui, logic packages).
	-Locate and run the WelcomeScreen/Main class by clicking Run.

Option 2: Using Command Line:
	-Navigate to the project directory in your terminal.
	-Compile all .java files
	-Run the WelcomeScreen/Main class to start the application

Project Structure-

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


How to Use:

-Launch the Application
	•Upon launching, a Welcome Screen with two buttons will appear: Start and About.
-Input Tasks
	•Click Start to open the task input page.
	•Enter the Task Name, Duration, and Dependencies(Comma separated. If there is no dependency, please leave the field 	 blank.)
	•Click Add Task for adding each task and Submit to calculate.
-View Results
	•The Output Page will display tasks, their schedules, and the Critical Path in a color-coded table.
	•Critical tasks will be highlighted in light green, and non-critical tasks in light pink.
-Save Results
	•The results are saved automatically to the output/project_results.txt file.


Example of Use Case-
You can use this CPM Calculator to plan software development, construction projects, or any scenario where tracking task dependencies and schedules is critical.


Contact Information-

For issues or explanation, please contact:
Md. Salman Khan
Email: salman2517@student.nstu.edu.bd