package gui;

import javax.swing.*;
import java.awt.*;

public class WelcomeScreen extends JFrame {

    public WelcomeScreen() {
        setTitle("Welcome to CPM Calculator");
        setSize(600, 400);
        setLocationRelativeTo(null);
        setDefaultCloseOperation(EXIT_ON_CLOSE);

        GradientPanel backgroundPanel = new GradientPanel();
        backgroundPanel.setLayout(new GridBagLayout());
        setContentPane(backgroundPanel);

        JPanel centerPanel = new JPanel(new BorderLayout());
        centerPanel.setPreferredSize(new Dimension(400, 200));
        centerPanel.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(new Color(0, 0, 0), 4, true),
                BorderFactory.createEmptyBorder(20, 20, 20, 20)
        ));
        centerPanel.setBackground(new Color(58, 97, 134));

        JLabel label = new JLabel("<html><center>Welcome To Coordinator,<br>Please Click START to enter.</center></html>", SwingConstants.CENTER);
        label.setFont(new Font("Arial", Font.BOLD, 18));
        label.setForeground(Color.BLACK);
        centerPanel.add(label, BorderLayout.CENTER);

        GridBagConstraints gbc = new GridBagConstraints();
        gbc.gridx = 0;
        gbc.gridy = 0;
        gbc.weightx = 1;
        gbc.weighty = 1;
        gbc.anchor = GridBagConstraints.CENTER;
        backgroundPanel.add(centerPanel, gbc);

        JPanel buttonPanel = new JPanel(new GridLayout(1, 2, 10, 10));
        buttonPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
        buttonPanel.setOpaque(false);

        RoundedButton startButton = new RoundedButton("Start");
        startButton.setBackground(new Color(51, 51, 153));
        startButton.setForeground(Color.BLACK);
        startButton.setFont(new Font("Arial", Font.BOLD, 14));
        startButton.setToolTipText("Click to start entering tasks");
        startButton.addActionListener(e -> {
            dispose();
            new InputPage().setVisible(true);
        });

        RoundedButton aboutButton = new RoundedButton("About");
        aboutButton.setBackground(new Color(51, 51, 152));
        aboutButton.setForeground(Color.BLACK);
        aboutButton.setFont(new Font("Arial", Font.BOLD, 14));
        aboutButton.setToolTipText("Click to learn more about the CPM calculator");
        aboutButton.addActionListener(e -> {

            JDialog dialog = new JDialog(this, "About", true);
            dialog.setSize(400, 200);
            dialog.setLayout(new BorderLayout());
            dialog.setDefaultCloseOperation(JDialog.DISPOSE_ON_CLOSE);

            JLabel aboutLabel = new JLabel("<html><center>" +
                    "<h2>About CPM Calculator</h2>" +
                    "This is a Critical Path Method (CPM) Calculator.<br>" +
                    "It helps you plan and manage complex projects efficiently.<br>" +
                    "<br>Developed by: <b>Md. Salman Khan</b><br>" +
                    "Version: <b>1.0</b>" +
                    "</center></html>");
            aboutLabel.setHorizontalAlignment(SwingConstants.CENTER);
            dialog.add(aboutLabel, BorderLayout.CENTER);

            dialog.setLocationRelativeTo(this);
            dialog.setVisible(true);
        });

        buttonPanel.add(startButton);
        buttonPanel.add(aboutButton);

        gbc.gridy = 1;
        gbc.anchor = GridBagConstraints.PAGE_END;
        backgroundPanel.add(buttonPanel, gbc);
    }

    private static class GradientPanel extends JPanel {
        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            Graphics2D g2d = (Graphics2D) g;

            Color color1 = new Color(243, 144, 79);
            Color color2 = new Color(59, 67, 113);
            GradientPaint gradient = new GradientPaint(0, 0, color1, 0, getHeight(), color2);
            g2d.setPaint(gradient);
            g2d.fillRect(0, 0, getWidth(), getHeight());
        }
    }
}
