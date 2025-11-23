// Simulating a Junior Developer's Spring Boot code
public class user_controller {  // Error: Should be PascalCase (UserController)

    String db_password = "secret_password_123"; // Error: Hardcoded secret
    
    public void GetData() { // Error: Method should be camelCase (getData)
        System.out.println("Connecting to DB with: " + db_password);
    }
}