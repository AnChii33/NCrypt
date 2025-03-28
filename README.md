# NCrypt – Prototype Multi-Layered File Encryption Tool

## Overview
NCrypt is a prototype encryption tool comprised of two coupled utilities: **Encryptor** and **Decryptor**. It is designed to securely encrypt text files by applying multiple layers of encryption, then removing the original content from local storage. The decryption process restores the original file only when all the correct keys are provided in reverse order.

## How It Works

### Encryption
1. **Launch the Encryptor:**  
   - Open the Encryptor tool.
   - Select the text file to encrypt.
   - Enter the desired number of encryption layers.
   - Click **Submit**.
2. **Encryption Process:**  
   - The file’s content is encrypted.
   - The original content is removed from local storage and replaced with the message:  
     `"THIS FILE IS ENCRYPTED"`.
   - The tool displays all the generated keys, including a final key, in its lower section.

### Decryption
1. **Launch the Decryptor:**  
   - Open the Decryptor tool.
   - Select the file to decrypt.
   - Enter the number of layers used during encryption and the final key.
   - Click **Submit**.
   - If the final key or number of layers does not match, an error is shown.
2. **Key Submission:**  
   - If the initial check passes, you are prompted to enter the remaining keys in **reverse order**.
   - Click **Submit keys**.
3. **Decryption Outcome:**  
   - If all keys are correct, the tool displays `"SUCCESSFULLY DECRYPTED!"` and restores the original file content.
   - If any key is incorrect, it displays `"DECRYPTION FAILED! Invalid keys detected..."` and the file remains unchanged.

## Tech Stack
- **Programming Language:** Python
- **UI:** Tkinter
- **Database:** MongoDB

# IMPORTANT: NCrypt is a prototype and not a fully developed encryption product. Use it for educational and experimental purposes only.  
