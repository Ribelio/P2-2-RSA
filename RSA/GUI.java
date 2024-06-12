import java.awt.Dimension;
import java.awt.Font;
import java.io.IOException;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;

import java.io.BufferedReader; // Import the BufferedReader class
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.awt.GridLayout;
import java.awt.event.FocusAdapter;
import java.awt.event.FocusEvent;
import java.awt.event.FocusListener;
import java.math.BigInteger;
import javax.swing.JTextArea;


public class GUI {

    public GUI() {
        JFrame frame = new JFrame("RSA Encryption/Decryption");
        frame.setSize(600, 300);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setResizable(false);

        JPanel panel = new JPanel();

        JButton button = new JButton("ENCRYPT");
        button.setFocusable(false);
        

        JLabel instructions = new JLabel("<html><div style='text-align: center;'>Add whatever text you would like encrypted in the left text-box and click the button to receive a beautifully ciphered message in the right text-box!</div></html>");
        instructions.setFont(new Font("Arial", Font.PLAIN, 14));
        instructions.setPreferredSize(new Dimension(570, 50)); // Set preferred size
        instructions.setVerticalAlignment(JLabel.TOP);
        instructions.setHorizontalAlignment(JLabel.CENTER);
        instructions.setVerticalTextPosition(JLabel.TOP);
        instructions.setHorizontalTextPosition(JLabel.CENTER);

        JTextField input = new JTextField("Input");
        input.setPreferredSize(new Dimension(500,20));
        input.getDocument().addDocumentListener(new DocumentListener() {
            @Override
            public void insertUpdate(DocumentEvent e) {
                textChanged();
            }

            @Override
            public void removeUpdate(DocumentEvent e) {
                textChanged();
            }

            @Override
            public void changedUpdate(DocumentEvent e) {
                textChanged();
            }

            // This method will be called whenever the text changes
            private void textChanged() {
                button.setText("ENCRYPT");
                button.setEnabled(true);
            }
        });

        JTextArea output = new JTextArea("Output");
        output.setLineWrap(true);
        output.setWrapStyleWord(true);
        output.setEditable(false);
        output.setPreferredSize(new Dimension(500,20));

        panel.setLayout(new GridLayout(4, 1)); // Set panel layout to GridLayout with 4 rows and 1 column
        panel.add(instructions);
        panel.add(input);
        panel.add(output);
        panel.add(button);
        frame.add(panel);
        frame.setVisible(true);

        button.addActionListener(e -> {
            button.setText("Done!");
            button.setEnabled(false);
            String inpuString = input.getText();
            pythonScript(inpuString);
            try {
                byte[] bytes = Files.readAllBytes(Paths.get("output.bin"));
                String outputString = new BigInteger(1, bytes).toString(16);
                output.setText(outputString);
            } catch (IOException e1) {}
/*             @Override
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
            } */
        });

    }
    
    
    
    private void pythonScript(String inputString) {
        try {
            Files.write(Paths.get("input.txt"), inputString.getBytes());
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        String pythonScriptPath = "RSA/encrypt_CSPRNG.py";
        ProcessBuilder processBuilder = new ProcessBuilder(
            "python", 
            pythonScriptPath);
        Process process;
        
        try {
            process = processBuilder.start();

            // Capture error output
            BufferedReader errorReader = new BufferedReader(new InputStreamReader(process.getErrorStream()));
            String line;
            while ((line = errorReader.readLine()) != null) {
                System.out.println(line);
            }

            // Capture the output from the Python script
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }

            int exitCode = process.waitFor();
            if (exitCode == 0) {
                System.out.println("Python script executed successfully");
            } else {
                System.out.println("Error executing Python script, exit code: " + exitCode);
            }
            
            } catch(IOException e) {
                System.out.println("Error reading from the error stream");
                e.printStackTrace();
            } catch(InterruptedException e) {
                System.out.println("Error waiting for the process to finish");
                e.printStackTrace();
            }
    }

    public static void main(String[] args) {
        new GUI();
    }
}
