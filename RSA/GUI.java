import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.IOException;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;


public class GUI {

    public GUI() {
        JFrame frame = new JFrame("Temp");
        frame.setSize(600, 300);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setResizable(false);

        JPanel panel = new JPanel();

        JButton button = new JButton("ENCRYPT");
        button.setFocusable(false);
        button.addActionListener(new ActionListener() {

            @Override
            public void actionPerformed(ActionEvent e) {
                try{
                    String pythonScriptPath = "RSA/testtemp.py";
                    ProcessBuilder processBuilder = new ProcessBuilder("python", pythonScriptPath);
                    Process process = processBuilder.start();

                    int exitCode = process.waitFor();
                    if (exitCode == 0) {
                        System.out.println("Python script executed successfully");
                        button.setText("Done!");
                        button.setEnabled(false);
                    } else {
                        System.out.println("Error executing Python script, exit code: " + exitCode);
                    }
                } catch(IOException | InterruptedException ex){
                    ex.printStackTrace();
                }
            }

        });

        JLabel instructions = new JLabel("<html><div style='text-align: center;'>Add whatever text you would like encrypted in the top text-box and click the button to receive a beautifully ciphered message in the bottom text-box!</div></html>");
        instructions.setFont(new Font("Arial", Font.PLAIN, 14));
        instructions.setPreferredSize(new Dimension(570, 50)); // Set preferred size
        instructions.setVerticalAlignment(JLabel.TOP);
        instructions.setHorizontalAlignment(JLabel.CENTER);
        instructions.setVerticalTextPosition(JLabel.TOP);
        instructions.setHorizontalTextPosition(JLabel.CENTER);

        JTextField input = new JTextField("Input");
        input.setPreferredSize(new Dimension(500,20));
        JTextField output = new JTextField("Output");
        output.setPreferredSize(new Dimension(500,20));


        panel.add(instructions);
        panel.add(input);
        panel.add(output);
        panel.add(button);
        frame.add(panel);
        frame.setVisible(true);
    }

    public static void main(String[] args) {
        new GUI();
    }
}
