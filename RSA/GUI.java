import java.awt.Button;
import java.awt.Dimension;
import java.awt.Font;
import java.io.IOException;

import javax.swing.ButtonGroup;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JPopupMenu;
import javax.swing.JRadioButton;
import javax.swing.JTabbedPane;
import javax.swing.JTextField;
import javax.swing.UIManager;
import javax.swing.UnsupportedLookAndFeelException;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.InputStreamReader;
import java.io.Reader;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.awt.GridLayout;
import java.awt.event.FocusAdapter;
import java.awt.event.FocusEvent;
import java.awt.event.FocusListener;
import java.math.BigInteger;
import javax.swing.JTextArea;

public class GUI {

    private String message;
    private BigInteger public_key;
    private BigInteger public_exp;
    private String chosenAttackMode;
    private JButton decryptButton;

    public GUI() {
        JFrame frame = new JFrame("RSA Encryption/Decryption");
        frame.setSize(1000, 400);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setResizable(false);

        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (ClassNotFoundException | InstantiationException | IllegalAccessException | UnsupportedLookAndFeelException e) {
            e.printStackTrace();
        }

        JTabbedPane tabbedPane = new JTabbedPane();
        tabbedPane.setFocusable(false);

        JPanel encryptPanel = new JPanel();
        addEncryptionObjects(encryptPanel);
        tabbedPane.addTab("Encrypt", encryptPanel);

        JPanel decryptPanel = new JPanel();
        addDecryptionComponents(decryptPanel);
        tabbedPane.addTab("Decrypt", decryptPanel);

        frame.add(tabbedPane);
        frame.setVisible(true);
    
    }


    public void addEncryptionObjects(JPanel panel) {
        JButton button = new JButton("ENCRYPT");
        button.setFocusable(false);
        

        JLabel instructions = new JLabel("<html><div style='text-align: center;'>Add whatever text you would like encrypted in the top text-box and click the button to receive a beautifully ciphered message in the bottom text-box!</div></html>");
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

        panel.setLayout(new GridLayout(4, 1)); 
        panel.add(instructions);
        panel.add(input);
        panel.add(output);
        panel.add(button);

        button.addActionListener(e -> {
            button.setText("Done!");
            button.setEnabled(false);
            String inpuString = input.getText();
            pythonScript(inpuString);
            try (BufferedReader br = new BufferedReader(new FileReader("output.txt"))) {
                String line;
                while ((line = br.readLine()) != null) {
                    output.setText(line);
                }
            } catch (IOException ex) {
                ex.printStackTrace();
            }

            File outputFile = new File("output.txt");
            outputFile.delete();
        });
    }

