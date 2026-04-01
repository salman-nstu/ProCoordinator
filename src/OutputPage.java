package gui;

import logic.CPMCalculator;
import logic.Task;

import javax.swing.*;
import javax.swing.table.DefaultTableCellRenderer;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.io.*;
import java.util.ArrayList;

public class OutputPage extends JFrame {

    public OutputPage(ArrayList<Task> tasks) {
        setTitle("CPM Results");
        setSize(800, 600);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        setLayout(new BorderLayout());

        JLabel headerLabel = new JLabel("Critical Path Method Results", SwingConstants.CENTER);
        headerLabel.setFont(new Font("Arial", Font.BOLD, 20));
        headerLabel.setOpaque(true);
        headerLabel.setBackground(new Color(0, 102, 204));
        headerLabel.setForeground(Color.WHITE);
        add(headerLabel, BorderLayout.NORTH);

        CPMCalculator calculator = new CPMCalculator(tasks);
        calculator.calculate();

        ArrayList<Task> criticalPath = calculator.getCriticalPath();

        JPanel tablePanel = new JPanel(new BorderLayout());
        tablePanel.setBorder(BorderFactory.createTitledBorder("Task Matrix"));
        JTable taskTable = new JTable();
        DefaultTableModel tableModel = new DefaultTableModel();
        tableModel.addColumn("Task Name");
        tableModel.addColumn("Earliest Start");
        tableModel.addColumn("Earliest Finish");
        tableModel.addColumn("Latest Start");
        tableModel.addColumn("Latest Finish");
        tableModel.addColumn("Slack");

        for (Task task : tasks) {
            Object[] rowData = new Object[]{
                    task.getName(),
                    task.getES(),
                    task.getEF(),
                    task.getLS(),
                    task.getLF(),
                    task.getSlack()
            };
            tableModel.addRow(rowData);
        }

        taskTable.setModel(tableModel);

        taskTable.setDefaultRenderer(Object.class, new DefaultTableCellRenderer() {
            @Override
            public Component getTableCellRendererComponent(JTable table, Object value, boolean isSelected, boolean hasFocus, int row, int column) {
                Component cell = super.getTableCellRendererComponent(table, value, isSelected, hasFocus, row, column);

                int slack = Integer.parseInt(table.getValueAt(row, 5).toString());

                if (slack == 0) {
                    cell.setBackground(new Color(204, 255, 204));
                } else {
                    cell.setBackground(new Color(255, 204, 204));
                }

                cell.setForeground(Color.BLACK);
                if (isSelected) {
                    cell.setBackground(new Color(184, 207, 229));
                }
                return cell;
            }
        });

        JScrollPane tableScrollPane = new JScrollPane(taskTable);
        tablePanel.add(tableScrollPane, BorderLayout.CENTER);


        JPanel infoPanel = new JPanel(new GridLayout(2, 1, 10, 10));
        infoPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
        infoPanel.setBackground(Color.LIGHT_GRAY);


        JPanel criticalPathPanel = new JPanel(new BorderLayout());
        criticalPathPanel.setBorder(BorderFactory.createTitledBorder("Critical Path"));
        JLabel criticalPathLabel = new JLabel(
                "Critical Path: " + String.join(" → ", calculator.getCriticalPath().stream()
                        .map(Task::getName)
                        .toArray(String[]::new))
        );
        criticalPathLabel.setFont(new Font("Arial", Font.BOLD, 14));
        criticalPathLabel.setHorizontalAlignment(SwingConstants.CENTER);
        criticalPathPanel.add(criticalPathLabel, BorderLayout.CENTER);

        JPanel durationPanel = new JPanel(new BorderLayout());
        durationPanel.setBorder(BorderFactory.createTitledBorder("Project Duration"));
        JLabel durationLabel = new JLabel(
                "Project Duration: " + calculator.getProjectDuration() + " units"
        );
        durationLabel.setFont(new Font("Arial", Font.BOLD, 14));
        durationLabel.setHorizontalAlignment(SwingConstants.CENTER);
        durationPanel.add(durationLabel, BorderLayout.CENTER);

        infoPanel.add(criticalPathPanel);
        infoPanel.add(durationPanel);

        add(tablePanel, BorderLayout.CENTER);
        add(infoPanel, BorderLayout.SOUTH);


        saveResultsToFile(tasks, calculator);
    }


    private void saveResultsToFile(ArrayList<Task> tasks, CPMCalculator calculator) {

        File directory = new File("output");
        if (!directory.exists()) directory.mkdirs();

        try (BufferedWriter writer = new BufferedWriter(new FileWriter("output/project_results.txt"))) {

            writer.write("Task Name, ES, EF, LS, LF, Slack\n");
            for (Task task : tasks) {
                writer.write(task.getName() + ", " +
                        task.getES() + ", " +
                        task.getEF() + ", " +
                        task.getLS() + ", " +
                        task.getLF() + ", " +
                        task.getSlack() + "\n");
            }

            writer.write("\nCritical Path: ");
            writer.write(String.join(" → ", calculator.getCriticalPath().stream()
                    .map(Task::getName)
                    .toArray(String[]::new)) + "\n");

            writer.write("Project Duration: " + calculator.getProjectDuration() + " units\n");

            JOptionPane.showMessageDialog(this, "Results saved to 'output/project_results.txt'", "Save Successful", JOptionPane.INFORMATION_MESSAGE);
        } catch (IOException e) {
            e.printStackTrace();
            JOptionPane.showMessageDialog(this, "An error occurred while saving the results.", "Save Failed", JOptionPane.ERROR_MESSAGE);
        }
    }
}
