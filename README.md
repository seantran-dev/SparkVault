# SparkVault: Encrypted Password Manager

## Overview
A desktop password manager written in Python that securely stores credentials using SQLite and a custom implementation of AES-256 in CTR mode, originally written by me in Java, and now ported to Python years later. This application features a modern desktop interface and is distributed as a standalone windows executable.

I created this project to learn the principles behind security for secure credential storage and to better understand the software responsible for protecting my own sensitive information.

## Features
 - PySide6 modern desktop interface
 - User registration and authentication with Argon2 password hashing
 - Add, edit, view, and delete credentials, with clipboard copy support
 - AES-CTR and are encrypted using a key derived from the user's master password via PBKDF2
 - Encrypted passwords are stored as ciphertext and nonce pairs in database
 - Dockerized PostgreSQL database for persistent data storage

<table>
 <tr>
  
  <td align="center">
   <img width="300" height="297" alt="login" src="https://github.com/user-attachments/assets/c1bc499d-e1d8-4562-aac6-6be8edd24f1d" />
   <b>User Authentication</b><br>
  </td>
    
  <td align="center">
   <img width="300" height="296" alt="delete" src="https://github.com/user-attachments/assets/f6f600d9-5715-4b8e-91f0-6ccfe4e0813c" />
   <b>Delete Existing Credential</b><br>
  </td>

  <td align="center">
   <img width="300" height="295" alt="add" src="https://github.com/user-attachments/assets/9a96af26-48c5-485b-be22-12c7aa34b013" />
   <b>Add New Credential</b><br>
  </td>
  
 </tr>
</table>

## Technologies
 - Python (psycopg --> SQLite3)
 - PostgreSQL --> SQLite
 - Docker
 - Cryptography (AES, Argon2, PBKDF2)

## Installation
1. Clone the repository
2. Install dependencies
3. Start PostgreSQL
4. Run the application


## Project Structure

authentication/
database/
encryption/
menus/

## Security Notes
- Master passwords are hashed using Argon2 before storage.
- Stored credentials are encrypted with AES-CTR.
- Passwords are never stored or shown in plaintext and are only displayed when explicitly requested by the user.
- The application requires log-in verification on each bootup.

<img width="1826" height="176" alt="8ca6e0a805b6374d5f86a0ab70aa4a0d" src="https://github.com/user-attachments/assets/3d2ac4aa-6315-4c98-9c12-18f600f1285e" />