    private void addDecryptionComponents(JPanel panel) {
        JLabel instructions = new JLabel("<html><div style='text-align: center;'>Add the encrypted text, public key, and public exponent. Then click the button to decrypt it!</div></html>");
        instructions.setFont(new Font("Arial", Font.PLAIN, 14));
        instructions.setPreferredSize(new Dimension(570, 50));
        instructions.setVerticalAlignment(JLabel.TOP);
        instructions.setHorizontalAlignment(JLabel.CENTER);
        instructions.setVerticalTextPosition(JLabel.TOP);
        instructions.setHorizontalTextPosition(JLabel.CENTER);

        decryptButton = new JButton("DECRYPT");
        decryptButton.setFocusable(false);

        JTextField input = new JTextField("Encrypted Message");
        input.setPreferredSize(new Dimension(500, 20));
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
                decryptButton.setText("DECRYPT");
                decryptButton.setEnabled(true);
            }
        });

        JTextField input2 = new JTextField("Public Key (n)");
        input2.setPreferredSize(new Dimension(500, 20));
        input2.getDocument().addDocumentListener(new DocumentListener() {
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
                decryptButton.setText("DECRYPT");
                decryptButton.setEnabled(true);
            }
        });

        JTextField input3 = new JTextField("Public Exponent (e)");
        input3.setPreferredSize(new Dimension(500, 20));
        input3.getDocument().addDocumentListener(new DocumentListener() {
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
                decryptButton.setText("DECRYPT");
                decryptButton.setEnabled(true);
            }
        });

        JTextArea output = new JTextArea("Output");
        output.setLineWrap(true);
        output.setWrapStyleWord(true);
        output.setEditable(false);
        output.setPreferredSize(new Dimension(500, 20));


        JRadioButton bruteforceButton = new JRadioButton("Bruteforce Attack");
        bruteforceButton.setFocusable(false);
        bruteforceButton.setSelected(true);
        JRadioButton mathematicalButton = new JRadioButton("Mathematical Attack");
        mathematicalButton.setFocusable(false);
        JRadioButton timingButton = new JRadioButton("Timing Attack");
        timingButton.setFocusable(false);

        ButtonGroup group = new ButtonGroup();
        group.add(bruteforceButton);
        group.add(mathematicalButton);
        group.add(timingButton);
   
        JPanel radioButtonsPanel = new JPanel();
        radioButtonsPanel.add(bruteforceButton);
        radioButtonsPanel.add(mathematicalButton);
        radioButtonsPanel.add(timingButton);

        panel.setLayout(new GridLayout(7, 1));
        panel.add(instructions);
        panel.add(input);
        panel.add(input2);
        panel.add(input3);
        panel.add(radioButtonsPanel);   
        panel.add(output);
        panel.add(decryptButton);

        decryptButton.addActionListener(e -> {
            decryptButton.setEnabled(false);

            message = input.getText();
            try {
                public_key = new BigInteger(input2.getText());
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(null, "Public key is not a number", "Input Error", JOptionPane.ERROR_MESSAGE);
            }
            try {
                public_exp = new BigInteger(input3.getText());
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(null, "Public exponent is not a number", "Input Error", JOptionPane.ERROR_MESSAGE);
            }
            if (bruteforceButton.isSelected() == true) {
                chosenAttackMode = "bruteforce";
            } else if (mathematicalButton.isSelected() == true) {
                chosenAttackMode = "mathematical";
            } else {chosenAttackMode = "timing";}
            
            String fileName = "encrypted_text_info.txt";

            try {
                BufferedWriter writer = new BufferedWriter(new FileWriter(fileName));
                writer.write("Encrypted Text (Base64):\n");
                writer.write(message + "\n\n"); 
                writer.write("Public Key (n):\n");
                writer.write(public_key + "\n\n"); 
                writer.write("Public Exponent (e):\n");
                writer.write(public_exp + "\n\n"); 
                writer.write("Method:\n");
                writer.write(chosenAttackMode + "\n");
                writer.close();
            } catch (IOException exep) {
                exep.printStackTrace();
            }

            pythonScriptDecrypt(fileName);

            try (BufferedReader br = new BufferedReader(new FileReader("output.txt"))) {
                String line;
                while ((line = br.readLine()) != null) {
                    output.setText(line);
                }
            } catch (IOException ex) {
                ex.printStackTrace();
            }

            File outputFile = new File("output.txt");
            outputFile.delete();

        });
    }
    
    
    private void pythonScriptDecrypt(String file) {
        String pythonScriptPath;
        if (chosenAttackMode == "bruteforce") {
            pythonScriptPath = "Decrypt/bruteforce.py";
        } else if (chosenAttackMode == "mathematical") {
            pythonScriptPath = "Decrypt/mathematical.py";
        } else if (chosenAttackMode == "timing") {
            pythonScriptPath = "Decrypt/timing.py";
        } else {pythonScriptPath = null;};

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
                decryptButton.setText("Done!");
            } else if (exitCode == 2) {
                System.out.println("Error executing Python script, exit code: " + exitCode);
                decryptButton.setText("Public key is too large for bruteforce.");
            } else if (exitCode == 1) {
                decryptButton.setText("Something went wrong. Verify that the public key is correct.");
            }
            
        } catch(IOException e) {
            System.out.println("Error reading from the error stream");
            e.printStackTrace();
        } catch(InterruptedException e) {
            System.out.println("Error waiting for the process to finish");
            e.printStackTrace();
        }
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
