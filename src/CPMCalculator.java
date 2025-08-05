package logic;

import java.util.*;

public class CPMCalculator {
    private final HashMap<String, Task> tasks;
    private final ArrayList<Task> taskList;

    public CPMCalculator(ArrayList<Task> taskList) {
        this.tasks = new HashMap<>();
        this.taskList = taskList;

        // Populate the task map for quick lookup
        for (Task task : taskList) {
            tasks.put(task.getName(), task);
        }
    }

    public void calculate() {
        forwardPass();
        backwardPass();
    }

    private void forwardPass() {
        // Set ES to 0 for the first task
        for (Task task : taskList) {
            int maxEF = 0;

            // Calculate based on dependencies
            for (String dependency : task.getDependencies()) {
                Task dependencyTask = tasks.get(dependency);
                if (dependencyTask != null) {
                    maxEF = Math.max(maxEF, dependencyTask.getEF());
                }
            }

            // Set ES and EF
            task.setES(maxEF);
            task.setEF(task.getES() + task.getDuration());
        }
    }

    private void backwardPass() {
        // Initialize LF to the project duration (max EF of all tasks)
        int projectDuration = taskList.stream().mapToInt(Task::getEF).max().orElse(0);

        // Traverse tasks in reverse order for the backward pass
        for (int i = taskList.size() - 1; i >= 0; i--) {
            Task task = taskList.get(i);

            // If it's the last task in the project, set LF to project duration
            if (i == taskList.size() - 1) {
                task.setLF(projectDuration);
            } else {
                // LF is the minimum LS of all successor tasks
                int minLS = Integer.MAX_VALUE;
                for (Task t : taskList) {
                    if (t.getDependencies().contains(task.getName())) {
                        minLS = Math.min(minLS, t.getLS());
                    }
                }
                if (minLS != Integer.MAX_VALUE) {
                    task.setLF(minLS);
                }
            }

            // Set LS and slack
            task.setLS(task.getLF() - task.getDuration());
            task.setSlack(task.getLS() - task.getES());
        }
    }

    public ArrayList<Task> getCriticalPath() {
        ArrayList<Task> criticalPath = new ArrayList<>();
        for (Task task : taskList) {
            if (task.getSlack() == 0) {
                criticalPath.add(task);
            }
        }
        return criticalPath;
    }

    public int getProjectDuration() {
        return taskList.stream().mapToInt(Task::getEF).max().orElse(0);
    }
}
