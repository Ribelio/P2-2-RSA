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
import java.io.BufferedReader;
import java.io.InputStreamReader;


public class RNGUI {

    public RNGUI() {
        JFrame frame = new JFrame("Tester");
        frame.setSize(600, 300);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setResizable(false);

        JPanel panel = new JPanel();

        JLabel welcomeLabel = new JLabel("<html><div style='text-align: center;'>Welcome!</div></html>");
        welcomeLabel.setFont(new Font("Arial", Font.BOLD, 40));

        JLabel instructions = new JLabel("<html><div style='text-align: center;'>Thank you for helping us test our program. All you have to do is to click the \"Generate\" button below. This will create two files. You can view these yourself if you wish.</div></html>");
        instructions.setFont(new Font("Arial", Font.PLAIN, 14));
        instructions.setPreferredSize(new Dimension(570, 50)); // Set preferred size
        instructions.setVerticalAlignment(JLabel.TOP);
        instructions.setHorizontalAlignment(JLabel.CENTER);
        instructions.setVerticalTextPosition(JLabel.TOP);
        instructions.setHorizontalTextPosition(JLabel.CENTER);

        JButton button = new JButton("Generate");
        button.setFocusable(false);
        button.addActionListener(new ActionListener() {

            @Override
            public void actionPerformed(ActionEvent e) {
                try{
                        String pythonScriptPath = "CSPRNG/tester.py";
                        ProcessBuilder processBuilder = new ProcessBuilder("python", pythonScriptPath);
                        Process process = processBuilder.start();

                        // Capture error output
                        BufferedReader errorReader = new BufferedReader(new InputStreamReader(process.getErrorStream()));
                        String line;
                        while ((line = errorReader.readLine()) != null) {
                            System.out.println(line);
                        }


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

        JLabel instructions2 = new JLabel("<html><div style='text-align: center;'>Once the files are created, please send them to us. After that you may exit the program. Thank you!</div></html>");
        instructions2.setFont(new Font("Arial", Font.PLAIN, 14));
        instructions2.setPreferredSize(new Dimension(570, 50)); // Set preferred size
        instructions2.setVerticalAlignment(JLabel.TOP);
        instructions2.setHorizontalAlignment(JLabel.CENTER);
        instructions2.setVerticalTextPosition(JLabel.TOP);
        instructions2.setHorizontalTextPosition(JLabel.CENTER);

        JLabel note = new JLabel("<html><div style='text-align: center;'>Note: This might take a few minutes longer if you are missing required Python libraries.</div></html>");
        note.setForeground(Color.RED);
        note.setFont(new Font("Arial", Font.PLAIN, 14));
        note.setPreferredSize(new Dimension(570, 50)); // Set preferred size
        note.setVerticalAlignment(JLabel.TOP);
        note.setHorizontalAlignment(JLabel.CENTER);
        note.setVerticalTextPosition(JLabel.TOP);
        note.setHorizontalTextPosition(JLabel.CENTER);        

        panel.add(welcomeLabel);
        panel.add(instructions);
        panel.add(button);
        panel.add(instructions2);
        panel.add(note);
        frame.add(panel);
        frame.setVisible(true);
    }

    public static void main(String[] args) {
        new RNGUI();
    }
}
