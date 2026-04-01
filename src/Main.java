import gui.WelcomeScreen;

public class Main {
    public static void main(String[] args) {
        javax.swing.SwingUtilities.invokeLater(() -> new WelcomeScreen().setVisible(true));
    }
}
