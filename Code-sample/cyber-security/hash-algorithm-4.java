import org.mindrot.jbcrypt.BCrypt;
import java.time.LocalDateTime;
…
//============================================================
///---1.Registration service (Logic)---
//============================================================
public UserModel register(String name, String username, String password) {
    …
    //BCrypt slow hashing algorithm and the output of that will be 60 characters.
    String hashedPassword = BCrypt.hashpw(password, BCrypt.gensalt(12)); //12 is the strength of hashing
    UserModel newUser = new UserModel();
    newUser.setName(name);
    newUser.setUsername(username);
    newUser.setPassword(hashedPassword);
    newUser.setCreationTime(LocalDateTime.now());

    return userRepository.save(newUser);
}


import org.mindrot.jbcrypt.BCrypt;
…
public String login(String username, String password) {
    //If we hash the password with common algorithms, the logic of checking it becomes easily possible
    //the entered raw password is compared textually with the hashed password in the database:
    if (!password.equals(user.getPassword())) {
        throw new RuntimeException("The username or password is incorrect.");
    }
    …
    //BCrypt hash check
    //compare the password string with the hash stored in the database:
    if (!BCrypt.checkpw(password, user.getPassword())) {
        throw new UserExceptionHandler.AuthenticationException("Incorrect username or password!");
    }
}