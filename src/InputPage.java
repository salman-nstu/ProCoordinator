package gui;

import logic.Task;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.io.*;
import java.util.ArrayList;

public class InputPage extends JFrame {
    private ArrayList<Task> tasks = new ArrayList<>();
    private JTextField nameField, durationField, dependencyField;

    public InputPage() {
        setTitle("Task Input");
        setSize(600, 500);
        setLocationRelativeTo(null);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLayout(new BorderLayout());


        JLabel headerLabel = new JLabel("Enter Task Details", SwingConstants.CENTER);
        headerLabel.setFont(new Font("Arial", Font.BOLD, 22));
        headerLabel.setForeground(Color.WHITE);
        headerLabel.setOpaque(true);
        headerLabel.setBackground(new Color(58, 97, 134));
        add(headerLabel, BorderLayout.NORTH);


        JPanel formPanel = new JPanel(new GridLayout(0, 2, 10, 10));
        formPanel.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));
        formPanel.setBackground(Color.LIGHT_GRAY);

        JLabel nameLabel = new JLabel("Task Name:");
        nameLabel.setFont(new Font("Arial", Font.BOLD, 16));
        nameField = new JTextField();
        nameField.setFont(new Font("Arial", Font.PLAIN, 16));
        nameField.setPreferredSize(new Dimension(200, 30));
        nameField.setBorder(BorderFactory.createLineBorder(Color.GRAY, 1));
        nameField.setBackground(new Color(255, 175, 189));
        nameField.setHorizontalAlignment(JTextField.CENTER);

        JLabel durationLabel = new JLabel("Duration:");
        durationLabel.setFont(new Font("Arial", Font.BOLD, 16));
        durationField = new JTextField();
        durationField.setFont(new Font("Arial", Font.PLAIN, 16));
        durationField.setPreferredSize(new Dimension(200, 30));
        durationField.setBorder(BorderFactory.createLineBorder(Color.GRAY, 1));
        durationField.setBackground(new Color(255, 175, 189));
        durationField.setHorizontalAlignment(JTextField.CENTER);

        JLabel dependencyLabel = new JLabel("Dependencies (comma-separated):");
        dependencyLabel.setFont(new Font("Arial", Font.BOLD, 16));
        dependencyField = new JTextField();
        dependencyField.setFont(new Font("Arial", Font.PLAIN, 16));
        dependencyField.setPreferredSize(new Dimension(200, 30));
        dependencyField.setBorder(BorderFactory.createLineBorder(Color.GRAY, 1));
        dependencyField.setBackground(new Color(255, 175, 189));
        dependencyField.setHorizontalAlignment(JTextField.CENTER);

        nameField.setBorder(BorderFactory.createCompoundBorder(
                nameField.getBorder(),
                BorderFactory.createEmptyBorder(5, 10, 5, 10)
        ));
        durationField.setBorder(BorderFactory.createCompoundBorder(
                durationField.getBorder(),
                BorderFactory.createEmptyBorder(5, 10, 5, 10)
        ));
        dependencyField.setBorder(BorderFactory.createCompoundBorder(
                dependencyField.getBorder(),
                BorderFactory.createEmptyBorder(5, 10, 5, 10)
        ));

        formPanel.add(nameLabel);
        formPanel.add(nameField);
        formPanel.add(durationLabel);
        formPanel.add(durationField);
        formPanel.add(dependencyLabel);
        formPanel.add(dependencyField);

        add(formPanel, BorderLayout.CENTER);


        JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.CENTER, 30, 20));
        buttonPanel.setBackground(Color.LIGHT_GRAY);

        RoundedButton addButton = new RoundedButton("Add Task");
        addButton.setBackground(new Color(67, 198, 172));
        addButton.setForeground(Color.WHITE);
        addButton.setFont(new Font("Arial", Font.BOLD, 14));
        addButton.setPreferredSize(new Dimension(130, 40));
        addButton.setToolTipText("Click to add a task");

        RoundedButton submitButton = new RoundedButton("Submit");
        submitButton.setBackground(new Color(67, 198, 172));
        submitButton.setForeground(Color.WHITE);
        submitButton.setFont(new Font("Arial", Font.BOLD, 14));
        submitButton.setPreferredSize(new Dimension(130, 40));
        submitButton.setToolTipText("Click to save tasks and view results");

        addButton.addActionListener((ActionEvent e) -> {
            String name = nameField.getText().trim();
            String durationText = durationField.getText().trim();
            String dependencyText = dependencyField.getText().trim();

            if (name.isEmpty() || durationText.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Please fill in all fields!", "Error", JOptionPane.ERROR_MESSAGE);
                return;
            }

            try {
                int duration = Integer.parseInt(durationText);
                ArrayList<String> dependencies = new ArrayList<>();
                for (String dep : dependencyText.split(",")) {
                    if (!dep.trim().isEmpty()) dependencies.add(dep.trim());
                }
                tasks.add(new Task(name, duration, dependencies));
                nameField.setText("");
                durationField.setText("");
                dependencyField.setText("");
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(this, "Invalid duration value!", "Error", JOptionPane.ERROR_MESSAGE);
            }
        });

        submitButton.addActionListener((ActionEvent e) -> {
            if (tasks.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Please add at least one task!", "Error", JOptionPane.ERROR_MESSAGE);
                return;
            }
            saveTasksToFile();
            new OutputPage(tasks).setVisible(true);
            dispose();
        });

        buttonPanel.add(addButton);
        buttonPanel.add(submitButton);

        add(buttonPanel, BorderLayout.SOUTH);
    }

    private void saveTasksToFile() {
        File directory = new File("output");
        if (!directory.exists()) directory.mkdirs();

        try (BufferedWriter writer = new BufferedWriter(new FileWriter("output/project_data.txt"))) {
            for (Task task : tasks) {
                writer.write(task.getName() + "," + task.getDuration() + "," + String.join(":", task.getDependencies()));
                writer.newLine();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
